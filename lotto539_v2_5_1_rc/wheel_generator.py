
"""
wheel_generator.py  –  Hybrid Wheel Builder 2.1‑RC
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
* 嚴格遵守:
  - 每組 ≥1 Guard(3/38)、≥1 Cold、≥1 Mid
  - 非 Guard 號碼 MaxRepeat ≤ 2
  - Guard 3 與 38 預設各使用 5 次 (10 組排輪)
"""
import random
from collections import Counter

def generate_wheels(core_pool, guard_nums=(3,38), cold_nums=None, n_combos=10):
    if cold_nums is None:
        raise ValueError("cold_nums must be provided (≥5 建議)")
    mid_nums=[n for n in core_pool if 21<=n<=30]
    # 計數器
    limit={n:(5 if n in guard_nums else 2) for n in core_pool}
    counts=Counter()
    combos=[[] for _ in range(n_combos)]
    # -- guard配置 --
    guards_seq=list(guard_nums[0] for _ in range(n_combos//2))+list(guard_nums[1] for _ in range(n_combos-n_combos//2))
    random.shuffle(guards_seq)
    for i,g in enumerate(guards_seq):
        combos[i].append(g); counts[g]+=1
    # -- cold配置 --
    cold_pool=list(cold_nums)
    while len(cold_pool)<n_combos:
        cold_pool+=cold_nums
    random.shuffle(cold_pool)
    for i in range(n_combos):
        c=cold_pool[i]
        while counts[c]>=limit[c]:
            c=random.choice(cold_nums)
        combos[i].append(c); counts[c]+=1
    # -- mid配置 --
    mid_pool=mid_nums*2
    random.shuffle(mid_pool)
    for i in range(n_combos):
        m=mid_pool.pop()
        while counts[m]>=limit[m]:
            m=random.choice(mid_nums)
        combos[i].append(m); counts[m]+=1
    # -- 填滿至 5 碼 --
    other=[n for n in core_pool if n not in guard_nums]
    for i in range(n_combos):
        while len(combos[i])<5:
            cand=[n for n in other if counts[n]<limit[n] and n not in combos[i]]
            if not cand:
                break
            pick=random.choice(cand)
            combos[i].append(pick); counts[pick]+=1
        combos[i]=sorted(combos[i])
    # 最終驗證
    for combo in combos:
        assert any(n in guard_nums for n in combo)
        assert any(n in cold_nums for n in combo)
        assert any(21<=n<=30 for n in combo)
    return combos
