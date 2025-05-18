from feature_extraction import compute_features
import numpy as np, pandas as pd

def build_core_pool(df):
    rates, sigma_h = compute_features(df)
    if sigma_h < 0.12:
        k=17
    elif sigma_h < 0.20:
        k=16
    else:
        k=15
    ranked=sorted(rates.items(), key=lambda x: x[1], reverse=True)
    core=[n for n,_ in ranked[:k]]
    mid=[n for n in core if 21<=n<=30]
    if len(mid)<5:
        mid_candidates=[n for n,_ in ranked if 21<=n<=30 and n not in core]
        core.extend(mid_candidates[:(5-len(mid))])
    # guards
    low_guard=3
    # rotate high guard by latest period parity
    latest_period=int(df['period'].iloc[-1])
    high_guard=38 if latest_period %2==1 else 35
    for g in (low_guard, high_guard):
        if g not in core:
            core[-1]=g  # overwrite tail to keep size
    core=sorted(set(core))
    meta={'sigma_h':sigma_h,'k':len(core)}
    return core, meta
