import random
import numpy as np
import math as mt
from Thief import Thief
from Item import Item
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
        house, next_house = tsp_sol[i], tsp_sol[i + 1]
        
        knapsack_tarjet += steal_items(house, thief, items, knapsack_sol)

        pos_1 = houses[house].get_pos()
        pos_2 = houses[next_house].get_pos()

        distance = mt.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
        time = distance / thief.get_actual_velocity()

        TSP_tarjet += time

    knapsack_tarjet += steal_items(tsp_sol[tsp_size - 1], thief, items, knapsack_sol)

    pos_1 = houses[tsp_size - 1].get_pos()
    pos_2 = houses[0].get_pos()

    distance = mt.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)
    time = distance / thief.get_actual_velocity()

    TSP_tarjet += time

    return knapsack_tarjet - data['Tasa'] * TSP_tarjet

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

def create_population(population_size: int = 4, total_cities_amount: int = 3, total_objects_amount: int = 7) -> tuple:
    """
    Esta función deberá recibir el tamaño de la población inicial
    y retornará una tupla en la cual la posición 0 corresponde a los agentes del
    problema TSP y en la posición 1 corresponde a los del knapsack.
    """
    population = []

    for _ in range(population_size):
        
        ttp_actual_solution = random.sample(range(1, total_cities_amount + 1), total_cities_amount)
        knapsack_actual_solution = [random.choice([0, 1]) for _ in range(total_objects_amount)]
        population.append((ttp_actual_solution, knapsack_actual_solution))


    return population 
    

def select_parent(population: list[tuple], truncation_ratio: float) -> tuple:
    """
    Esta función recibirá una lista de tuplas que corresponderán a las
    posibles soluciones del problema, de aquí se escogerán a los 2 mejores
    padres los cuales serán discriminados en base a truncation_ratio.
    """
    best_p1 = 0
    best_p2 = 0

    for sol in population:
        target = fitness(sol)

        if target >= best_p1:
            best_p2 = best_p1
            best_p1 = sol

        elif target >= best_p2:
            best_p2 = sol
    return best_p1, best_p1

import random

def crossover_knapsack(p1: list, p2:list) ->list:
    #Utilizamos un cruce simple de probabilidades para ver si se intercambian los bits de los padres
        first_child_knapsack = []
        for i in len(p1):
            probability = random.randint(1,100)
            #si la probablidad es menor a 50% se mantienen iguales
            if probability <= 50:
                first_child_knapsack.append(p1[i])
            #si la probabilidad es mayor a 50% se intercambian estos bits
            else:
                first_child_knapsack.append(p2[i])
        return first_child_knapsack

def crossover_TSP(p1:list, p2:list) ->list:
     #Usamos un Cruce de Segmento Ordenado
        #Se divide los padres en 3 particiones de tamaños iguales
        #partition_length = len(p1)/3
        first_child = []
        segment = []

        segment.append(random.random())
        segment.append(random.random())
        segment.sort()

        normalized_probs = (1 / len(p1))
        segment_start = (segment[0]/normalized_probs)
        segment_end = (segment[1]/normalized_probs)

        for i in range(segment_start, segment_end, 1):
            first_child.append(p1[i])

        cont = 0
        for i in p2:
            #Se agregan en el primer segmento hasta que el largo de este se cumpla
            while cont <= segment_start:
                if i not in first_child:
                    #Si no esta se agrega en la poscicion del contador el elemento i
                    first_child.insert(cont, i)
                    cont += 1
            #una vez ya se cumple el largo del primer segmento, se empiezan agregar los faltantes al final
            if i not in first_child:
                first_child.append(i)

        return first_child

def crossover(parent_1: tuple, parent_2: tuple) -> tuple:
    """
    Está función recibirá a dos agentes padres y deberá generar un nuevo 
    agente hijo, a partir de aquí debe retornar una tupla donde la posición 
    0 sea la solución al problema TSP y la 1 al knapsack.
    """
    #KNAPSACK
    first_knapsack = crossover_knapsack(parent_1[1], parent_2[1])

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
    if random.random(0, 1) < mutate_ratio:
        mutatedRoute = mutateTSP(child[0])
        mutatedObjects = mutateKnapsack(child[1]) 

        child = mutatedRoute, mutatedObjects 
    return child

def GA(data: dict, mutate_ratio: float, truncation_ratio: float, epochs: int, population_size: int,
       total_cities: int, total_objects: int, mutateTSP, mutateKnapsack):
    population = create_population(population_size, total_cities, total_objects)

    for gen in range(epochs):
        child_population = []

        for _ in range(population_size):
            parent_1, parent_2 = select_parent(population, truncation_ratio)
            offspring = crossover(parent_1, parent_2)
            offspring = mutate(offspring, mutate_ratio, mutateTSP, mutateKnapsack)

            child_population.append(offspring)
        
        population = child_population
        best = best_sol(data, population)
        print(f"Generation {gen}: Best individual = {best}, Fitness = {fitness(best)}")
    
    return best

