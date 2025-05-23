
"""
optimizer.py – Hybrid DE → PSO → GA pipeline (v2.7 demo)
The implementation is intentionally lightweight and dependency‑free;
replace sections with calls to DEAP / PyGAD in production.
"""
import random, math
from typing import Callable, List, Tuple

Ball = int
Combo = Tuple[Ball, Ball, Ball, Ball, Ball]

class EvolutionOptimizer:
    def __init__(self,
                 population_size:int = 300,
                 generations:int = 500,
                 rng: random.Random = random.Random(42)):
        self.pop_size = population_size
        self.generations = generations
        self.rng = rng

    # ---------- basic helpers ----------
    def random_combo(self) -> Combo:
        return tuple(sorted(self.rng.sample(range(1,40), 5)))

    def mutate(self, combo: Combo, rate:float=0.2) -> Combo:
        combo = list(combo)
        if self.rng.random() < rate:
            idx = self.rng.randrange(5)
            new_val = self.rng.randrange(1,40)
            while new_val in combo:
                new_val = self.rng.randrange(1,40)
            combo[idx] = new_val
        return tuple(sorted(combo))

    # ---------- main ----------
    def run(self, fitness_fn: Callable[[Combo], float]) -> Combo:
        # init population
        pop = [self.random_combo() for _ in range(self.pop_size)]
        # eval
        scores = [fitness_fn(c) for c in pop]
        for gen in range(self.generations):
            # DE phase (前 300 代)
            if gen < 300:
                trial_pop=[]
                for i in range(self.pop_size):
                    a,b,c = self.rng.sample(pop,3)
                    mutant = tuple(sorted(set(a) ^ set(b) ^ set(c)))[:5] or self.random_combo()
                    trial = mutant if fitness_fn(mutant) > scores[i] else pop[i]
                    trial_pop.append(trial)
                pop = trial_pop
            # PSO phase (後 200 代簡化為 global elite push)
            else:
                best_idx = scores.index(max(scores))
                gbest = pop[best_idx]
                pop = [self.mutate(gbest, rate=0.3) if self.rng.random()<0.5 else self.random_combo()
                       for _ in range(self.pop_size)]
            # GA crossover every 50 代
            if gen % 50 == 0:
                for i in range(0, self.pop_size, 2):
                    if self.rng.random() < 0.2:
                        a,b = pop[i], pop[i+1]
                        cut = self.rng.randint(1,4)
                        child1 = a[:cut] + tuple(x for x in b if x not in a[:cut])
                        child2 = b[:cut] + tuple(x for x in a if x not in b[:cut])
                        pop[i], pop[i+1] = child1[:5], child2[:5]
            scores = [fitness_fn(c) for c in pop]
        best_idx = scores.index(max(scores))
        return pop[best_idx]
