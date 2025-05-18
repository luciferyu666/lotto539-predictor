
import numpy as np, random
from util.constants import MID_SEGMENT, SEGMENT_COVERAGE_BONUS

class PPOAgent:
    def __init__(self):
        self.gamma=0.99
    def reward_fn(self, combo, winning_nums):
        hit=len(set(combo)&set(winning_nums))
        mid_hit=len([n for n in combo if n in MID_SEGMENT])
        seg_bonus=SEGMENT_COVERAGE_BONUS if mid_hit>0 else 0
        return hit + seg_bonus
    def update(self, trajectories):
        # demo stub
        pass
