"""
wheel_generator.py
Hybrid Wheel 2.4 – generate wheel combinations with risk labeling.
"""

import random, itertools

def generate_wheel(core_pool, n_combos=10, size=5):
    combos=set()
    while len(combos)<n_combos:
        combo=tuple(sorted(random.sample(core_pool,size)))
        combos.add(combo)
    return list(combos)

def risk_label(combo, hot_set, threshold=3):
    return 'HighRisk' if len(hot_set.intersection(combo))>=threshold else 'LowRisk'
