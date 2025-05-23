"""
rl_agent.py
PPO implementation via Stable‑Baselines3 for action‑space = {select number}.
"""

import gym, numpy as np
from stable_baselines3 import PPO
from gym import spaces

class LottoEnv(gym.Env):
    """
    Observation: feature vector length 39
    Action: Discrete(39) pick number
    Reward: custom via dual_guard_hit etc.
    """
    def __init__(self, features, core_pool_size=14):
        super().__init__()
        self.features=np.array([features[n] for n in range(1,40)], dtype=np.float32)
        self.action_space=spaces.MultiBinary(39)  # choose 0/1 per number
        self.observation_space=spaces.Box(low=0, high=1, shape=(39,), dtype=np.float32)
        self.core_pool_size=core_pool_size
        self.reset()

    def reset(self):
        self.selected=np.zeros(39, dtype=np.int8)
        return self.features

    def step(self, action):
        # action is binary vector
        self.selected=action
        done=True
        k=self.selected.sum()
        reward=-abs(k-self.core_pool_size)  # placeholder reward
        return self.features, reward, done, {}

def train_agent(features, timesteps=1000):
    env=LottoEnv(features)
    model=PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=timesteps)
    return model

