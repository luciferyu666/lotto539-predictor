
from typing import List, Tuple, Set

def build_wheels(elites: List[Tuple[int]], guard_low: int, guard_high: int) -> List[Tuple[int]]:
    """Ensure each combo contains dual guard numbers and uniqueness."""
    wheels = []
    seen = set()
    for combo in elites:
        combo_set = set(combo)
        combo_set.update([guard_low, guard_high])
        if len(combo_set) > 5:
            # trim extra numbers preserving guards
            others = sorted(combo_set - {guard_low, guard_high})
            combo = tuple(sorted([guard_low, guard_high] + others[:3]))
        else:
            combo = tuple(sorted(combo_set))
        if combo not in seen:
            wheels.append(combo)
            seen.add(combo)
        if len(wheels) == 10:
            break
    return wheels
