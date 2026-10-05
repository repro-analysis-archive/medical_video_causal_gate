/* decode_bench.c - in-process H.264 decode benchmark for sampling a fixed physical-time grid (synthetic test videos
 * only; never run on DS203 files).
 * usage: decode_bench <file> <cpu|nvdec> <seq|seek|hybrid|keyonly> <rate_fps> <threads>
 *   seq     : decode every frame; keep the first frame at or after each grid time k/rate
 *   seek    : for every grid time, seek to the preceding keyframe, flush, decode forward to the grid time
 *   hybrid  : seek only when the grid time lies beyond the next keyframe; otherwise keep decoding forward
 *   keyonly : decode keyframes only (AVDISCARD_NONKEY; samples at keyframe times, not on the grid) - reference
 *   skip    : like hybrid, but jumps forward without av_seek_frame / decoder flush: packets are read and discarded
 *             until the keyframe preceding the grid time (all bytes are still read; added after the main matrix run,
 *             the other strategies' code is unchanged)
 * Selected NVDEC frames are copied to host memory (av_hwframe_transfer_data), as a model input pipeline would need.
 * Prints one JSON line. Timing excludes container open and decoder creation (reported separately as init_s). */
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/hwcontext.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
static enum AVPixelFormat hw_fmt(AVCodecContext *c, const enum AVPixelFormat *f) {
    for (; *f != AV_PIX_FMT_NONE; f++) if (*f == AV_PIX_FMT_CUDA) return *f;
    fprintf(stderr, "CUDA pixel format not offered\n"); return AV_PIX_FMT_NONE;
}

static AVFormatContext *fmt; static AVCodecContext *ctx; static AVStream *st; static int si, hw;
static AVPacket *pkt; static AVFrame *fr, *sw;
static long n_dec = 0, n_sel = 0, n_seek = 0, n_xfer_fail = 0, n_skipped = 0; static int eof = 0;
static int64_t skip_until = INT64_MIN, last_sent_dts = INT64_MIN;

