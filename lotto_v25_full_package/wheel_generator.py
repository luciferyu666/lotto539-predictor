
import random, itertools
from util.constants import MID_SEGMENT, LOW_GUARD, HIGH_GUARD_PAIR

def generate_wheel(core, period, n_combos=10):
    rand=random.Random(42)
    mid=[n for n in core if n in MID_SEGMENT]
    others=[n for n in core if n not in mid and n not in (LOW_GUARD,)+HIGH_GUARD_PAIR]
    high_guard=HIGH_GUARD_PAIR[0] if period%2==0 else HIGH_GUARD_PAIR[1]
    wheel=[]
    for i in range(n_combos):
        guard=LOW_GUARD if i%2==0 else high_guard
        mid_pick=rand.choice(mid)
        others_pick=rand.sample(others,3)
        combo=set([guard,mid_pick]+others_pick)
        while len(combo)<5:
            combo.add(rand.choice(core))
        risk='high' if guard==high_guard else 'low'
        wheel.append({'numbers':sorted(combo),'risk_level':risk})
    return wheel
