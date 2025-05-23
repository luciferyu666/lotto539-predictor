"""
optimizer.py
Hybrid DE + PSO + GA optimizer for number pool selection.
"""

import random, numpy as np

def fitness(pool, score_dict, weight_hit2=2.0):
    # simplistic fitness: sum scores
    return sum(score_dict[n] for n in pool)

def pso_optimize(score_dict, k=14, iterations=100, pop_size=40):
    # toy PSO: random search as placeholder
    best=None; best_f=-1
    nums=list(score_dict.keys())
    for _ in range(iterations):
        cand=set(random.sample(nums,k))
        f=fitness(cand,score_dict)
        if f>best_f: best, best_f=cand, f
    return sorted(best)

if __name__=='__main__':
    scores={i:random.random() for i in range(1,40)}
    print(pso_optimize(scores))
