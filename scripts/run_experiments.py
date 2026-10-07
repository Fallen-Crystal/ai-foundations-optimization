import argparse, json, platform
import numpy as np
import pandas as pd
from common import ROOT, load_config
from src.ga import run_ga
from src.reference_solver import solve_reference
p = argparse.ArgumentParser()
p.add_argument('--seeds', type=int, default=30)
p.add_argument('--config')
a = p.parse_args()
if a.seeds < 1:
    p.error('--seeds must be positive')
cfg = load_config(a.config)
out = ROOT/'data/results'
out.mkdir(parents=True, exist_ok=True)
ref = solve_reference()
assert abs(ref['objective']+6) < 1e-10
(out/'reference.json').write_text(json.dumps(ref, indent=2)+'\n')
rows, histories = [], []
for seed in range(a.seeds):
    r = run_ga(cfg, seed)
    histories.extend(r.pop('history'))
    x = r.pop('chromosome')
    r.update({name: value for name, value in zip(['u1','u2','u3','u4','u5','v1','v2'], x or [None]*7)})
    rows.append(r)
    print(f"seed={seed:02d} feasible={r['feasible']} f={r['objective']} success={r['success']}", flush=True)
df = pd.DataFrame(rows)
df.to_csv(out/'raw_runs.csv', index=False)
pd.DataFrame(histories).to_csv(out/'convergence_history.csv', index=False)
# Read the persisted data so the summary is based on the delivered CSV.
df = pd.read_csv(out/'raw_runs.csv')
vals = df.loc[df.feasible, 'objective']
summary = dict(runs=len(df), feasible_runs=int(df.feasible.sum()),
               success_rate=float(df.success.mean()), mean=float(vals.mean()),
               std=float(vals.std(ddof=1)), best=float(vals.min()), worst=float(vals.max()),
               mean_runtime_seconds=float(df.runtime_seconds.mean()),
               mean_first_target_generation=float(df.first_target_generation.mean()))
pd.DataFrame([summary]).to_csv(out/'summary.csv', index=False)
metadata = dict(python=platform.python_version(), platform=platform.platform(),
                numpy=np.__version__, pandas=pd.__version__, config=cfg,
                seeds=list(range(a.seeds)), feasibility_tolerance=cfg['feasibility_tolerance'],
                success_definition='feasible and abs(objective + 6) <= target_tolerance')
(out/'experiment_metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
print(json.dumps(summary, indent=2))