static void select_frame(void) {
    n_sel++;
    if (hw) { av_frame_unref(sw); if (av_hwframe_transfer_data(sw, fr, 0) < 0) n_xfer_fail++; }
}
/* decode the next frame into fr; returns 0 on success, <0 at end of stream */
static int next_frame(int keyonly) {
    for (;;) {
        int r = avcodec_receive_frame(ctx, fr);
        if (r == 0) { n_dec++; return 0; }
        if (r == AVERROR_EOF) return -1;
        if (eof) return -1;
        r = av_read_frame(fmt, pkt);
        if (r < 0) { eof = 1; avcodec_send_packet(ctx, NULL); continue; }
        if (pkt->stream_index == si && skip_until != INT64_MIN) {
            if ((pkt->flags & AV_PKT_FLAG_KEY) && pkt->dts >= skip_until) skip_until = INT64_MIN;
            else { n_skipped++; av_packet_unref(pkt); continue; }
        }
        if (pkt->stream_index == si && (!keyonly || (pkt->flags & AV_PKT_FLAG_KEY))) { last_sent_dts = pkt->dts; avcodec_send_packet(ctx, pkt); }
        av_packet_unref(pkt);
    }
}
static int64_t fpts(void) { return fr->best_effort_timestamp != AV_NOPTS_VALUE ? fr->best_effort_timestamp : fr->pts; }

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: %s file cpu|nvdec seq|seek|hybrid|keyonly|skip rate threads\n", argv[0]); return 2; }
    const char *file = argv[1], *mode = argv[3]; hw = !strcmp(argv[2], "nvdec"); double rate = atof(argv[4]); int threads = atoi(argv[5]);
    int keyonly = !strcmp(mode, "keyonly");
    av_log_set_level(AV_LOG_ERROR);
    double t0 = now();
    if (avformat_open_input(&fmt, file, NULL, NULL) < 0 || avformat_find_stream_info(fmt, NULL) < 0) { fprintf(stderr, "open failed\n"); return 1; }
    AVCodec *dec = NULL; si = av_find_best_stream(fmt, AVMEDIA_TYPE_VIDEO, -1, -1, &dec, 0); st = fmt->streams[si];
    ctx = avcodec_alloc_context3(dec); avcodec_parameters_to_context(ctx, st->codecpar);
    AVBufferRef *dev = NULL;
    if (hw) {
        if (av_hwdevice_ctx_create(&dev, AV_HWDEVICE_TYPE_CUDA, NULL, NULL, 0) < 0) { fprintf(stderr, "cuda device failed\n"); return 1; }
        ctx->hw_device_ctx = av_buffer_ref(dev); ctx->get_format = hw_fmt; ctx->thread_count = 1;
    } else { ctx->thread_count = threads; ctx->thread_type = FF_THREAD_FRAME | FF_THREAD_SLICE; }
    if (keyonly) ctx->skip_frame = AVDISCARD_NONKEY;
    if (avcodec_open2(ctx, dec, NULL) < 0) { fprintf(stderr, "decoder open failed\n"); return 1; }
    pkt = av_packet_alloc(); fr = av_frame_alloc(); sw = av_frame_alloc();
    double dur = st->duration != AV_NOPTS_VALUE ? st->duration * av_q2d(st->time_base) : fmt->duration / (double)AV_TIME_BASE;
    int64_t start = st->start_time != AV_NOPTS_VALUE ? st->start_time : 0;
    long n_tgt = (long)(dur * rate - 1e-9) + 1;
    double t1 = now();
    if (!strcmp(mode, "seq") || keyonly) {
        long k = 0;
        while (next_frame(keyonly) == 0) {
            int64_t p = fpts();
            if (keyonly) { select_frame(); continue; }
            if (k < n_tgt && p >= start + (int64_t)(k / rate / av_q2d(st->time_base))) {
                select_frame();
                while (k < n_tgt && p >= start + (int64_t)(k / rate / av_q2d(st->time_base))) k++;
            }
        }
    } else {
        int hybrid = !strcmp(mode, "hybrid"), skip = !strcmp(mode, "skip"); int64_t last = INT64_MIN;
        for (long k = 0; k < n_tgt; k++) {
            int64_t ts = start + (int64_t)(k / rate / av_q2d(st->time_base));
            int need_seek = 1;
            if (skip) {
                need_seek = 0;
                int i = av_index_search_timestamp(st, ts, AVSEEK_FLAG_BACKWARD);
                if (i >= 0 && st->index_entries[i].timestamp > last_sent_dts) { skip_until = st->index_entries[i].timestamp; n_seek++; }
            }
            else if (hybrid && last != INT64_MIN && last < ts) {
                int i = av_index_search_timestamp(st, ts, AVSEEK_FLAG_BACKWARD);
                if (i >= 0 && st->index_entries[i].timestamp <= last) need_seek = 0;
            }
            if (need_seek) {
                if (av_seek_frame(fmt, si, ts, AVSEEK_FLAG_BACKWARD) < 0) break;
                avcodec_flush_buffers(ctx); eof = 0; n_seek++;
            }
            int got = 0;
            while (next_frame(0) == 0) { last = fpts(); if (last >= ts) { got = 1; break; } }
            if (!got) break;
            select_frame();
        }
    }
    double t2 = now();
    printf("{\"file\":\"%s\",\"device\":\"%s\",\"mode\":\"%s\",\"rate\":%g,\"threads\":%d,\"video_s\":%.3f,\"targets\":%ld,"
           "\"selected\":%ld,\"decoded\":%ld,\"seeks\":%ld,\"skipped_packets\":%ld,\"xfer_fail\":%ld,\"init_s\":%.4f,\"wall_s\":%.4f,\"x_realtime\":%.3f}\n",
           file, hw ? "nvdec" : "cpu", mode, rate, hw ? 1 : threads, dur, keyonly ? 0 : n_tgt, n_sel, n_dec, n_seek, n_skipped, n_xfer_fail,
           t1 - t0, t2 - t1, dur / (t2 - t1));
    av_frame_free(&fr); av_frame_free(&sw); av_packet_free(&pkt); avcodec_free_context(&ctx); avformat_close_input(&fmt); av_buffer_unref(&dev);
    return 0;
}
