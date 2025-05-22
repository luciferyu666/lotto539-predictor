"""
rl_agent.py – PPO agent with reward function v2.7
"""
import numpy as np

class PPORunner:
    def __init__(self, env, epsilon_max: float = 0.30):
        self.env = env
        self.epsilon_max = epsilon_max
        # placeholder for actual PPO implementation

def compute_reward(roi, cold_cover, segment_cover, cold_hit, mid_segment_hit, dual_guard_hit):
    reward = (
        roi
        + cold_cover * 0.12
        + segment_cover * 0.25
        + (0.3 if cold_hit else 0)
        + (0.2 if mid_segment_hit else 0)
        + (0.15 if dual_guard_hit else 0)
    )
    return reward
