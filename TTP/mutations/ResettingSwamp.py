from .Mutation_Base import Mutation_Base
from numpy import ndarray
import random

class ResettingSwamp(Mutation_Base):
    def execute_knapsack(self, sol: ndarray, item_list: list = None, max_capacity: int = 0) -> ndarray:
        i = random.randint(0, len(sol) - 1)
        sol[i] = random.choice([0, 1])

        return sol
    
    def execute_tsp(self, sol: ndarray) -> ndarray:
        i, j = random.sample(range(len(sol)), 2)
        sol[i], sol[j] = sol[j], sol[i]

        return sol

    def execute(self, child: tuple, mutate_ratio: float) -> tuple:
        if random.random() < mutate_ratio:
            mutatedRoute = self.execute_tsp(child[0])
            mutatedObjects = self.execute_knapsack(child[1])

            child = mutatedRoute, mutatedObjects 
        return child