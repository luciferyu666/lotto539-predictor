
"""
optimizer.py
~~~~~~~~~~~~
Meta‑PSO v2（簡化示範）— 針對 Wheel 組合做粒子群優化。

* Fitness = 1.0×Hit₂ + 0.8×ExpectedPrizeProxy + 0.3×MidColdRetention
* 若 ROI 改善 < 0.1 %，則隨機重啟
"""
from __future__ import annotations
import random, math, typing, statistics
from rl_agent import DummyPPOAgent

class SimplePSOWheelOptimizer:
    def __init__(self,
                 midcold: set[int],
                 guards: set[int]):
        self.agent = DummyPPOAgent()
        self.midcold = midcold
        self.guards = guards

    # ------------------------------
    def _fitness(self, combo: list[int]) -> float:
        exp_prize = self.agent.expected_prize(combo)
        mid_ret = sum(1 for n in combo if n in self.midcold) / len(combo)
        hit2_proxy = 1.0  # placeholder，真實應用 Monte‑Carlo 或 NN 預估
        return 1.0*hit2_proxy + 0.8*(exp_prize/1e5) + 0.3*mid_ret

    # ------------------------------
    def optimize(self,
                 init_wheels: list[list[int]],
                 max_iter: int = 100) -> list[list[int]]:
        wheels = init_wheels[:]
        best = max(wheels, key=self._fitness)
        best_score = self._fitness(best)
        for _ in range(max_iter):
            # 隨機兩支交換元素
            a, b = random.sample(range(len(wheels)), 2)
            i, j = random.randrange(0,5), random.randrange(0,5)
            wheels[a][i], wheels[b][j] = wheels[b][j], wheels[a][i]
            cand = max(wheels, key=self._fitness)
            cand_score = self._fitness(cand)
            # 收斂檢查 (ROI Proxy)
            if abs(cand_score - best_score) < 0.001:
                wheels = self._random_restart(wheels)
            else:
                best, best_score = cand, cand_score
        return wheels

    def _random_restart(self, wheels: list[list[int]]) -> list[list[int]]:
        """ROI 無明顯改善時，隨機重啟。"""
        flat = [n for combo in wheels for n in combo]
        random.shuffle(flat)
        it = iter(flat)
        return = [[next(it) for _ in range(5)] for _ in range(len(wheels))]
        return return
