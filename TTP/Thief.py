from Backpack import Backpack

class Thief():
    def __init__(self, v_max: int, v_min: int, max_weight: int) -> None:
        self.__v_max = v_max
        self.__v_min = v_min
        self.__v_act = v_max
        self.__backpack = Backpack(max_weight)
        self.__pos = {"x": 0, "y": 0}
    
    def steal(self, new_object) -> bool:
        if(self.__backpack.add_object(new_object)):
            total_weight = self.__backpack.get_total_weight()
            max_weight = self.__backpack.get_max_weight()
            self.__v_act = self.__v_max - total_weight * ((self.__v_max - self.__v_min) / max_weight)

            return True

        return False
            