# Dataset-record screening rubric (data_audit/SEARCH_IMPLEMENTATION.md §3; gate baadf5c §3)

For each record (title + description/abstract + url), assign exactly one category:
- DATASET-C-COL: the record releases, hosts or describes a dataset of COLONOSCOPY video (lower-GI endoscopy video,
  including datasets mixing colonoscopy with other GI endoscopy). Include clip-level and single-centre ones; the
  later audit decides multi-centre / full-procedure.
- DATASET-C-SURG: the record releases, hosts or describes a dataset of SURGICAL video with linked labels or
  annotations (e.g. phases, tools, actions, skill), INCLUDING robotic-surgery datasets with recorded kinematics.
- DATASET-OTHER: the record is a dataset, but neither of the above (e.g. static images only, other endoscopy such as
  gastroscopy/bronchoscopy/capsule only, ultrasound, non-medical).
- NOT-DATASET: not a dataset release/description (e.g. a method paper merely using a dataset, a review, an
  unrelated record). If a method paper clearly introduces a NEW colonoscopy/surgical video dataset, classify it as
  the dataset category, not NOT-DATASET.
Also give dataset_name: the dataset's name if identifiable (e.g. "REAL-Colon", "Cholec80", "JIGSAWS"), else "".
When in doubt between a DATASET-C-* category and anything else, choose the DATASET-C-* category.
