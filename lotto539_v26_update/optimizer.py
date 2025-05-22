"""Evolutionary optimizer v2.6."""

def fitness(hit2, cold_cover, diversity, mid_boost_score):
    return hit2 + cold_cover * 1.3 + diversity + 0.5 * mid_boost_score
