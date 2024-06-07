import random
import numpy as np
import math as mt
from .common import Thief
from .common import Item
from .crossovers import Crossover_Base
from .mutations import Mutation_Base
from .objective_function import objective_function as fitness
from copy import deepcopy

def best_sol(data: dict, population: list) -> tuple:
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
        actual_selected_items = [0] * (total_objects_amount)

        # list with random numbers ex: [2,1,4,5,3,6,7,9,8,0] that represents the order to select items randomly
        order_selection = random.sample(range(0, total_objects_amount), total_objects_amount)

        for i in range(total_objects_amount):
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

def prepare_init_pop(init_pop: tuple, population_size: int, mutation: Mutation_Base):
    population = [init_pop]

    for _ in range(population_size - 1):
        new_state = mutation.execute(init_pop, 1)
        population.append(new_state)

    return population

def GA(data: dict, mutate_ratio: float, truncation_ratio: float, epochs: int, population_size: int,
       total_cities: int, total_objects: int, mutation: Mutation_Base, crossover: Crossover_Base, 
       init_pop: tuple = None) -> tuple:
    num_units = mt.log10(epochs) // 1

    if init_pop is None: population = create_population(population_size, total_cities, total_objects, data['Thief'].get_free_weight(), data['Items'])
    else: population = prepare_init_pop(init_pop, population_size, mutation)

    for gen in range(epochs):
        child_population = []

        for _ in range(population_size):
            parent_1, parent_2 = select_parents(population, truncation_ratio, deepcopy(data))
            
            offspring = crossover.execute(parent_1, parent_2, data['Items'], data['Thief'].get_free_weight())
            offspring = mutation.execute(offspring, mutate_ratio)

            child_population.append(offspring)
        
        population = child_population
        best = best_sol(data, population)
        print(f"Generation {gen: {num_units}d}: Fitness = {round(fitness(data, best), 3)}")
    
    return best