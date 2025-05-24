
"""
wheel_generator.py
~~~~~~~~~~~~~~~~~~
生成 Hybrid Wheel 2.5 (High / Low risk)。
High : Guard + ≥2 Mid‑Cold + ≥1 Cold
Low  : Guard + Hot≤2 + 無 Cold

本模組僅依核心池分段結果產生 10 組範例組合；實務上可透過
GA / PSO 等演算法尋優後再餵入本邏輯過濾。
"""
from __future__ import annotations
import random, typing

def classify_numbers(core_pool: list[int],
                     hot: set[int],
                     mid_cold: set[int],
                     cold: set[int]) -> dict[str, list[int]]:
    return {
        "hot": [n for n in core_pool if n in hot],
        "mid": [n for n in core_pool if n in mid_cold],
        "cold": [n for n in core_pool if n in cold],
    }

def generate_wheels(core_pool: list[int],
                    hot: set[int],
                    mid_cold: set[int],
                    cold: set[int],
                    guards: set[int],
                    seed: int | None = None) -> tuple[list[list[int]], list[list[int]]]:
    if seed is not None:
        random.seed(seed)
    cls = classify_numbers(core_pool, hot, mid_cold, cold)
    high, low = [], []
    # ---------- High Risk ----------
    while len(high) < 6:
        g = random.choice(list(guards))
        mid = random.sample(cls["mid"], 2)
        c = random.sample(cls["cold"], 1)
        rest = [n for n in core_pool if n not in {g, *mid, *c}]
        other = random.sample(rest, 1)
        combo = sorted([g] + mid + c + other)
        if combo not in high:
            high.append(combo)
    # ---------- Low Risk ----------
    while len(low) < 4:
        g = random.choice(list(guards))
        hot_num = random.sample(cls["hot"], random.choice([1,2]))
        rest = [n for n in core_pool if n not in {g, *hot_num} and n not in cls["cold"]]
        fill = random.sample(rest, 5 - len([g] + hot_num))
        combo = sorted([g] + hot_num + fill)
        # 條件：Hot ≤ 2, 無 Cold
        if sum(1 for n in combo if n in hot) <= 2 and not any(n in cold for n in combo):
            if combo not in low:
                low.append(combo)
    return high, low
