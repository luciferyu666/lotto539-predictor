
import random
from typing import List

class PPOAgent:
    """Simplified placeholder agent returning exploration/exploitation toggle."""
    def __init__(self, epsilon_max: float = 0.25):
        self.epsilon_max = epsilon_max
        self.epsilon = epsilon_max

    def should_explore(self) -> bool:
        return random.random() < self.epsilon

    def update(self, reward: float):
        # Dummy update: anneal epsilon slightly if reward positive
        if reward > 0:
            self.epsilon = max(0.05, self.epsilon * 0.95)
        else:
            self.epsilon = min(self.epsilon_max, self.epsilon * 1.05)
