"""
wheel_generator.py – Hybrid Wheel 2.3
"""
import itertools, random
from typing import List, Tuple, Sequence

def generate_wheels(core_pool: Sequence[int], high_risk:int=6, low_risk:int=4, max_repeat:int=2, rng=random.Random(42)) -> Tuple[List[Tuple[int]], List[Tuple[int]]]:
    core_set = set(core_pool)
    guard_set = {3,35,38} & core_set
    cold_set = {n for n in core_pool if n in (22,30)}  # example cold flags
    mid_set  = {n for n in core_pool if 21<=n<=30}
    # High‑risk generation
    high=[]
    attempt=0
    while len(high)<high_risk and attempt<2000:
        combo = rng.sample(core_pool, 5)
        if len(cold_set & set(combo))>=2 and len(guard_set & set(combo))>=1 and len(mid_set & set(combo))>=1:
            combo=tuple(sorted(combo))
            if combo not in high:
                high.append(combo)
        attempt+=1
    # Low‑risk generation
    low=[]
    attempt=0
    while len(low)<low_risk and attempt<2000:
        combo = rng.sample(core_pool, 5)
        if len(cold_set & set(combo))==0 and len(guard_set & set(combo))>=1:
            combo=tuple(sorted(combo))
            if combo not in low and combo not in high:
                low.append(combo)
        attempt+=1
    return high, low
