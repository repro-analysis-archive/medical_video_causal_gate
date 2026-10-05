"""Launch one locked ss_benchmark.pipeline command with the run's execution settings (orchestration only).

Settings (CC_TASK_SS_resource_policy_v1.md); none of them is an analysis choice:
* torch intra-op threads = --threads (OMP / MKL thread variables are set to the same value by the orchestrator);
* deterministic GPU settings: cudnn.deterministic = True, cudnn.benchmark = False and
  torch.use_deterministic_algorithms(True, warn_only=True) ("where supported"); CUBLAS_WORKSPACE_CONFIG is set by the
  orchestrator before CUDA initialises.
Then ss_benchmark.pipeline.main(<args>) runs unchanged from the run's code snapshot (this file's repository root).

    python scripts/step4_5_launch.py --threads N -- mask-check --videos DIR --out FILE
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv):
    if len(argv) < 3 or argv[0] != "--threads" or argv[2] != "--":
        raise SystemExit("usage: step4_5_launch.py --threads N -- <pipeline args>")
    threads, args = int(argv[1]), argv[3:]
    import torch
    torch.set_num_threads(threads)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True, warn_only=True)
    sys.path.insert(0, ROOT)
    from ss_benchmark import pipeline
    return pipeline.main(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
