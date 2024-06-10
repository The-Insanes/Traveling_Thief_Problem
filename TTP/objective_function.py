from TTP.utils import Thief, Item
from copy import deepcopy
import math as mt

def steal_items(house: int, thief: Thief, items: list[Item], sol: list[int]) -> float:
    total = 0
    items_size = len(sol)

    for i in range(items_size):
        if sol[i] == 1 and items[i].get_house_id() == house:
            thief.steal(items[i])
            total += items[i].get_profit()
    
    return total

def objective_function(data: dict, sol: tuple, verbose: bool = False) -> float:
    tsp_sol, knapsack_sol = sol[0], sol[1]
    if not 1 in tsp_sol: tsp_sol.insert(0, 1)
    tsp_size = len(tsp_sol)
    houses, items = data['Houses'], data['Items']
    thief = Thief(data['Thief']['v_max'], data['Thief']['v_min'], data['Thief']['max_capacity'])
    TSP_tarjet = 0.0
    
    for i in range(tsp_size - 1):
        house, next_house = str(tsp_sol[i]), str(tsp_sol[i + 1])
        
        steal_items(int(house), thief, items, knapsack_sol)

        pos_1 = houses[house].get_pos()
        pos_2 = houses[next_house].get_pos()

        distance = mt.sqrt((pos_1['x'] - pos_2['x']) ** 2 + (pos_1['y'] - pos_2['y']) ** 2)
        time = distance / float(thief.get_actual_velocity())

        TSP_tarjet += time

    steal_items(tsp_sol[tsp_size - 1], thief, items, knapsack_sol)

    pos_1 = houses[str(tsp_sol[tsp_size - 1])].get_pos()
    pos_2 = houses[str(tsp_sol[0])].get_pos()

    distance = mt.sqrt((pos_1['x'] - pos_2['x']) ** 2 + (pos_1['y'] - pos_2['y']) ** 2)
    time = distance / float(thief.get_actual_velocity())

    TSP_tarjet += time

    if verbose:
        print(f'Valor obtenido: ${thief.get_price()}')
        print(f'Tiempo de recorrido: {round(TSP_tarjet, 3)}')
    return thief.get_price() - float(data['Ratio']) * TSP_tarjet