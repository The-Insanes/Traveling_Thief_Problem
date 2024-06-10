import random
import numpy as np
import time
import math as mt
from TTP.mutations import ResettingScramble
from TTP.crossovers import PMXSimple
from copy import deepcopy

class GA:
    def __init__(self, epochs: int, pop_size: int, pc: float, pm: float, pb: float) -> None:
        self.epochs = epochs
        self.pop_size = pop_size
        self.pc = pc
        self.pm = pm
        self.pb = pb
        self.best = None
        self.best_target = -1 * mt.inf

    def __init_parameters__(self, problem_dict: dict) -> None:
        self.data_ttp = problem_dict['data']
        self.fitness = problem_dict['obj_func']
        self.mutation = problem_dict['mut_class'] if ('mut_class' in problem_dict and problem_dict['mut_class'] is not None) else ResettingScramble() 
        self.crossover = problem_dict['cross_class'] if ('cross_class' in problem_dict and problem_dict['cross_class'] is not None) else PMXSimple()
        self.init_pop = problem_dict['init_pop'] if ('init_pop' in problem_dict and problem_dict['init_pop'] is not None) else None

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
        

        for _ in range(self.pop_size):# range of solutions we need

            # Start with all houses available for every solution
            remain_houses = deepcopy(self.data_ttp['Houses'])
            tsp_actual_solution = [] 
     

            start_house_id = '1'
            current_pos = extract_pos(remain_houses[start_house_id].get_pos())
            remain_houses.pop(start_house_id)

            while remain_houses:

                scores = []

                for house_id in remain_houses.keys():
                    house_pos = extract_pos(remain_houses[house_id].get_pos())
                    distance = calculate_distance(current_pos, house_pos)
                    ratio = remain_houses[house_id].get_ratio()
                    if distance == 0:
                        score = float('inf')  # Avoid division by zero by assigning a very high score (if the same house)
                    else:
                        score = ratio / distance  # Higher score for better value and closer distance
                    scores.append((score, house_id))
                
                # Sort houses by score in descending order (higher scores first)
                scores.sort(reverse=True, key=lambda x: x[0])

                # Calculate the top 2 (or less) houses with the best scores
                num_best = min(2, len(scores))

                # Select a random number of best houses (at most 4)
                num_selected = random.randint(1, num_best)
                # Select random indices from the top scores list
                selected_indices = random.sample(range(num_best), num_selected)
                # Extract the corresponding house IDs using the selected indices
                selected_houses = [scores[i][1] for i in selected_indices]

                # Select a random house among the selected best houses
                chosen_house_id = random.choice(selected_houses)
                
                # Calculate the top 90% of the houses with the best scores
                num_best = max(1, len(scores) // 95)
                
                # Select a random house among the best houses
                best_houses = scores[:num_best]
                chosen_score, chosen_house_id = random.choice(best_houses)
                
                tsp_actual_solution.append(int(chosen_house_id))
                current_pos = extract_pos(remain_houses[chosen_house_id].get_pos())
                remain_houses.pop(chosen_house_id)
            


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
            population.append((tsp_actual_solution, knapsack_actual_solution)) 

        return population 
    
    def select_parents(self, pop: np.ndarray):
        population_sorted = sorted(pop, key=lambda ind: self.fitness(self.data_ttp, deepcopy(ind)), reverse=True)
        truncation_index = int(self.pc * len(pop))
        truncated_population = population_sorted[:truncation_index]
        
        parent1 = random.choice(truncated_population)
        parent2 = random.choice(truncated_population)
        
        return parent1, parent2
    
    def search_best_sol(self, population: list) -> bool:
        population_size = len(population)
        self.c_best_target = self.fitness(self.data_ttp, deepcopy(population[0]))
        if self.best is None:
            self.best_target = self.c_best_target
            self.best = population[0]

        temp_target = self.best_target

        for i in range(population_size):
            target = self.fitness(self.data_ttp, deepcopy(population[i]))

            if target > self.c_best_target:
                self.c_best_target = target
            if target > self.best_target:
                self.best_target = target
                self.best = population[i]
            
        if temp_target == self.best_target: return False

        return True

    def process_individual_gen(self, pop: list):
        parent_1, parent_2 = self.select_parents(pop)

        offspring = self.crossover.execute(parent_1, parent_2, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])
        if random.random() <= self.pm:
            offspring = self.mutation.execute(offspring, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])

        return offspring
    
    def merge_pop(self, pop):
        population_sorted = sorted(pop, key=lambda ind: self.fitness(self.data_ttp, deepcopy(ind)))
        truncation_index = int(self.pb * len(pop))
  
        population_sorted[0] = self.best
        for i in range(1, truncation_index):
            new_state = self.mutation.execute(self.best, self.data_ttp['Items'], self.data_ttp['Thief']['max_capacity'])
            population_sorted[i] = new_state

        return pop

    def solve(self, problem_dict: dict, verbose: bool = True) -> None:
        try:
            init_exec_time = time.time()
            self.__init_parameters__(problem_dict)

            if self.init_pop is None and self.best is None: pop = self.create_population()
            elif self.best is not None: pop = self.prepare_init_pop(self.best)
            elif self.init_pop is not None: pop = self.prepare_init_pop(self.init_pop)

            for epoch in range(self.epochs):
                init_gen = time.time()
                child_population = []

                child_population = list(map(lambda x: self.process_individual_gen(pop), range(self.pop_size)))
            
                pop = child_population
                if not self.search_best_sol(pop): pop = self.merge_pop(pop)

                end_gen = time.time()
                gen_time = end_gen - init_gen

                if verbose: 
                    print(f"Epoch {epoch + 1}: Global best: {round(self.best_target, 3)} | Current best: {round(self.c_best_target, 3)} | Execution_time: {round(gen_time, 3)}[s]")

        except KeyboardInterrupt as e:
            print('Ejecución Interrumpida')
            
        exit_exec_time = time.time()
        total_time = exit_exec_time - init_exec_time

        print(f'Global best: {round(self.best_target, 3)}  |  Current best: {round(self.c_best_target, 3)}  |  Execution_time: {int(total_time) // 60}:{int(total_time) % 60}')

        return self.best