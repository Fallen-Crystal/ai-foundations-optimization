"""Original seven-variable coursework problem and problem-specific repair."""
import numpy as np

LOWER = np.array([1., 0.])
UPPER = np.array([4., 3.5])
TARGET = -6.0

def objective(x):
    x = np.asarray(x, dtype=float)
    u, v = x[..., :5], x[..., 5:]
    return np.sum(u*u - 3*u, axis=-1) + 2*(v[..., 0]-v[..., 1])**2

def violations(x):
    """Nonnegative residuals: count, inequality, equality, box, integrality."""
    x = np.asarray(x, dtype=float)
    u, v = x[..., :5], x[..., 5:]
    return np.stack([
        np.maximum(u.sum(axis=-1)-3, 0),
        np.maximum(1-2*v[..., 0]+1.2*v[..., 1], 0),
        np.abs(u[..., 1]*v[..., 0]+u[..., 3]*v[..., 1]-2.2),
        np.maximum(LOWER-v, 0).sum(axis=-1)+np.maximum(v-UPPER, 0).sum(axis=-1),
        np.minimum(np.abs(u), np.abs(u-1)).sum(axis=-1),
    ], axis=-1)

def feasible(x, tolerance=1e-8):
    return np.all(violations(x) <= tolerance, axis=-1)

def repair(x, rng):
    """Repair binary/count constraints and project to equality plus box only.

    The inequality remains in the penalty; no optimal continuous value is seeded.
    """
    x = np.asarray(x, dtype=float).copy()
    u = (x[:5] >= .5).astype(float)
    if u[1] == 0 and u[3] == 0:
        u[rng.choice([1, 3])] = 1
    while u.sum() > 3:
        candidates = np.flatnonzero(u)
        # Keep at least one equality coefficient active.
        candidates = [i for i in candidates if not (i in (1, 3) and u[1]+u[3] == 1)]
        u[rng.choice(candidates)] = 0
    v = np.clip(x[5:], LOWER, UPPER)
    if u[1] == 1 and u[3] == 0:
        v[0] = 2.2
    elif u[1] == 0 and u[3] == 1:
        v[1] = 2.2
    else:
        # Exact projection to {(t,2.2-t): 1<=t<=2.2}.
        t = np.clip((v[0]-v[1]+2.2)/2, 1., 2.2)
        v[:] = [t, 2.2-t]
    return np.concatenate([u, v])
