
"""
rl_agent.py
~~~~~~~~~~~
極簡 PPO 代理，用於選號策略增強。

> 實作重點：以 log(ExpectedPrize+1) 當作 reward，並對 mid_cold_retention
  與 dual_guard_hit 施加懲罰/獎勵。

本版本僅示範接口，方便後續替換為真實 RL 模型。
"""
from __future__ import annotations
import math, random, typing, collections

class DummyPPOAgent:
    def __init__(self,
                 midcold_weight: float = 0.3,
                 guard_weight: float = 0.2):
        self.midcold_weight = midcold_weight
        self.guard_weight = guard_weight

    # ------------------------------
    @staticmethod
    def expected_prize(combo: list[int]) -> float:
        """以 Hit₂~Hit₅ 的期望獎金粗估，示意用。"""
        # 假設命中 2 顆獎金 400、3 顆 1e4、4 顆 30 萬、5 顆 800 萬
        # 機率採 539 標準 C(39,5) 組合計算
        total_combo = math.comb(39,5)
        prob_hit2 = (math.comb(5,2)*math.comb(34,3)) / total_combo
        prob_hit3 = (math.comb(5,3)*math.comb(34,2)) / total_combo
        prob_hit4 = (math.comb(5,4)*math.comb(34,1)) / total_combo
        prob_hit5 = (math.comb(5,5)*math.comb(34,0)) / total_combo
        exp = prob_hit2*400 + prob_hit3*1e4 + prob_hit4*3e5 + prob_hit5*8e6
        return exp

    # ------------------------------
    def evaluate(self,
                 combo: list[int],
                 midcold_set: set[int],
                 guards: set[int]) -> float:
        prize = self.expected_prize(combo)
        reward = math.log(prize + 1.0)

        # mid‑cold retention
        mid_ratio = sum(1 for n in combo if n in midcold_set) / len(combo)
        reward += self.midcold_weight * mid_ratio

        # dual_guard_hit（至少 1 Guard）
        if any(n in guards for n in combo):
            reward += self.guard_weight
        else:
            reward -= self.guard_weight
        return reward

    # ------------------------------
    def choose(self,
               candidate_wheels: list[list[int]],
               midcold_set: set[int],
               guards: set[int],
               top_n: int = 10) -> list[list[int]]:
        scored = [(self.evaluate(c, midcold_set, guards), c) for c in candidate_wheels]
        scored.sort(reverse=True)
        return [c for _, c in scored[:top_n]]
