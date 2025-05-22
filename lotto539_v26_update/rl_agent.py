"""Reinforcement Learning agent (PPO) v2.6."""

def compute_reward(roi, cold_cover, segment_cover,
                   cold_hit=False, mid_segment_hit=False, dual_guard_hit=False):
    return (roi +
            cold_cover * 0.12 +
            segment_cover * 0.25 +
            (0.3 if cold_hit else 0) +
            (0.2 if mid_segment_hit else 0) +
            (0.15 if dual_guard_hit else 0))
