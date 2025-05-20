
"""
wheel_generator.py
Hybrid Wheel Builder 2.0
 * Guarantees ≥1 cold, ≥1 mid, ≥1 guard per combo
 * MaxRepeat soft‑constraint (default 2)
"""

import random
from collections import Counter

def generate_wheels(core_pool, cold_numbers, guards, n_combos=10, max_repeat=2):
    mids = [n for n in core_pool if 21<=n<=30]
    others = [n for n in core_pool if n not in cold_numbers+guards+mids]

    counts = Counter()
    wheels = []
    for _ in range(n_combos):
        combo = set()
        combo.add(random.choice(guards))
        combo.add(random.choice(cold_numbers))
        combo.add(random.choice(mids))
        while len(combo)<5:
            candidate = random.choice(core_pool)
            if counts[candidate] < max_repeat or len(combo)>=4:  # allow overflow late
                combo.add(candidate)
        for n in combo:
            counts[n]+=1
        wheels.append(sorted(combo))
    return wheels
