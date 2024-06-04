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

def crossover(p1: tuple ,p2: tuple) -> tuple:   
        #KNAPSACK
        first_knapsack = crossover_knapsack(p1[1],p2[1])
 
        #TRAVELING SALESMAN PROBLEM
        first_TSP= crossover_TSP(p1[0],p2[0])
        first_tuple = (first_TSP, first_knapsack)
        return first_tuple

