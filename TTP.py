import math
from TTP import House
from TTP import Thief
from read_file import read_file
from knapsack import knapsack

#def setHouseValues(city: list) ->list:
#    for house in city:
#        house.price = 0
#        house.weigth = 0
#        for objeto in house.objects:
#           house.price += objeto.price
#            house.weigth += objeto.weigth
#        house.value = house.price / house.weigth

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


def TSP(thief: Thief, city: dict) -> list:
    distance_matrix = create_distance_matrix(city)
    print("si")
    total_time = 0 
    route = []
    act_house = city["1"]
    while(len(route) < len(city)):
        best_next_distance = math.inf
        best_next_house = None
        for i in range(1,len(city)+1 , 1):
            if distance_matrix[act_house.get_index()-1][i-1] < best_next_distance and i != act_house.get_index():
                if city[str(i)].get_index() not in route:
                    best_next_distance = distance_matrix[act_house.get_index()-1][i-1]
                    best_next_house = city[str(i)]
        total_time += best_next_distance/float(thief.get_actual_velocity())
        act_house = best_next_house
        #AQUI SE DEBE APLICAR EL ROBO 
        remaining_houses = len(city)- len(route)
        weight_rate = int(thief.get_free_weight())/remaining_houses
        object_list = knapsack(act_house.get_objects() , weight_rate)
        for obj in object_list:
            thief.steal(obj)
            
        route.append((act_house.get_index()))
    return route, total_time , thief.get_price()


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

name , thief , city , ratio = read_file("c:/Users/Taipan/Desktop/instances/usa13509/usa13509_n13508_bounded-strongly-corr_02.ttp")
print(TSP(thief, city))