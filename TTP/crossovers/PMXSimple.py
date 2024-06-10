from .Crossover_Base import Crossover_Base
from numpy import ndarray
from copy import deepcopy
import random

class PMXSimple(Crossover_Base):
    def execute_knapsack(self, parent_1: ndarray, parent_2: ndarray, item_list: list, max_capacity: float) -> ndarray:
        first_child_knapsack = []
        p1_size = len(parent_1)
        weight = 0

        for i in range(p1_size):
            probability = random.randint(1,100)
            #si la probablidad es menor a 50% se mantienen iguales
            if probability <= 50:
                first_child_knapsack.append(parent_1[i])
            #si la probabilidad es mayor a 50% se intercambian estos bits
            else:
                first_child_knapsack.append(parent_2[i])

            if first_child_knapsack[i] == 1:
                """Si el peso que se va a agregar, superaria el maximo permitido, se cambia automaticamente a 0
                para asi cumplir con la restriccion del problema de la mochila de no superar los pesos maximos"""
                if item_list[i].get_weight() > max_capacity:
                    first_child_knapsack == 0
                else:
                    weight += item_list[i].get_weight()

        return first_child_knapsack

    def execute_tsp(self, parent_1: ndarray, parent_2: ndarray) -> ndarray:
        first_child = ['-1']*(len(parent_1))
        second_child = ['-1']*(len(parent_1))
        segment = []

        segment.append(random.randint(0,(len(parent_1))-1))
        segment.append(random.randint(0,(len(parent_1)-1)))
        segment.sort()

        for i in range(segment[0], segment[1]):
            first_child[i] = parent_2[i]
            second_child[i] = parent_1[i]

        for i in range(len(parent_1)):
            if i not in range(segment[0], segment[1]):
                gene = parent_1[i]

                while gene in first_child:
                    ind = first_child.index(gene)
                    gene = second_child[ind]
                first_child[i] = gene

                gene2 = parent_2[i]
                while gene2 in second_child:
                    ind = second_child.index(gene2)
                    gene2 = first_child[ind]
                second_child[i] = gene2
        return first_child

    def execute(self, parent_1: tuple, parent_2: tuple, items: list, max_capacity: float) -> tuple:
        #KNAPSACK
        first_knapsack = self.execute_knapsack(deepcopy(parent_1[1]), deepcopy(parent_2[1]), items, max_capacity)

        #TRAVELING SALESMAN PROBLEM
        first_TSP= self.execute_tsp(deepcopy(parent_1[0]), deepcopy(parent_2[0]))
        first_tuple = (first_TSP, first_knapsack)

        return first_tuple