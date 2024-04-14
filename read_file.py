from TTP.Thief import Thief
from TTP.House import House
from TTP.Item import Item
import os
import re

def read_file(file_name: str) -> tuple:
    file = open(file_name, mode = 'r', encoding= 'utf-8')

    info = {}
    pattern = re.compile(r'(\w+.*?):\s*(.+)')
    
    for line in file:
        match = pattern.match(line)
        if match:
            key = match.group(1).strip()
            if key == 'NODE_COORD_SECTION	(INDEX, X, Y)': break

            value = match.group(2).strip()
            info[key] = value

    name = info['DIMENSION'] + '_' + info['NUMBER OF ITEMS'] + 'CAPACITY OF KNAPSACK'
    thief = Thief(info['MAX SPEED'], info['MIN SPEED'], info['CAPACITY OF KNAPSACK'])
    houses = dict()

    digit_pattern = re.compile(r'\d+')
    for line in file:
        if not digit_pattern.search(line): break
        
        line = line.split('\t')
        houses[line[0]] = House(int(line[1]), int(line[2]), int(line[0]))

    for line in file:
        
        line = line.split('\t')
        houses[str(int(line[3]))].add_object(Item(int(line[2]), int(line[1])))

    return name, thief, houses, info['RENTING RATIO']

def read_all_files(direct) -> None:
    elements = os.listdir(direct)

    folders_1 = [element for element in elements if os.path.isdir(os.path.join(direct, element))]

    cases = {}

    for folder_1 in folders_1:
        files = os.listdir(direct + '/' + folder_1)

        total_files = len(files)
        cont = 0
        for file in files:
            print(f"{round(cont / total_files, 3)}%")
            name, thief, houses, ratio = read_file(direct + '/' + folder_1 + '/' + file)
            cases[name] = {
                            "thief": thief,
                            "houses": houses,
                            "ratio": ratio
                            }
            cont += 1

    return cases
