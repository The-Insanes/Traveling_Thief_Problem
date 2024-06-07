from .Mutation_Base import Mutation_Base
from numpy import ndarray
import random

class FlipScramble(Mutation_Base):
    def execute_knapsack(self, sol: ndarray, item_list: list = None, max_capacity: int = 0) -> ndarray:
        i = random.randint(0, len(sol) - 1)
        sol[i] = 1 - sol[i]

        return sol
    
    def execute_tsp(self, sol: ndarray) -> ndarray:
        i, j = sorted(random.sample(range(len(sol)), 2))
        segmento = sol[i:j+1]
        random.shuffle(segmento)
        sol[i:j+1] = segmento

        return sol

    def execute(self, child: tuple, mutate_ratio: float) -> tuple:
        if random.random() < mutate_ratio:
            mutatedRoute = self.execute_tsp(child[0])
            mutatedObjects = self.execute_knapsack(child[1])

            child = mutatedRoute, mutatedObjects 
        return child