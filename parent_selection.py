def fitness(sol: tuple) -> float:
    pass

def select_parent(population: list[tuple]) ->tuple:
    best_p1 = 0
    best_p2 = 0
    for sol in population:
        target = fitness(sol)
        if target >= best_p1:
            best_p2 = best_p1
            best_p1 = sol
        elif target >= best_p2:
            best_p2 = sol
    return best_p1, best_p1