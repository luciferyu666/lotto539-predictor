
# wheel_generator.py – Hybrid Wheel 2.1
import random, collections
def generate(core,guards=(3,38),cold_pool=None):
    if cold_pool is None: cold_pool=[]
    mid=[n for n in core if 21<=n<=30]
    limit={n:(5 if n in guards else 2) for n in core}
    cnt=collections.Counter()
    combos=[[] for _ in range(10)]
    # guards
    gs=[guards[0]]*5+[guards[1]]*5
    random.shuffle(gs)
    for i,g in enumerate(gs): combos[i].append(g); cnt[g]+=1
    # cold
    cold_cycle=(cold_pool*10)[:10]; random.shuffle(cold_cycle)
    for i,c in enumerate(cold_cycle):
        while cnt[c]>=limit[c]:
            c=random.choice(cold_pool)
        combos[i].append(c); cnt[c]+=1
    # mid
    mids=(mid*2)[:10]; random.shuffle(mids)
    for i,m in enumerate(mids):
        while cnt[m]>=limit[m]:
            m=random.choice(mid)
        combos[i].append(m); cnt[m]+=1
    # fill
    for i in range(10):
        while len(combos[i])<5:
            cand=[n for n in core if cnt[n]<limit[n] and n not in combos[i]]
            if not cand: break
            p=random.choice(cand); combos[i].append(p); cnt[p]+=1
        combos[i]=sorted(combos[i])
    return combos
