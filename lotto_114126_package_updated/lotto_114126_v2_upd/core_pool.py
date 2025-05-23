"""
core_pool.py
Implements Elastic‑K pool construction with σ_h check.
"""

from feature_engineering import entropy_balance
import random

def build_core_pool(candidates, scores, k_default=14):
    pool=set()
    # rank candidates by score descending
    ranked=sorted(candidates, key=lambda n: scores[n], reverse=True)
    pool.update(ranked[:k_default])
    sigma_h=entropy_balance(pool)
    return sorted(pool), sigma_h
