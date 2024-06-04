import random
import numpy as np

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
    pass

def crossover(parent_1: tuple, parent_2: tuple) -> tuple:
    """
    Está función recibirá a dos agentes padres y deberá generar un nuevo 
    agente hijo, a partir de aquí debe retornar una tupla donde la posición 
    0 sea la solución al problema TSP y la 1 al knapsack.
    """
    pass

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