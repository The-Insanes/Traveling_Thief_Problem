import math
from read_file import read_file
from knapsack import knapsack
from TTP.Genetic_TTP import GA, Mutate
import time 


name, thief , cities , items, ratio = read_file("./data/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp")

data = {'Houses': cities,
        'Items': items,
        'Thief': thief,
        'Ratio': ratio}

print(GA(data, mutate_ratio= 0.2, truncation_ratio= 0.8, epochs= 10, 
    population_size= 100, total_cities= len(cities), 
    total_objects= len(items), mutateKnapsack= Mutate.bit_flip, 
    mutateTSP= Mutate.scramble_mutation))