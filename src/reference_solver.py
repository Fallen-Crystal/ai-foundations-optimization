"""Independent enumeration with analytic continuous interval minimization."""
from itertools import product
import numpy as np
from .problem import objective, feasible

def solve_reference():
    cases = []
    for bits in product([0, 1], repeat=5):
        u = np.array(bits)
        if u.sum() > 3 or (u[1] == 0 and u[3] == 0):
            continue
        if u[1] == 1 and u[3] == 0:
            # v1=2.2; inequality implies v2 <= (4.4-1)/1.2.
            v = np.array([2.2, np.clip(2.2, 0, min(3.5, (4.4-1)/1.2))])
        elif u[1] == 0 and u[3] == 1:
            # v2=2.2; inequality implies v1 >= (1+1.2*2.2)/2.
            v = np.array([np.clip(2.2, max(1, (1+1.2*2.2)/2), 4), 2.2])
        else:
            # v=(t,2.2-t); inequality requires 3.2t >= 3.64.
            lo, hi = max(1., 2.2-3.5, 3.64/3.2), min(4., 2.2)
            v = np.array([np.clip(1.1, lo, hi), 0.])
            v[1] = 2.2-v[0]
        x = np.concatenate([u, v])
        if not feasible(x):
            raise AssertionError('Reference candidate violated constraints')
        cases.append(dict(chromosome=x.tolist(), objective=float(objective(x))))
    best = min(c['objective'] for c in cases)
    optima = [c for c in cases if abs(c['objective']-best) <= 1e-10]
    return dict(objective=best, chromosome=optima[0]['chromosome'],
                optima=optima, feasible_binary_patterns=len(cases), cases=cases)

if __name__ == '__main__':
    import json
    print(json.dumps(solve_reference(), indent=2))
