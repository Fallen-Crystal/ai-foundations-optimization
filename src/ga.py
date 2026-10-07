"""Mixed binary/real genetic algorithm; no reference solver is imported."""
import time
import numpy as np
from .problem import objective, violations, feasible, repair, TARGET

def run_ga(config, seed=0):
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    n = config['population_size']
    if n < 2 or not 1 <= config['elite_count'] < n:
        raise ValueError('Require population>=2 and 1<=elite_count<population')
    raw = np.column_stack([rng.integers(0, 2, (n, 5)),
                           rng.uniform([1, 0], [4, 3.5], (n, 2))])
    population = np.array([repair(x, rng) for x in raw])
    best_x, best_f, first_hit = None, float('inf'), None
    history = []
    for generation in range(config['generations']+1):
        values = objective(population)
        residuals = violations(population)
        valid = feasible(population, config['feasibility_tolerance'])
        scores = values + config['penalty_weight']*np.sum(residuals**2, axis=1)
        if valid.any():
            ids = np.flatnonzero(valid)
            i = ids[np.argmin(values[ids])]
            if values[i] < best_f:
                best_f, best_x = float(values[i]), population[i].copy()
        if first_hit is None and best_x is not None and abs(best_f-TARGET) <= config['target_tolerance']:
            first_hit = generation
        history.append(dict(seed=seed, generation=generation,
                            best_feasible_objective=best_f if best_x is not None else None,
                            best_penalized_score=float(scores.min()),
                            feasible_fraction=float(valid.mean())))
        if generation == config['generations']:
            break
        def select():
            ids = rng.integers(n, size=config['tournament_size'])
            return population[ids[np.argmin(scores[ids])]].copy()
        next_population = [x.copy() for x in population[np.argsort(scores)[:config['elite_count']]]]
        while len(next_population) < n:
            a, b = select(), select()
            child = a.copy()
            if rng.random() < config['crossover_rate']:
                mask = rng.random(5) < .5
                child[:5] = np.where(mask, a[:5], b[:5])
                alpha = rng.random(2)
                child[5:] = alpha*a[5:] + (1-alpha)*b[5:]
            flips = rng.random(5) < config['bit_mutation_rate']
            child[:5] = np.where(flips, 1-child[:5], child[:5])
            mutations = rng.random(2) < config['real_mutation_rate']
            child[5:] += mutations*rng.normal(0, config['mutation_sigma'], 2)
            next_population.append(repair(child, rng))
        population = np.array(next_population)
    return dict(seed=seed, objective=best_f if best_x is not None else None,
                feasible=best_x is not None,
                success=first_hit is not None, chromosome=best_x.tolist() if best_x is not None else None,
                first_target_generation=first_hit, runtime_seconds=time.perf_counter()-start,
                history=history)
