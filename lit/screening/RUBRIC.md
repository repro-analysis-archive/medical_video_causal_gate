# Screening rubric (verbatim from lit/SEARCH_IMPLEMENTATION.md §5; gate baadf5c §6)

For each record, decide from title + abstract (+ venue) exactly one of NONE, RELATED, FULLTEXT.

FULLTEXT (possible DIRECT/PARTIAL; will be read in full by the lead analyst) if ANY holds:
(L1) learned/foundation/generative image, video or text representations are used as adjustment covariates or
     confounder proxies for a causal effect of an action or treatment;
(L2) learned representations are analysed as carrying acquisition information (site, scanner, device, operator,
     batch) that affects bias, confounding adjustment or overlap in causal estimation;
(L3) a semi-synthetic causal benchmark built on real medical images or video;
(L4) causal role of acquisition information in representations as a function of duration/persistence, or the effect
     of site-invariant / harmonized / debiased representations on causal estimation in longitudinal or sequential
     settings.
RELATED: adjacent but none of the above (e.g. site/shortcut leakage in embeddings without causal estimation; causal
inference with images without learned representations as adjustment; generic identification theory; counterfactual
image generation without causal effect estimation of an action/treatment).
NONE: otherwise.
Records without an abstract: screen on title/venue; if a FULLTEXT criterion cannot be ruled out -> FULLTEXT.
When in doubt between RELATED and FULLTEXT, choose FULLTEXT. Never assign DIRECT or PARTIAL.
