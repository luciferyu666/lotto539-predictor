
"""
core_pool.py – Elastic‑K Adaptive‑Core 2.7 + Entropy‑Balance
"""
import numpy as np
from collections import Counter
from typing import List, Tuple

class AdaptiveCore:
    def __init__(self, hot_threshold:float=0.30):
        self.hot_threshold = hot_threshold  # max ratio of hot numbers in core

    @staticmethod
    def sigma_to_k(sigma_h: float) -> int:
        if sigma_h >= 0.18:
            return 16
        elif sigma_h >= 0.05:
            return 14
        else:
            return 12

    def entropy_balance(self, core: List[int], hot_flags: List[bool]) -> List[int]:
        # hot_flags aligned to all 39 numbers, True if number in top‑5 hot list
        core_hot_idx = [idx for idx, n in enumerate(core) if hot_flags[n-1]]
        while len(core_hot_idx) / len(core) > self.hot_threshold:
            # remove one hottest (last)
            drop_idx = core_hot_idx.pop()
            del core[drop_idx]
        return core

    def build_core(self,
                   candidate_scores: List[float],
                   hot_flags: List[bool],
                   guard_numbers=(3,35,38)) -> Tuple[List[int], float, int]:
        ranked = np.argsort(candidate_scores)[::-1]  # indices 0‑38
        sigma_h = np.std(candidate_scores)
        k = self.sigma_to_k(sigma_h)
        core = list(ranked[:k] + 1)  # convert idx→ball (1‑39)

        core = self.entropy_balance(core, hot_flags)

        # Guard injection，確保至少 1 個 Guard
        for g in guard_numbers:
            if g not in core:
                if len(core) < k:
                    core.append(g)
                else:
                    core[-1] = g
        return sorted(core), sigma_h, len(core)
