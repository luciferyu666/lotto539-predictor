
import statistics
from typing import List, Tuple

def hit_at_core(core_pool: List[int], winning_nums: List[int]) -> int:
    return len(set(core_pool) & set(winning_nums))

def hit2_expectation(wheels: List[Tuple[int]], history: List[List[int]]) -> float:
    """Rough Monte‑Carlo hit2 expectation."""
    hits = 0
    for draw in history:
        for combo in wheels:
            if len(set(combo) & set(draw)) >= 2:
                hits += 1
                break
    return hits / len(history) if history else 0.0
