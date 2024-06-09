from .Crossover_Base import Crossover_Base
from numpy import ndarray
from copy import deepcopy
import random

class ImprovedCrossover(Crossover_Base):
    def execute_knapsack(self, parent_1: ndarray, parent_2: ndarray, item_list: list, max_capacity: float) -> ndarray:
        child_knapsack = [0] * len(parent_1)
        weight = 0

        # Combine the items from both parents and sort by value-to-weight ratio
        items = [(i, item_list[i].get_profit() / item_list[i].get_weight()) for i in range(len(item_list))]
        items.sort(key=lambda x: x[1], reverse=True)

        for i, _ in items:
            if parent_1[i] == 1 or parent_2[i] == 1:
                item_weight = item_list[i].get_weight()
                if weight + item_weight <= max_capacity:
                    child_knapsack[i] = 1
                    weight += item_weight

        return child_knapsack

    def execute_tsp(self, parent_1: ndarray, parent_2: ndarray) -> ndarray:
        size = len(parent_1)
        child = [-1] * size

        start, end = sorted(random.sample(range(size), 2))
        child[start:end] = parent_1[start:end]

        fill_position = end
        parent_2_index = 0

        while -1 in child:
            if parent_2_index >= size:
                parent_2_index = 0

            if parent_2[parent_2_index] not in child:
                if fill_position >= size:
                    fill_position = 0
                child[fill_position] = parent_2[parent_2_index]
                fill_position += 1

            parent_2_index += 1

        return child

    def execute(self, parent_1: tuple, parent_2: tuple, items: list, max_capacity: float) -> tuple:
        # KNAPSACK
        child_knapsack = self.execute_knapsack(deepcopy(parent_1[1]), deepcopy(parent_2[1]), items, max_capacity)

        # TRAVELING SALESMAN PROBLEM
        child_tsp = self.execute_tsp(deepcopy(parent_1[0]), deepcopy(parent_2[0]))

        return (child_tsp, child_knapsack)