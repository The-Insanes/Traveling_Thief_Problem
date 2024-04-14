<<<<<<< HEAD
from .Item import Item
=======
from Item import Object
>>>>>>> Knapsack

class Backpack():
    def __init__(self, max_weight: int) -> None:
        self.__objects = []
        self.__max_weight = max_weight
        self.__total_weight = 0
        self.__total_price = 0

    def add_object(self, new_object: Item) -> bool:
        if self.__total_weight + new_object.get_weight() > self.__total_weight:
            return False
        
        self.__objects.append(new_object)
        self.__total_weight += new_object.get_weight()
        self.__total_price += new_object.get_profit()

        return True

    def show_objects(self) -> None:
        total_objects = len(self.__objects)

        for i in range(total_objects):
            print(f"Objeto {i + 1}:")
            print(f"    Peso: {self.__objects[i].get_weight()}")
            print(f"    Precio: {self.__objects[i].get_profit()}\n")
        
    def get_total_price(self) -> int:
        return self.__total_price

    def get_total_weight(self) -> int:
        return self.__total_weight

    def get_max_weight(self) -> int:
        return self.__max_weight