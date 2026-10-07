import json
from pathlib import Path
from src.ga import run_ga
from src.problem import feasible

def test_seed_reproducibility():
    cfg = json.loads((Path(__file__).resolve().parents[1]/'configs/baseline.json').read_text())
    cfg.update(population_size=30, generations=30)
    a, b = run_ga(cfg, 42), run_ga(cfg, 42)
    a.pop('runtime_seconds');b.pop('runtime_seconds')
    assert a == b
    assert a['feasible'] and feasible(a['chromosome'])
    assert a['objective'] >= -6-1e-10
