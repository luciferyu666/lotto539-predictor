
"""
core_pool.py
Implements Adaptive‑Core 2.5 logic:
 * Dual‑Window heat modeling (334 & 1500 draws)
 * MidBoost ×1.3
 * Dynamic‑K tiered buffer based on σ_h
 * Dual‑Extreme Guard injection (#03 low, #35/#38 high)
 * Cold‑Boost & Entropy‑Balance placeholder
"""

import numpy as np
from collections import Counter

SHORT_WINDOW = 334
LONG_WINDOW = 1500
MID_SEGMENT = range(21, 31)
LOW_GUARD = 3
HIGH_GUARDS = {35, 38}

def build_core_pool(draw_history, period, high_guard=38):
    """
    Parameters
    ----------
    draw_history : list of list[int]
        Full historical draws ordered ascending by period
    period : int
        Current target period (for parity guard rotation)
    high_guard : int
        Selected high segment guard (35 or 38)
    Returns
    -------
    list[int] : adaptive core number pool
    """
    # last N draws
    recent_short = draw_history[-SHORT_WINDOW:]
    recent_long = draw_history[-LONG_WINDOW:]

    def freq(window):
        cnt = Counter()
        for draw in window:
            cnt.update(draw)
        total = len(window)
        return {n:cnt[n]/total for n in range(1,40)}

    short_f = freq(recent_short)
    long_f = freq(recent_long)

    heat = {n:(short_f[n]+long_f[n])/2 for n in range(1,40)}
    # MidBoost
    for n in MID_SEGMENT:
        heat[n] *= 1.3

    sigma_h = np.std(list(heat.values()))
    # Dynamic‑K tiered
    K = 15
    if sigma_h <= 0.15:
        K += 2
    if sigma_h < 0.12:
        K += 1

    # select by heat
    sorted_nums = sorted(range(1,40), key=lambda x:heat[x], reverse=True)
    core = sorted_nums[:K]

    # Ensure guards
    if LOW_GUARD not in core:
        core[-1] = LOW_GUARD
    if high_guard not in core:
        core[-2] = high_guard

    # Ensure ≥5 mids
    mids = [n for n in core if n in MID_SEGMENT]
    if len(mids)<5:
        candidates = [n for n in sorted_nums if n in MID_SEGMENT and n not in core]
        core = core[:-len(candidates[:5-len(mids)])] + candidates[:5-len(mids)]

    return sorted(core)
