from .Mutation_Base import Mutation_Base
from numpy import ndarray
from copy import deepcopy
import random

class ResettingScramble(Mutation_Base):
    def execute_knapsack(self, sol: ndarray, item_list: list = None, max_capacity: int = 0) -> ndarray:
        objects_amount = len(sol)
        #i = random.randint(0, len(sol) - 1)
        indexes = random.sample(range(objects_amount), objects_amount//15)

        for index in indexes:
            
            if sol[index] == 1:
                sol[index] = 0
            else:
                item_weight = item_list[index].get_weight()
                total_weight = sum(item_list[j].get_weight() for j in range(len(sol)) if sol[j] == 1)
                if total_weight + item_weight <= max_capacity:
                    sol[index] = 1
            return sol  
    
        
    def execute_tsp(self, sol: ndarray) -> ndarray:
        i, j = sorted(random.sample(range(len(sol)), 2))
        segmento = sol[i:j+1]
        random.shuffle(segmento)
        sol[i:j+1] = segmento

        return sol

    def execute(self, child: tuple, item_list: list, max_capacity: int) -> tuple:
        mutatedRoute = self.execute_tsp(deepcopy(child[0]))
        mutatedObjects = self.execute_knapsack(deepcopy(child[1]), item_list, max_capacity)

        child = mutatedRoute, mutatedObjects 
        return child

