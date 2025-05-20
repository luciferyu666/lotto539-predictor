
"""
optimizer.py
PSO / GA / DE optimizer scaffold implementing Fitness v2.5.
"""

def fitness(combo_stats):
    return (combo_stats['hit2'] +
            combo_stats['cold_cover'] +
            combo_stats['diversity'] +
            0.5*combo_stats['mid_boost'])
