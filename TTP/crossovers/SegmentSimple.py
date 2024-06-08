from .Crossover_Base import Crossover_Base
from numpy import ndarray
from copy import deepcopy
import random

class SegmentSimple(Crossover_Base):
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
        first_child = []
        segment = []

        segment.append(random.random())
        segment.append(random.random())
        segment.sort()

        normalized_probs = (1 / len(parent_1))
        segment_start = int(segment[0] / normalized_probs)
        segment_end = int(segment[1] / normalized_probs)

        for i in range(segment_start, segment_end):
            first_child.append(parent_1[i])

        cont = 0
        for i in parent_2:
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

    def execute(self, parent_1: tuple, parent_2: tuple, items: list, max_capacity: float) -> tuple:
        #KNAPSACK
        first_knapsack = self.execute_knapsack(deepcopy(parent_1[1]), deepcopy(parent_2[1]), items, max_capacity)

        #TRAVELING SALESMAN PROBLEM
        first_TSP= self.execute_tsp(deepcopy(parent_1[0]), deepcopy(parent_2[0]))
        first_tuple = (first_TSP, first_knapsack)

        return first_tuple