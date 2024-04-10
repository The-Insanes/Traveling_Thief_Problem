from Object import Object

class House():
    def __init__(self) -> None:
        self.__objects = []
        self.__total_value = 0
        self.__pos = {"x": 0, "y": 0}

    def add_object(self, new_object: Object) -> None:
        self.__objects.append(new_object)
        self.__total_value += new_object.get_profit()
    
    def delete_object(self, del_object: Object):
        self.__objects.remove(del_object)

    def get_objects(self) -> list:
        return self.__objects

    def get_pos(self) -> None:
        return self.__pos

    

    