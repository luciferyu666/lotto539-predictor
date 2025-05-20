
# core_pool.py – Adaptive-Core 2.5.2 (Compact 10–16)
import numpy as np, collections
SHORT=334; LONG=1500
MID=range(21,31)
LOW_G, HIGH_G = 3, 38
MIN_SZ, MAX_SZ = 10, 16
def _freq(ds):
    c=collections.Counter(); [c.update(d) for d in ds]; tot=len(ds)
    return {n:c[n]/tot for n in range(1,40)}
def build(history):
    heat={}; short, long = history[-SHORT:], history[-LONG:]
    sf, lf = _freq(short), _freq(long)
    for n in range(1,40):
        v=(sf[n]+lf[n])/2; heat[n]=v*1.3 if n in MID else v
    # 初步取 Top‑Heat
    sorted_nums=sorted(heat,key=heat.get,reverse=True)
    pool=set(sorted_nums[:8])
    # ensure guards
    pool.update({LOW_G, HIGH_G})
    # ensure ≥5 mids
    for n in sorted_nums:
        if len([x for x in pool if x in MID])>=5: break
        if n in MID: pool.add(n)
    # cold extremes (3)
    for n in sorted(heat,key=heat.get)[:3]: pool.add(n)
    # 截斷至 MAX_SZ
    pool=sorted(pool, key=lambda x:heat[x], reverse=True)[:MAX_SZ]
    # 若小於 MIN_SZ，用熱度補足
    for n in sorted_nums:
        if len(pool)>=MIN_SZ: break
        if n not in pool: pool.append(n)
    return sorted(pool)
