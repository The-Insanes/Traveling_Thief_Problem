import random
import numpy as np
import math as mt
from TTP.Thief import Thief
from TTP.Item import Item
from copy import deepcopy

class Mutate:

    def random_resetting(knapsack_solution):
        i = random.randint(0, len(knapsack_solution) - 1)
        knapsack_solution[i] = random.choice([0, 1])
        return knapsack_solution

    def bit_flip(knapsack_solution):
        i = random.randint(0, len(knapsack_solution) - 1)
        knapsack_solution[i] = 1 - knapsack_solution[i]
        return knapsack_solution
    
    def scramble_mutation(tsp_solution):
        i, j = sorted(random.sample(range(len(tsp_solution)), 2))
        segmento = tsp_solution[i:j+1]
        random.shuffle(segmento)
        tsp_solution[i:j+1] = segmento
        return tsp_solution
    
    def swap_mutation(tsp_solution):
        i, j = random.sample(range(len(tsp_solution)), 2)
        tsp_solution[i], tsp_solution[j] = tsp_solution[j], tsp_solution[i]
        return tsp_solution
    
def steal_items(house: int, thief: Thief, items: list[Item], sol: list[int]) -> float:
    total = 0
    items_size = len(sol)

    for i in range(items_size):
        if not sol[i] == 0 and items[i].get_house_id() == house:
            thief.steal(items[i])
            total += items[i].get_profit() 

    return total

def fitness(data: dict, sol: tuple) -> float:
    tsp_sol, knapsack_sol = sol[0], sol[1]
    tsp_size = len(tsp_sol)
    houses, items, thief = data['Houses'], data['Items'], deepcopy(data['Thief'])
    knapsack_tarjet, TSP_tarjet = 0, 0

    for i in range(tsp_size - 1):
        house, next_house = str(tsp_sol[i]), str(tsp_sol[i + 1])
        
        knapsack_tarjet += steal_items(house, thief, items, knapsack_sol)

        pos_1 = houses[house].get_pos()
        pos_2 = houses[next_house].get_pos()

        distance = mt.sqrt((pos_1['x'] - pos_2['x']) ** 2 + (pos_1['y'] - pos_2['y']) ** 2)
        time = distance / thief.get_actual_velocity()

        TSP_tarjet += time

    knapsack_tarjet += steal_items(tsp_sol[tsp_size - 1], thief, items, knapsack_sol)

    pos_1 = houses[str(tsp_sol[tsp_size - 1])].get_pos()
    pos_2 = houses[str(tsp_sol[0])].get_pos()

    distance = mt.sqrt((pos_1['x'] - pos_2['x']) ** 2 + (pos_1['y'] - pos_2['y']) ** 2)
    time = distance / thief.get_actual_velocity()

    TSP_tarjet += time

    return knapsack_tarjet - float(data['Ratio']) * TSP_tarjet

def best_sol(data: dict, population: list) -> np.ndarray:
    population_size = len(population)
    best_tarjet = fitness(data, population[0])
    best_sol = population[0]

    for i in range(1, population_size):
        tarjet = fitness(data, population[i])

        if tarjet > best_tarjet:
            best_tarjet = tarjet
            best_sol = population[i]

    return best_sol

def create_population(population_size: int, total_cities_amount: int, total_objects_amount: int, max_weight: int, item_list: list[Item]) -> tuple:
    """
    Esta función deberá recibir el tamaño de la población inicial
    y retornará una tupla en la cual la posición 0 corresponde a los agentes del
    problema TSP y en la posición 1 corresponde a los del knapsack.
    """
    population = []

    for _ in range(population_size):
        
        ttp_actual_solution = random.sample(range(1, total_cities_amount + 1), total_cities_amount)
        
        # solution example for knapsack: [1,0,0,0,1,0,1,1,0,1] with 10 items in total
        # for each knapsack solution

        actual_weight = 0 
        # list with items selected in actual solution
        actual_selected_items = [0]*len(item_list)

        # list with random numbers ex: [2,1,4,5,3,6,7,9,8,0] that represents the order to select items randomly
        order_selection = random.sample(range(0, len(item_list)), len(item_list))

        for i in range(len(item_list)):
            # add item weight to actual weight to prove if its more than max weight or not
            if ((actual_weight + (item_list[order_selection[i]]).get_weight()) <= max_weight):
                # the object in 'item_list[order_selection[i]' is an 'Item' so we can tecnically use .getWeight()
                actual_weight += (item_list[order_selection[i]]).get_weight()
                actual_selected_items[order_selection[i]] = 1 #the item selection is_valid so we put '1'  in the actual_selected_items list
            else:
                break
        knapsack_actual_solution = actual_selected_items
        
        # we add both solutions to population and continue with next child
        population.append((ttp_actual_solution, knapsack_actual_solution)) 


    return population 
    

