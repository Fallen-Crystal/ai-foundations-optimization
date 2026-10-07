import numpy as np
from src.reference_solver import solve_reference
from src.problem import feasible

def test_reference_optimum_and_all_patterns():
    r = solve_reference()
    assert abs(r['objective']+6) < 1e-12
    assert r['feasible_binary_patterns'] == 18
    assert len(r['optima']) == 6
    assert all(feasible(c['chromosome']) for c in r['cases'])
    both = [c for c in r['cases'] if c['chromosome'][1] == c['chromosome'][3] == 1]
    best_both = min(both, key=lambda c:c['objective'])
    np.testing.assert_allclose(best_both['chromosome'][5:], [1.1375, 1.0625])
    assert abs(best_both['objective']-(-5.98875)) < 1e-12
