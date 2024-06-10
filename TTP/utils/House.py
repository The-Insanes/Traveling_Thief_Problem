from TTP.utils import Item

class House():
    def __init__(self, x: int, y: int, index: int) -> None:
        self.__objects = []
        self.__total_value = 0
        self.__total_weight = 0
        self.__ratio = 0
        self.__pos = {"x": x, "y": y}
        self.__index = index

    def add_object(self, new_object: Item) -> None:
        self.__objects.append(new_object)
        self.__total_value += new_object.get_profit()
        self.__total_weight += new_object.get_weight()
        self.__ratio = self.__total_value / self.__total_weight

    def delete_object(self, del_object: Item):
        self.__objects.remove(del_object)

    def get_index(self) -> int:
        return self.__index

    def get_ratio(self) -> float:
        return self.__ratio

    def get_objects(self) -> list:
        return self.__objects

    def get_pos(self) -> None:
        return self.__pos
    
    def get_weight(self) -> float:
        return self.__total_weight

    def get_value(self) -> float:
        return self.__total_value
