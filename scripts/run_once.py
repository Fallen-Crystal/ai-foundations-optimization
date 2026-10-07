import argparse, json
from common import load_config
from src.ga import run_ga
from src.problem import violations
p = argparse.ArgumentParser()
p.add_argument('--seed', type=int, default=0)
p.add_argument('--config')
a = p.parse_args()
r = run_ga(load_config(a.config), a.seed)
r.pop('history')
if r['chromosome'] is not None:
    r['constraint_residuals'] = violations(r['chromosome']).tolist()
print(json.dumps(r, indent=2, ensure_ascii=False))
if not r['feasible']:
    raise SystemExit(1)
