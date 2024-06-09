import random
import numpy as np
import time
import math as mt
from TTP.mutations import ResettingScramble
from TTP.crossovers import SegmentSimple

class GA:
    def __init__(self, epochs: int, pop_size: int, pc: float, pm: float, pb: float) -> None:
        self.epochs = epochs
        self.pop_size = pop_size
        self.pc = pc
        self.pm = pm
        self.pb = pb
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
        total_cities_amount = len(self.data_ttp['Houses'])
        total_objects_amount = len(self.data_ttp['Items'])
        item_list = self.data_ttp['Items']
        max_weight = self.data_ttp['Thief']['max_capacity']
        population = []

        for _ in range(self.pop_size):
            
            ttp_actual_solution = random.sample(range(2, total_cities_amount + 1), total_cities_amount - 1)
            
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
    
    def select_parents(self, pop: np.ndarray):
        population_sorted = sorted(pop, key=lambda ind: self.fitness(self.data_ttp, ind), reverse=True)
        truncation_index = int(self.pc * len(pop))
        truncated_population = population_sorted[:truncation_index]
        
        parent1 = random.choice(truncated_population)
        parent2 = random.choice(truncated_population)
        
        return parent1, parent2
    
    def best_sol(self, population: list) -> bool:
        population_size = len(population)
        if self.best is None:
            self.best_tarjet = self.fitness(self.data_ttp, population[0])
            self.best = population[0]
        temp_tarjet = self.best_tarjet

        for i in range(population_size):
            tarjet = self.fitness(self.data_ttp, population[i])

            if tarjet > self.best_tarjet:
                self.best_tarjet = tarjet
                self.best = population[i]
            
        if temp_tarjet == self.best_tarjet: return False

        return True

    def process_individual_gen(self, pop: list):
        parent_1, parent_2 = self.select_parents(pop)

        offspring = self.crossover.execute(parent_1, parent_2, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])
        if random.random() <= self.pm:
            offspring = self.mutation.execute(offspring, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])

        return offspring
    
    def merge_pop(self, pop):
        population_sorted = sorted(pop, key=lambda ind: self.fitness(self.data_ttp, ind))
        truncation_index = int(self.pb * len(pop))
  
        population_sorted[0] = self.best
        for i in range(1, truncation_index):
            new_state = self.mutation.execute(self.best, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])
            population_sorted[i] = new_state

        return pop

    def solve(self, problem_dict: dict, verbose: bool = True) -> None:
        try:
            exec_time = 0
            self.__init_parameters__(problem_dict)

            if self.init_pop is None and self.best is None: pop = self.create_population()
            elif self.best is not None: pop = self.prepare_init_pop(self.best)
            elif self.init_pop is not None: pop = self.prepare_init_pop(self.init_pop)

            for gen in range(self.epochs):
                init_gen = time.time()
                child_population = []

                child_population = list(map(lambda x: self.process_individual_gen(pop), range(self.pop_size)))
            
                pop = child_population
                if not self.best_sol(pop): pop = self.merge_pop(pop)

                end_gen = time.time()
                gen_time = end_gen - init_gen
                exec_time += gen_time

                if verbose: 
                    print(f"Generation {gen}:")
                    print(f"   Fitness: {round(self.best_tarjet, 3)} Execution_time: {round(gen_time, 3)}")
        except KeyboardInterrupt as e:
            print(f'best sol: {round(self.best_tarjet, 3)}')
            
        return self.best