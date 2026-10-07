# Session Status

Date: 2026-10-08 (Asia/Shanghai)

## Completed

- Model instruction corrected to GPT-6.1 sol / Medium; no model switching requested or performed by project scripts.
- Problem transcribed from the clear coursework image, including all constraints and course requirements.
- GitHub repository created; visibility changed to PUBLIC at user request.
- Mixed-encoding GA implemented from scratch; independent analytic/enumeration reference solver implemented.
- 30 independent seeds (0..29), all 200 generations, raw results, summary and 6030 history rows saved.
- Convergence and per-run statistics figures generated and visually checked.
- README generated from delivered CSV data. Technical report deferred per latest user instruction; the unpushed local draft was removed.
- Corrected runbook saved as docs/runbook_corrected.pdf; original prompt pages reflowed to prevent clipping.

## Verified

- GitHub initial create and push: PASS.
- Most recent experiment milestone local SHA: bd99797 (the final SHA is resolved by the command below).
- Visibility read-back: PUBLIC.
- pytest: PASS, 5 passed, both implementation and fresh virtual environment.
- Fresh-environment installation from requirements-lock.txt: PASS, Python 3.12.13.
- run_once.py in fresh environment: PASS, feasible objective -6 and all constraint residuals zero.
- Reference optimum: PASS, -6, 18 feasible binary patterns, 6 global optimal points.
- 30-run experiment: PASS, all feasible and successful at the configured threshold.
- CSV audit: PASS, 30 seeds, 6030 rows, objective/constraints/statistics/first-target checks.
- Fixed-seed reproduction: PASS (runtime excluded).
- Figures and corrected PDF pages: visually checked.
- Final local/remote SHA: run `python scripts/verify_github.py`; the delivery receipt stores the exact SHA after the last commit and push.

## Remaining

- Fill author, student ID, class and contact placeholders before coursework submission.
- Technical report is intentionally outside the current preliminary-experiment scope. Write it later when requested, using the course template.
- Python 3.11 was not separately tested; actual clean-environment validation used 3.12.13.

## Exact next command

```bash
source .venv/bin/activate
python scripts/run_once.py
python scripts/verify_github.py
```

The final commit cannot embed its own commit hash in a tracked file. Exact final local/remote hashes are recorded in the adjacent delivery receipt and can be recomputed by the verification script without changing the working tree.
