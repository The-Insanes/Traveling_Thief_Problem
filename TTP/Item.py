class Item():
    def __init__(self, weight, profit) -> None:
        self.__weight = weight
        self.__profit = profit

    def get_weight(self) -> int:
        return self.__weight
    
    def get_profit(self) -> int:
        return self.__profit