def select_parents(population, truncation_ratio, data):
    population_sorted = sorted(population, key=lambda ind: fitness(data, ind), reverse=True)
    truncation_index = int(truncation_ratio * len(population))
    truncated_population = population_sorted[:truncation_index]
    
    parent1 = random.choice(truncated_population)
    parent2 = random.choice(truncated_population)
    
    return parent1, parent2

def crossover_knapsack(p1: list, p2:list, items: list[Item], thief: Thief) -> list:
    #Utilizamos un cruce simple de probabilidades para ver si se intercambian los bits de los padres
    first_child_knapsack = []
    p1_size = len(p1)
    weight = 0

    for i in range(p1_size):
        probability = random.randint(1,100)
        #si la probablidad es menor a 50% se mantienen iguales
        if probability <= 50:
            first_child_knapsack.append(p1[i])
        #si la probabilidad es mayor a 50% se intercambian estos bits
        else:
            first_child_knapsack.append(p2[i])

        if first_child_knapsack[i] == 1:
            """Si el peso que se va a agregar, superaria el maximo permitido, se cambia automaticamente a 0
            para asi cumplir con la restriccion del problema de la mochila de no superar los pesos maximos"""
            if items[i].get_weight() > thief.get_free_weight():
                first_child_knapsack == 0
            else:
                weight += items[i].get_weight()

    return first_child_knapsack

def crossover_TSP(p1: list, p2: list) -> list:
    # Usamos un Cruce de Segmento Ordenado
    # Se divide los padres en 3 particiones de tamaños iguales
    first_child = []
    segment = []

    segment.append(random.random())
    segment.append(random.random())
    segment.sort()

    normalized_probs = (1 / len(p1))
    segment_start = int(segment[0] / normalized_probs)
    segment_end = int(segment[1] / normalized_probs)

    for i in range(segment_start, segment_end):
        first_child.append(p1[i])

    cont = 0
    for i in p2:
        # Se agregan en el primer segmento hasta que el largo de este se cumpla
        while cont <= segment_start:
            if i not in first_child:
                # Si no esta se agrega en la poscicion del contador el elemento i
                first_child.insert(cont, i)
            cont += 1  # Este incremento debe estar fuera del `if` para evitar el bucle infinito
        # Una vez ya se cumple el largo del primer segmento, se empiezan agregar los faltantes al final
        if i not in first_child:
            first_child.append(i)

    return first_child

def crossover(parent_1: tuple, parent_2: tuple, data) -> tuple:
    """
    Está función recibirá a dos agentes padres y deberá generar un nuevo 
    agente hijo, a partir de aquí debe retornar una tupla donde la posición 
    0 sea la solución al problema TSP y la 1 al knapsack.
    """
    #KNAPSACK
    first_knapsack = crossover_knapsack(parent_1[1], parent_2[1], data['Items'], deepcopy(data['Thief']))

    #TRAVELING SALESMAN PROBLEM
    first_TSP= crossover_TSP(parent_1[0], parent_2[0])
    first_tuple = (first_TSP, first_knapsack)
    return first_tuple

def mutate(child: tuple, mutate_ratio: float, mutateTSP, mutateKnapsack) -> tuple:
    """
    Está función recibirá a un agente el cual pasará por un proceso de
    mutación, está puede llegar a ocurrir como no, esto se realizará 
    con la variable mutate_ratio.
    """
    if random.random() < mutate_ratio:
        mutatedRoute = mutateTSP(child[0])
        mutatedObjects = mutateKnapsack(child[1]) 

        child = mutatedRoute, mutatedObjects 
    return child

def GA(data: dict, mutate_ratio: float, truncation_ratio: float, epochs: int, population_size: int,
       total_cities: int, total_objects: int, mutateTSP, mutateKnapsack):
    population = create_population(population_size, total_cities, total_objects, data['Thief'].get_free_weight(), data['Items'])

    for gen in range(epochs):
        child_population = []

        for _ in range(population_size):
            parent_1, parent_2 = select_parents(population, truncation_ratio, data)
            
            offspring = crossover(parent_1, parent_2, data)
            offspring = mutate(offspring, mutate_ratio, mutateTSP, mutateKnapsack)

            child_population.append(offspring)
        
        population = child_population
        best = best_sol(data, population)
        print(f"Generation {gen}: Fitness = {fitness(data, best)}")
    
    return best