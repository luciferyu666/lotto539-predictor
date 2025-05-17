
import random, itertools, math
from typing import List, Tuple, Set

def fitness(combo: Tuple[int], hot_set: Set[int], cold_set: Set[int]) -> float:
    """Simple fitness emphasising presence of hot and cold guards + diversity."""
    score = 0.0
    if hot_set & set(combo):
        score += 1.0
    if cold_set & set(combo):
        score += 1.0
    # uniqueness bonus
    score += len(set(combo)) / 5.0
    return score

def pso_ga_search(core_pool: List[int], hot: List[int], cold: List[int],
                  n_particles: int = 200, generations: int = 35) -> List[Tuple[int]]:
    """Return elite combinations after simplified search."""
    hot_set, cold_set = set(hot), set(cold)
    population = [tuple(sorted(random.sample(core_pool, 5))) for _ in range(n_particles)]

    for _ in range(generations):
        # evaluate
        ranked = sorted(population, key=lambda c: fitness(c, hot_set, cold_set), reverse=True)
        elites = ranked[:20]
        # crossover + mutation
        new_pop = elites.copy()
        while len(new_pop) < n_particles:
            a, b = random.sample(elites, 2)
            cut = random.randint(1, 4)
            child = tuple(sorted(list(a)[:cut] + list(b)[cut:]))
            # mutation: swap
            if random.random() < 0.1:
                idx = random.randint(0, 4)
                new_num = random.choice(core_pool)
                child = list(child)
                child[idx] = new_num
                child = tuple(sorted(child))
            new_pop.append(child)
        population = new_pop
    return ranked[:10]
