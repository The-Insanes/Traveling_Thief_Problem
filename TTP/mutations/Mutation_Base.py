from abc import abstractmethod
from abc import ABCMeta
from numpy import ndarray

class Mutation_Base(metaclass = ABCMeta):
    @abstractmethod
    def execute_knapsack(self, sol: ndarray, item_list: list, max_capacity: int) -> ndarray:
        pass

    @abstractmethod
    def execute_tsp(self, sol: ndarray) -> ndarray:
        pass

    @abstractmethod
    def execute(self, child: tuple, item_list: list, max_capacity: int) -> tuple:
        pass