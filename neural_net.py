
from typing import Dict

class SimpleHeuristicScorer:
    """Placeholder for BiGRU + Attention model.
    Combines frequency, inverse cold gap, and z-score dispersion into a scalar score."""
    def __init__(self, features: Dict):
        self.features = features
        self.max_freq = max(features['freq'].values())
        self.max_gap = max(features['cold_gap'].values())

    def score(self, num: int) -> float:
        f = self.features['freq'][num] / self.max_freq
        g = 1.0 - self.features['cold_gap'][num] / self.max_gap
        z_penalty = 1 - abs(self.features['z'][num]) / 3
        return 0.5 * f + 0.3 * g + 0.2 * z_penalty
