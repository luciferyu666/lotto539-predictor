"""
core_pool.py – Elastic‑K Adaptive‑Core 2.7 implementation
"""
import numpy as np
from collections import Counter
from typing import List

class AdaptiveCore:
    def __init__(self, base_k:int=14):
        self.base_k = base_k

    def sigma_to_k(self, sigma_h: float) -> int:
        if sigma_h >= 0.18:
            return 16
        elif sigma_h >= 0.05:
            return 14
        else:
            return 12

    def build_core(self, candidate_scores: List[float], cold_flags: List[bool], guard_numbers=(3,35,38)):
        ranked = np.argsort(candidate_scores)[::-1]  # high to low
        sigma_h = np.std(candidate_scores)
        k = self.sigma_to_k(sigma_h)
        core = list(ranked[:k])

        # Guard injection
        for g in guard_numbers:
            if g not in core:
                core[-1] = g  # replace last to enforce guard

        return sorted(core), sigma_h, k
