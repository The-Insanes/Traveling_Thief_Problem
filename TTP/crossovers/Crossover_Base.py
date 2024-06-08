from abc import abstractmethod
from abc import ABCMeta
from numpy import ndarray

class Crossover_Base(metaclass = ABCMeta):
    @abstractmethod
    def execute_knapsack(self, parent_1: ndarray, parent_2: ndarray, item_list: list, max_capacity: float) -> ndarray:
        pass

    @abstractmethod
    def execute_tsp(self, parent_1: ndarray, parent_2: ndarray) -> ndarray:
        pass

    @abstractmethod
    def execute(self, parent_1: tuple, parent_2: tuple, items: list, max_capacity: float) -> tuple:
        pass