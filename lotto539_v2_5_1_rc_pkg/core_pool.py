
# core_pool.py – Adaptive‑Core 2.5.1
SHORT_WINDOW=334
LONG_WINDOW=1500
import numpy as np, collections, random
MID=range(21,31)
LOW_GUARD, HIGH_GUARD = 3, 38
MIN_CORE_SIZE=25
def _freq(draws):
    c=collections.Counter()
    for d in draws: c.update(d)
    tot=len(draws)
    return {n:c[n]/tot for n in range(1,40)}
def build_core_pool(history):
    short=history[-SHORT_WINDOW:]
    long=history[-LONG_WINDOW:]
    heat={n:(_freq(short)[n]+_freq(long)[n])/2 for n in range(1,40)}
    for n in MID: heat[n]*=1.3
    sigma=np.std(list(heat.values()))
    K=15+(2 if sigma<=0.15 else 0)+(1 if sigma<0.12 else 0)
    sorted_nums=sorted(heat,key=lambda x:heat[x],reverse=True)
    core=sorted_nums[:K]
    for g in (LOW_GUARD,HIGH_GUARD):
        if g not in core: core.append(g)
    for n in sorted(heat,key=heat.get)[:7]:
        if n not in core: core.append(n)
    while len([n for n in core if n in MID])<5:
        for n in sorted_nums:
            if n in MID and n not in core:
                core.append(n)
                if len([x for x in core if x in MID])>=5: break
    idx=K
    while len(core)<MIN_CORE_SIZE:
        if sorted_nums[idx] not in core: core.append(sorted_nums[idx])
        idx+=1
    return sorted(core)
