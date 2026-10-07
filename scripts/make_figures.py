from common import ROOT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
out = ROOT/'artifacts/figures'
out.mkdir(parents=True, exist_ok=True)
h = pd.read_csv(ROOT/'data/results/convergence_history.csv')
r = pd.read_csv(ROOT/'data/results/raw_runs.csv')
plt.rcParams.update({'font.size':11, 'figure.dpi':140})
fig, ax = plt.subplots(figsize=(8,4.5))
for _, group in h.groupby('seed'):
    ax.plot(group.generation, (group.best_feasible_objective+6).clip(lower=1e-14),
            color='#4263eb', alpha=.2, linewidth=.8)
median = h.groupby('generation').best_feasible_objective.median()+6
ax.plot(median.index, median.clip(lower=1e-14), color='#172554', label='Median (30 runs)', linewidth=2)
ax.axhline(1e-3, color='#c2410c', linestyle='--', label='Success threshold: gap <= 0.001')
ax.set(xlabel='Generation (0 = initialized population)', ylabel='Best feasible objective gap f + 6',
       yscale='log', title='GA convergence across independent seeds')
ax.legend(); ax.grid(alpha=.2);fig.tight_layout()
fig.savefig(out/'convergence.png');plt.close(fig)
fig, axes = plt.subplots(1,2,figsize=(10,4))
axes[0].bar(r.seed, r.objective+6, color='#4263eb')
axes[0].set(xlabel='Seed', ylabel='Final objective gap f + 6', title='Final solution quality')
axes[1].bar(r.seed, r.first_target_generation, color='#0f766e')
axes[1].set(xlabel='Seed', ylabel='First target generation', title='First feasible gap <= 0.001')
for ax in axes: ax.grid(axis='y',alpha=.2)
fig.tight_layout();fig.savefig(out/'run_statistics.png');plt.close(fig)
print(out)
