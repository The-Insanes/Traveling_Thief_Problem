from read_file import read_file
from TTP import GA
from TTP.crossovers import SegmentSimple
from TTP.mutations import ResettingScramble



name, thief , cities , items, ratio = read_file("./data/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp")

data = {'Houses': cities,
        'Items': items,
        'Thief': thief,
        'Ratio': ratio}

print(GA(data, mutate_ratio= 0.5, truncation_ratio= 0.2, epochs= 50, 
    population_size= 200, total_cities= len(cities), 
    total_objects= len(items), mutation= ResettingScramble(), crossover= SegmentSimple()))