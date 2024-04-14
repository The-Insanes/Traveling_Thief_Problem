class Item():
<<<<<<< HEAD
    def __init__(self, weight: int, profit: int) -> None:
=======
    def __init__(self, weight, profit) -> None:
>>>>>>> Knapsack
        self.__weight = weight
        self.__profit = profit

    def get_weight(self) -> int:
        return self.__weight
    
    def get_profit(self) -> int:
        return self.__profit