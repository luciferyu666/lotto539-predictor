import random, itertools

def generate_wheel(core, n_combos=10):
    rand=random.Random(42)
    mid=[n for n in core if 21<=n<=30]
    other=[n for n in core if n not in mid and n not in (3,35,38)]
    wheel=[]
    for i in range(n_combos):
        guard=3 if i%2==0 else 38
        mid_pick=rand.choice(mid)
        others=rand.sample(other,3)
        combo=set([guard, mid_pick] + others)
        while len(combo)<5:
            combo.add(rand.choice(core))
        wheel.append(sorted(combo))
    return wheel
