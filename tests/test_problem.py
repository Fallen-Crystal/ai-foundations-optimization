import numpy as np
from src.problem import objective, violations, feasible, repair

def test_known_optimum():
    x = [1, 1, 1, 0, 0, 2.2, 2.2]
    assert objective(x) == -6
    assert feasible(x)
    np.testing.assert_allclose(violations(x), 0, atol=1e-12)

def test_constraints_and_objective():
    x = [1, 1, 1, 1, 0, 1, 2]
    assert objective(x) == -6
    assert not feasible(x)
    np.testing.assert_allclose(violations(x), [1, 1.4, .8, 0, 0])
    assert not feasible([.5, 1, 1, 0, 0, 2.2, 2.2])
    assert not feasible([1, 1, 1, 0, 0, 4.1, 0])

def test_repair_equality_box_count_and_binary():
    rng = np.random.default_rng(123)
    for _ in range(500):
        x = repair(rng.uniform(-5, 8, 7), rng)
        res = violations(x)
        np.testing.assert_allclose(res[[0, 2, 3, 4]], 0, atol=1e-12)
    # Repair intentionally leaves inequality infeasibility for penalty handling.
    x = repair([0, 1, 0, 1, 0, 1, 1.2], rng)
    assert violations(x)[1] > 0
