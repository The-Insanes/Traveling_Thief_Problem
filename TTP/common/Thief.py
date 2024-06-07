from .Backpack import Backpack
from .Item import Item

class Thief():
    def __init__(self, v_max: float, v_min: float, max_weight: int) -> None:
        self.__v_max = v_max
        self.__v_min = v_min
        self.__v_act = v_max
        self.__backpack = Backpack(max_weight)
        self.__pos = {'x': 0, 'y': 0}
    
    def steal(self, new_object: Item) -> bool:
        if(self.__backpack.add_object(new_object)):
            total_weight = self.__backpack.get_total_weight()
            max_weight = self.__backpack.get_max_weight()
            self.__v_act = self.__v_max - total_weight * ((self.__v_max - self.__v_min) / max_weight)
            
            return True

        return False
    
    def get_items(self):
        return self.__backpack.get_objects()
    
    def get_free_weight(self) -> int:
        return self.__backpack.get_max_weight() - self.__backpack.get_total_weight()

    def get_price(self) -> int:
        return self.__backpack.get_total_price()

    def move(self, x: int, y: int) -> None:
        self.__pos['x'] = x
        self.__pos['y'] = y

    def get_pos(self) -> dict:
        return self.__pos
    
    def get_actual_velocity(self) -> float:
        return self.__v_act 