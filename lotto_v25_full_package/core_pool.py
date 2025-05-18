
import pandas as pd, numpy as np
from feature_extraction import dual_window_counts, compute_sigma_h, hit2_score
from util.constants import MID_SEGMENT, LOW_GUARD, HIGH_GUARD_PAIR

def build_core_pool(df):
    fused=dual_window_counts(df)
    rates=fused/fused.sum()
    hit2={n:hit2_score(df,n) for n in range(1,40)}
    # 加權排序：熱度 0.6 + Hit₂ 0.4
    scores={n:0.6*rates[n]+0.4*hit2[n] for n in rates.index}
    sigma_h=compute_sigma_h(rates)
    if sigma_h<0.12:
        k=17
    elif sigma_h<0.20:
        k=16
    else:
        k=15
    ranked=sorted(scores.items(), key=lambda x: x[1], reverse=True)
    core=[n for n,_ in ranked[:k]]
    # Mid 段 ≥5
    mid=[n for n in core if n in MID_SEGMENT]
    if len(mid)<5:
        mid_candidates=[n for n,_ in ranked if n in MID_SEGMENT and n not in core]
        core.extend(mid_candidates[:(5-len(mid))])
    # Guard
    latest_period=int(df['period'].iloc[-1])
    high_guard=HIGH_GUARD_PAIR[0] if latest_period%2==0 else HIGH_GUARD_PAIR[1]
    for g in (LOW_GUARD, high_guard):
        if g not in core:
            core[-1]=g  # overwrite tail
    core=sorted(set(core))
    meta={'sigma_h':sigma_h,'k':len(core),'high_guard':high_guard}
    return core, scores, meta
