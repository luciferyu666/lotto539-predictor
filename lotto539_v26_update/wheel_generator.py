"""Wheel generator v2.6."""

MAX_REPEAT = 2
GUARD_NUMBERS = {3, 35, 38}

def validate_combo(combo, cold_set):
    return any(n in cold_set for n in combo) and any(21 <= n <= 30 for n in combo) and any(n in GUARD_NUMBERS for n in combo)
