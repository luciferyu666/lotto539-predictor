
# wheel_generator.py – Wheel 2.2 (Compact Pool)
import random, collections
def gen(pool, guards=(3,38), n_comb=10):
    cold=[n for n in pool if n not in guards and n not in range(21,31)]
    mid=[n for n in pool if 21<=n<=30]
    limit={n:(5 if n in guards else 4) for n in pool}
    cnt=collections.Counter()
    comb=[[] for _ in range(n_comb)]
    for i in range(n_comb):
        g=guards[i%2]; comb[i].append(g); cnt[g]+=1
        c=random.choice(cold); comb[i].append(c); cnt[c]+=1
        m=random.choice(mid); comb[i].append(m); cnt[m]+=1
        while len(comb[i])<5:
            cand=[n for n in pool if cnt[n]<limit[n] and n not in comb[i]]
            comb[i].append(random.choice(cand)); cnt[comb[i][-1]]+=1
        comb[i]=sorted(comb[i])
    return comb
