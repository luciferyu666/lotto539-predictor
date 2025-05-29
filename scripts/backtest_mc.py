
import numpy as np, math, itertools

def monte_carlo_eval(core_pool: list[int], wheels: list[list[int]], samples: int = 500_000):
    core_set = set(core_pool)
    draws = np.array([np.random.choice(39, 5, replace=False) for _ in range(samples)])
    # Matches with core pool
    matches_core = np.vectorize(lambda arr: len(core_set.intersection(arr)))(draws)
    hit_core = np.mean(matches_core >= 1)
    hit2 = np.mean(matches_core >= 2)
    hit3_plus = np.mean(matches_core >= 3)
    # Very簡化ROI: 假設中 2 個號回收 25，3+ 回收 250
    roi = hit2*25 + hit3_plus*250 - 50  # 投注成本 50
    return {'Hit@Core': float(hit_core),
            'Hit2': float(hit2),
            'Hit3+': float(hit3_plus),
            'ROI': float(roi)}
