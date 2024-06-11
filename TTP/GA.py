import random
import numpy as np
import time
import math as mt
from copy import deepcopy
from TTP.mutations import ResettingScramble
from TTP.crossovers import SegmentSimple

class GA:
    def __init__(self, epochs: int, pop_size: int, pc: float, pm: float) -> None:
        self.epochs = epochs
        self.pop_size = pop_size
        self.pc = pc
        self.pm = pm
        self.best = None
        self.best_tarjet = -1 * mt.inf

    def __init_parameters__(self, problem_dict: dict) -> None:
        self.data_ttp = problem_dict['data']
        self.fitness = problem_dict['obj_func']
        self.mutation = problem_dict['mut_class'] if (problem_dict['mut_class'] is not None) else ResettingScramble() 
        self.crossover = problem_dict['cross_class'] if (problem_dict['cross_class'] is not None) else SegmentSimple()
        self.init_pop = problem_dict['init_pop'] if (problem_dict['init_pop'] is not None) else None

    def prepare_init_pop(self, pop) -> list:
        population = [pop]

        for _ in range(self.pop_size - 1):
            new_state = self.mutation.execute(pop, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])
            population.append(new_state)

        return population

    def create_population(self) -> np.ndarray:
        def extract_pos(house):
            return house['x'], house['y']

        def calculate_distance(pos1: tuple, pos2: tuple) -> float:
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

        total_objects_amount = len(self.data_ttp['Items'])
        item_list = self.data_ttp['Items']
        max_weight = self.data_ttp['Thief']['max_capacity']
        population = []

        for _ in range(self.pop_size):  # range of solutions we need
            # Start with all houses available for every solution
            remain_houses = deepcopy(self.data_ttp['Houses'])
            tsp_actual_solution = []

            start_house_id = '1'
            current_pos = extract_pos(remain_houses[start_house_id].get_pos())
            remain_houses.pop(start_house_id)

            while remain_houses:
                distances = []

                for house_id, house in remain_houses.items():
                    house_pos = extract_pos(house.get_pos())
                    distance = calculate_distance(current_pos, house_pos)
                    distances.append((distance, house_id))

                # Sort houses by distance in ascending order (closer first)
                distances.sort(key=lambda x: x[0])

                # Select up to 4 (or less) closest houses
                num_closest = min(2, len(distances))
                selected_houses = [house_id for _, house_id in distances[:num_closest]]

                # Select a random house among the selected closest houses
                chosen_house_id = random.choice(selected_houses)

                tsp_actual_solution.append(int(chosen_house_id))
                current_pos = extract_pos(remain_houses[chosen_house_id].get_pos())
                remain_houses.pop(chosen_house_id)
            print(tsp_actual_solution)

            # Generate knapsack solution based on tsp_actual_solution
            actual_weight = 0
            actual_selected_items = [0] * total_objects_amount
            order_selection = random.sample(range(total_objects_amount), total_objects_amount)

            for i in tsp_actual_solution:
                for j in range(total_objects_amount):
                    if ((actual_weight + item_list[j].get_weight()) <= max_weight):
                        actual_weight += item_list[j].get_weight()
                        actual_selected_items[j] = 1

            population.append((tsp_actual_solution, actual_selected_items))

        return population

    
    def select_parents(self, pop: np.ndarray):
        population_sorted = sorted(pop, key=lambda ind: self.fitness(self.data_ttp, ind), reverse=True)
        truncation_index = int(self.pc * len(pop))
        truncated_population = population_sorted[:truncation_index]
        
        parent1 = random.choice(truncated_population)
        parent2 = random.choice(truncated_population)
        
        return parent1, parent2
    
    def best_sol(self, population: list) -> None:
        population_size = len(population)
        if self.best is None:
            self.best_tarjet = self.fitness(self.data_ttp, population[0])
            self.best = population[0]
        temp_tarjet = self.best_tarjet

        for i in range(1, population_size):
            tarjet = self.fitness(self.data_ttp, population[i])

            if tarjet > self.best_tarjet:
                self.best_tarjet = tarjet
                self.best = population[i]
            
        if temp_tarjet == self.best_tarjet: population[0] = self.best

    def solve(self, problem_dict: dict, verbose: bool = True) -> None:
        exec_time = 0
        self.__init_parameters__(problem_dict)

        if self.init_pop is None and self.best is None: 
            pop = self.create_population() 

        elif self.best is not None: pop = self.prepare_init_pop(self.best)
        elif self.init_pop is not None: pop = self.prepare_init_pop(self.init_pop)

        for gen in range(self.epochs):
            init_gen = time.time()
            child_population = []

            for _ in range(self.pop_size):
                parent_1, parent_2 = self.select_parents(pop)

                offspring = self.crossover.execute(parent_1, parent_2, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])
                if random.random() <= self.pm:
                    offspring = self.mutation.execute(offspring, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])

                child_population.append(offspring)
        
            pop = child_population
            self.best_sol(pop)

            end_gen = time.time()
            gen_time = end_gen - init_gen
            exec_time += gen_time

            if verbose: 
                print(f"Generation {gen}:")
                print(f"   Fitness: {round(self.best_tarjet, 3)} Execution_time: {round(gen_time, 3)}")
        
        return self.best