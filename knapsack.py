from TTP.Item import Item
import random 

def calculateRatioItem(Element: Item) -> float:
        ElementProfit = Element.get_profit()
        ElementWeight = Element.get_weight()
        ratio = ((ElementProfit)/(ElementWeight))
        return ratio

def knapsack(Objects, maxWeigth):
    #ratioDict = addItemsToDict(Objects)
    items = []
    knapsackCurrentWeigth = 0
    # Función que ordena una lista de objetos de tipo Items
    orderedItems = sorted(Objects, key=calculateRatioItem, reverse=True)    

    for i in range(len(orderedItems)):
        if (knapsackCurrentWeigth + orderedItems[i].get_weight() <= maxWeigth):
            items.append(orderedItems[i])  
            knapsackCurrentWeigth += orderedItems[i].get_weight()

        if(knapsackCurrentWeigth == maxWeigth): break
    return items
