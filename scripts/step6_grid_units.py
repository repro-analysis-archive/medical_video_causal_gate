"""Run the locked causal-grid units of §14 step 6 without the §14 step-7 aggregation (orchestration only).

`ss_benchmark.grid_driver.main` runs every (set, cell, replicate) unit — one locked `_unit` call each, written as a
shard; finished shards are skipped, so a rerun resumes — and then calls `aggregate`, which writes replicates.csv,
cell_metrics.csv and families.json (family verdicts, §12.3). The aggregation belongs to §14 step 7, which this runner
never runs. This launcher therefore replaces the module attribute `grid_driver.aggregate` by a function that only
logs, and then calls the locked `main` unchanged with the given arguments. Unit construction, seeds, learners,
workers and shard files are exactly the locked driver's. Step 7 later runs the locked `main` with the same arguments:
every shard exists, so it only aggregates.

    python scripts/step6_grid_units.py <grid_driver arguments>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ss_benchmark import grid_driver  # noqa: E402


def _no_step7(out, units, conditions, gsite):
    print(f"all {len(units)} units present; aggregation and family verdicts (§14 step 7) not run by the step-6 runner",
          flush=True)


if __name__ == "__main__":
    grid_driver.aggregate = _no_step7
    sys.exit(grid_driver.main(sys.argv[1:]))
