
import random, numpy as np
from util.constants import MID_SEGMENT

def fitness_v25(candidate, scores_dict):
    base=sum(scores_dict[n] for n in candidate)
    mid_boost=len([n for n in candidate if n in MID_SEGMENT])*0.1
    return base + mid_boost

def pso_ga(core_pool, scores):
    # Minimal hybrid optimiser, returns top 10 combos by random sampling + fitness
    candidates=[]
    for _ in range(500):
        combo=random.sample(core_pool,5)
        candidates.append((combo, fitness_v25(combo,scores)))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [sorted(x[0]) for x in candidates[:10]]
