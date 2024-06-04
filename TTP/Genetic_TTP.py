import random
import numpy as np
import math as mt
from Thief import Thief
from Item import Item
from copy import deepcopy

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

def create_population(population_size: int) -> tuple:
    """
    Esta función deberá recibir el tamaño de la población inicial
    y retornará una tupla en la cual la posición 0 corresponde a los agentes del
    problema TSP y en la posición 1 corresponde a los del knapsack.
    """
    pass

def select_parent(population: list[tuple], truncation_ratio: float) -> tuple:
    """
    Esta función recibirá una lista de tuplas que corresponderán a las
    posibles soluciones del problema, de aquí se escogerán a los 2 mejores
    padres los cuales serán discriminados en base a truncation_ratio.
    """
    pass

def crossover(parent_1: tuple, parent_2: tuple) -> tuple:
    """
    Está función recibirá a dos agentes padres y deberá generar un nuevo 
    agente hijo, a partir de aquí debe retornar una tupla donde la posición 
    0 sea la solución al problema TSP y la 1 al knapsack.
    """
    pass

def mutate(child: tuple, mutate_ratio: float) -> tuple:
    """
    Está función recibirá a un agente el cual pasará por un proceso de
    mutación, está puede llegar a ocurrir como no, esto se realizará 
    con la variable mutate_ratio.
    """
    pass

def GA(mutate_ratio: float, truncation_ratio: float, epochs: int, population_size: int):
    population = create_population(population_size)

    for gen in range(epochs):
        child_population = []

        for _ in range(population_size):
            parent_1, parent_2 = select_parent(population, truncation_ratio)
            offspring = crossover(parent_1, parent_2)
            offspring = mutate(offspring, mutate_ratio)

            child_population.append(offspring)
        
        population = child_population
        best = best_sol(population)
        print(f"Generation {gen}: Best individual = {best}, Fitness = {fitness(best)}")
    
    return best