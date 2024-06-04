import random
import numpy as np

def fitness(sol: tuple) -> float:
    pass

def best_sol(population: list) -> np.ndarray:
    pass

def create_population(population_size: int = 4, total_cities_amount: int = 3, total_objects_amount: int = 7) -> tuple:
    """
    Esta función deberá recibir el tamaño de la población inicial
    y retornará una tupla en la cual la posición 0 corresponde a los agentes del
    problema TSP y en la posición 1 corresponde a los del knapsack.
    """

    ttp_solutions = []
    knapsack_solutions = []

    for _ in range(population_size):
        
        ttp_actual_solution = random.sample(range(1, total_cities_amount + 1), total_cities_amount)
        knapsack_actual_solution = [random.choice([0, 1]) for _ in range(total_objects_amount)]
        #print(ttp_solution)
        #print(knapsack_solution)
        ttp_solutions.append(ttp_actual_solution)
        knapsack_solutions.append(knapsack_actual_solution)


    return ttp_solutions, knapsack_solutions
    

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




print(create_population())