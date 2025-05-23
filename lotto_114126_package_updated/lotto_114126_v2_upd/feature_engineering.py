"""
feature_engineering.py
Implements Dual‑Window 2.1, ColdBoost 3.0, Entropy‑Balance 2.0
"""

import numpy as np, pandas as pd
from collections import Counter

def dual_window_features(draws, short=110, long=334):
    """Return frequency ratios in two windows."""
    short_window=draws[-short:]
    long_window=draws[-long:]
    cnt_short=Counter()
    cnt_long=Counter()
    for d in short_window: cnt_short.update(d['nums'])
    for d in long_window: cnt_long.update(d['nums'])
    ratio={}
    for n in range(1,40):
        ratio[n]=cnt_short.get(n,0)/(cnt_long.get(n,1))
    return ratio

def cold_boost(freqs, threshold=0.85):
    """Amplify cold numbers (below threshold×mean)."""
    mean=np.mean(list(freqs.values()))
    return {n: (v*1.2 if v<mean*threshold else v) for n,v in freqs.items()}

def entropy_balance(pool):
    """
    Compute normalized entropy of pool distribution across 1‑39 range.
    σ_h <0.02 triggers K‑lock.
    """
    import math
    hist=[0]*39
    for n in pool: hist[n-1]+=1
    p=[h/sum(hist) for h in hist if h]
    entropy=-sum(pi*math.log(pi) for pi in p)
    max_entropy=math.log(len(hist))
    sigma_h=abs(entropy/max_entropy-1)
    return sigma_h
