
"""
rl_agent.py
Proximal Policy Optimization (PPO) agent skeleton with custom reward.
Reward = ROI + cold_cover*0.12 + segment_cover*0.25 + (0.2 if mid_segment_hit else 0)
Real environment and training loop omitted.
"""

class PPOAgent:
    def __init__(self, reward_fn=None):
        self.reward_fn = reward_fn
