
import numpy as np
from typing import List, Dict

def extract_features(draws: List[Dict], window: int = 334) -> Dict:
    """Return dict of per-number stats: frequency, cold_gap, z-score."""
    recent = draws[-window:]
    freq = {i: 0 for i in range(1, 40)}
    for rec in recent:
        for n in rec['nums']:
            freq[n] += 1

    # cold gap based on full history
    cold_gap = {}
    for num in range(1, 40):
        gap = 0
        for rec in reversed(draws):
            gap += 1
            if num in rec['nums']:
                cold_gap[num] = gap - 1
                break
        else:
            cold_gap[num] = len(draws)

    freq_values = np.array(list(freq.values()))
    z = (freq_values - freq_values.mean()) / (freq_values.std(ddof=0) + 1e-9)
    z_scores = {i + 1: z[i] for i in range(39)}

    return {'freq': freq, 'cold_gap': cold_gap, 'z': z_scores}
