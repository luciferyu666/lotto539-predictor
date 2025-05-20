
"""
core_pool.py  –  Adaptive‑Core 2.5.1‑RC
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
* 支援 MaxRepeat≤2 約束 → 若要產生 10 組 × 5 碼排輪，共 50 格；
  則當核心池 <25 碼時動態擴容至 25 (或以上)。
"""
import numpy as np
from collections import Counter

SHORT_WINDOW=334
LONG_WINDOW=1500
MID_SEGMENT=range(21,31)
LOW_GUARD=3
HIGH_GUARDS={38}
MIN_CORE_FOR_WHEEL=25  # 確保 MaxRepeat≤2

def _freq(draws):
    cnt=Counter()
    for d in draws: cnt.update(d)
    total=len(draws)
    return {n:cnt[n]/total for n in range(1,40)}

def build_core_pool(history, period):
    short=history[-SHORT_WINDOW:]
    long=history[-LONG_WINDOW:]
    heat={n:( _freq(short)[n]+_freq(long)[n])/2 for n in range(1,40)}
    for n in MID_SEGMENT: heat[n]*=1.3
    sigma=np.std(list(heat.values()))
    K=15+ (2 if sigma<=0.15 else 0)+ (1 if sigma<0.12 else 0)
    sorted_nums=sorted(heat, key=lambda x:heat[x], reverse=True)
    core=list(dict.fromkeys(sorted_nums[:K]))  # preserve order
    # guards
    for g in (LOW_GUARD,38):
        if g not in core: core.append(g)
    # cold extremes – 7 最低熱度
    cold_candidates=sorted(heat,key=lambda x:heat[x])[:7]
    for c in cold_candidates:
        if c not in core: core.append(c)
    # 強制 Mid ≥5
    mids=[n for n in core if n in MID_SEGMENT]
    if len(mids)<5:
        for n in sorted_nums:
            if n in MID_SEGMENT and n not in core:
                core.append(n)
                if len([x for x in core if x in MID_SEGMENT])>=5: break
    # 擴容保證 MaxRepeat≤2
    i=0
    while len(core)<MIN_CORE_FOR_WHEEL:
        n=sorted_nums[K+i]
        if n not in core:
            core.append(n)
        i+=1
    return core
