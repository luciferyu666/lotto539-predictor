"""Adaptive-Core logic v2.6."""

COLD_BOOST_FACTOR = 1.15
ENTROPY_TOP5_CAP = 0.30
K_BASE = 15

def determine_k(sigma_h):
    if sigma_h < 0.12:
        return 18
    elif sigma_h <= 0.15:
        return 17
    return K_BASE
