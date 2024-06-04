import random

#se entrega 0 al crossover si es de knapsack problem
#se entrega 1 al crossover si es TSP 
def crossover(p1: list ,p2: list, tpye_of_problem: int) -> list:   
    if tpye_of_problem == 0:
        #KNAPSACK
        #Utilizamos un cruce simple de probabilidades para ver si se intercambian los bits de los padres
        first_child = []
        second_child = []
        for i in len(p1):
            probability = random.randint(1,100)
            #si la probablidad es menor a 50% se mantienen iguales
            if probability <= 50:
                first_child.append(p1[i])
                second_child.append(p2[i])
            #si la probabilidad es mayor a 50% se intercambian estos bits
            else:
                first_child.append(p2[i])
                second_child.append(p1[i])
                
        return first_child, second_child
    if (tpye_of_problem == 1):
        #TRAVELING SALESMAN PROBLEM
        #Usamos un Cruce de Segmento Ordenado
        #Se divide los padres en 3 particiones de tamaños iguales
        partition_length = len(p1)/3
        first_child = []
        second_child= []
        #Se entrega un numero al azar entre 0 y 2 para ver cual segmento es el que se mantiene de los padres
        segment = random.randint(0,2)
        segment_start = segment * partition_length
        segment_end = ((segment + 1) * partition_length) + len(p1)%3
        for i in range(segment_start, segment_end, 1):
            first_child.append(p1[i])
            second_child.append(p2[i])
        
        #Se mantiene el orden relativo del padre 2 al agregar a la solucion hijo 1
        #Si el segmetno que se mantiene es el primero, se van agregando al final
        if segment == 0:
            for i in p2:
                if i not in first_child:
                    first_child.append(i)
            for j in p1:
                if j not in second_child:
                    second_child.append(j)
            #Se retornan ambos hijos creados
            
        
        # Si el segmento que se mantiene es el segundo, se agrega la mitad al primero y despues al final
        if segment == 1:
            cont = 0
            for i in p2:
                #Se agregan en el primer segmento hasta que el largo de este se cumpla
                while cont <= partition_length:
                    if i not in first_child:
                        #Si no esta se agrega en la poscicion del contador el elemento i
                        first_child.insert(cont, i)
                        cont += 1
                #una vez ya se cumple el largo del primer segmento, se empiezan agregar los faltantes al final
                if i not in first_child:
                    first_child.append(i)
            for j in p1:
                #Se agregan en el primer segmento hasta que el largo de este se cumpla
                while cont <= partition_length:
                    if j not in second_child:
                        #Si no esta se agrega en la poscicion del contador el elemento j
                        second_child.insert(cont, j)
                        cont += 1
                #una vez ya se cumple el largo del primer segmento, se empiezan agregar los faltantes al final
                if j not in second_child:
                    second_child.append(j)
        
        if segment == 2:
            contI = 0
            for i in p2:
                if i not in first_child:
                    first_child.insert(contI, i)
                    contI +=1
            contJ = 0
            for j in p1:
                if j not in second_child:
                    second_child.insert(contJ, j)
                    contJ += 1
             
        return first_child, second_child
    return 