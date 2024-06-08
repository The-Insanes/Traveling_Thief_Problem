import math
from .common import House, Thief, Item
import time 

def calcular_distancia(houseX: House,houseY: House) -> int:
    dist = math.sqrt((houseX.get_pos()["x"]-houseY.get_pos()["x"])**2 + (houseX.get_pos()["y"]-houseY.get_pos()["y"])**2) 

    return dist


def create_distance_matrix(city: dict) -> list:
    matrix = []

    for indexX in range(1, len(city)+1, 1):
        houseX = city[str(indexX)]
        houseX_distances = []

        for indexY in range(1,len(city)+1,1):
            houseY = city[str(indexY)]
            distanciaXY = calcular_distancia(houseX,houseY)
            houseX_distances.append(distanciaXY)

        matrix.append(houseX_distances)

    return matrix 



def no_se_repite(lista):
    """
    Comprueba si no se repiten números dentro de una lista.
    Retorna True si no hay números repetidos, False de lo contrario.
    """
    numeros_vistos = set()  # Creamos un conjunto para almacenar los números ya vistos
    
    for numero in lista:
        if numero in numeros_vistos:
            return False  # Si encontramos un número que ya hemos visto, retornamos False
        numeros_vistos.add(numero)  # Agregamos el número al conjunto de números vistos
    
    return True

def calculateRatioItem(Element: Item) -> float:
        ElementProfit = Element.get_profit()
        ElementWeight = Element.get_weight()
        ratio = ((ElementProfit)/(ElementWeight))
        return ratio

def knapsack(Objects, maxWeigth):
    #ratioDict = addItemsToDict(Objects)
    items = []
    knapsackCurrentWeigth = 0
    # Función que ordena una lista de objetos de tipo Items
    orderedItems = sorted(Objects, key=calculateRatioItem, reverse=True)    

    for i in range(len(orderedItems)):
        if (knapsackCurrentWeigth + orderedItems[i].get_weight() <= maxWeigth):
            items.append(orderedItems[i])  
            knapsackCurrentWeigth += orderedItems[i].get_weight()

        if(knapsackCurrentWeigth == maxWeigth): break
    return items
    
def greedy_ttp(thief: Thief, city: dict) -> tuple:
    init = time.time()
    distance_matrix = create_distance_matrix(city)
    total_time = 0 
    route = [city["1"].get_index()]
    act_house = city["1"]

    while(len(route) < len(city)):
        best_next_distance = math.inf
        best_next_house = None

        for i in range(1,len(city)+1 , 1):
            if distance_matrix[act_house.get_index()-1][i-1] < best_next_distance and i != act_house.get_index():
                if city[str(i)].get_index() not in route:
                    best_next_distance = distance_matrix[act_house.get_index()-1][i-1]
                    best_next_house = city[str(i)]

        total_time += best_next_distance / float(thief.get_actual_velocity())
        act_house = best_next_house

        #AQUI SE DEBE APLICAR EL ROBO 
        remaining_houses = len(city)- len(route)
        weight_rate = int(thief.get_free_weight()) / remaining_houses
        object_list = knapsack(act_house.get_objects(), weight_rate)

        for obj in object_list:
            thief.steal(obj)
            
        route.append((act_house.get_index()))

    final_house = city[str(route[-1])]
    init_house = city['1']

    distance = calcular_distancia(final_house, init_house)

    total_time += distance / thief.get_actual_velocity()
    
    end = time.time()
    finalTime = end - init

    return route, thief.get_items(), total_time , thief.get_price(), finalTime