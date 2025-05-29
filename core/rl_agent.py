import numpy as np
class PPOAgent:
    def __init__(self,scores): self.p=scores/scores.sum()
    def sample(self,n=25): return np.random.choice(39,n,replace=False,p=self.p).tolist()
