from .Mutation_Base import Mutation_Base
from numpy import ndarray
from copy import deepcopy
import random

class FlipSwamp(Mutation_Base):
    def execute_knapsack(self, sol: ndarray, item_list: list = None, max_capacity: int = 0) -> ndarray:
        i = random.randint(0, len(sol) - 1)
        sol[i] = 1 - sol[i]

        return sol
    
    def execute_tsp(self, sol: ndarray) -> ndarray:
        i, j = random.sample(range(len(sol)), 2)
        sol[i], sol[j] = sol[j], sol[i]

        return sol

    def execute(self, child: tuple, item_list: list, max_capacity: int) -> tuple:
        mutatedRoute = self.execute_tsp(deepcopy(child[0]))
        mutatedObjects = self.execute_knapsack(deepcopy(child[1]), item_list, max_capacity)

        child = mutatedRoute, mutatedObjects 
        return child