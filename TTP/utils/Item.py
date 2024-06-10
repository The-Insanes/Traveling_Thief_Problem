class Item():
    def __init__(self, weight: int, profit: int, house: int) -> None:
        self.__weight = int(weight)
        self.__profit = int(profit)
        self.__house = int(house)

    def get_house_id(self):
        return self.__house

    def get_weight(self) -> int:
        return self.__weight
    
    def get_profit(self) -> int:
        return self.__profit