from matplotlib.pyplot import draw
import data_model
from haversine import haversine
from time import time

from solution import Solution


def evaluation(btns):
    cv = [item[0] for item in btns]
    sum = 0
    for i in range(len(cv)):
        a = data_model.get_coordinate_of(cv[i-1])
        b = data_model.get_coordinate_of(cv[i])
        sum += haversine((a[1], a[0]), (b[1], b[0]))
    return sum

def perform(map, specific_iteration, animate):
    v = map.verticies.copy()
    
    if len(v) == 0:
        return

    indexes = [i for i in range(len(v))]
    
    costs = []
    c = 1
    
    btns = [v[i] for i in indexes]
    draw_lines = lambda btns: map.draw_lines(btns) if animate else None
    draw_lines(btns)
    cost = evaluation(btns)
    costs.append((c, cost))

    best_state = btns
    best_cost = cost
    
    s_cost = cost if specific_iteration == c else None
    s_state = btns if specific_iteration == c else None


    while indexes := lexico_graphic(indexes):
        c += 1
        btns = [v[i] for i in indexes]
        draw_lines(btns)
        cost = evaluation(btns)
        costs.append((c, cost))
        
        if cost < best_cost:
            best_cost = cost
            best_state = btns

        if specific_iteration == c:
            s_cost = cost
            s_state = btns


    return Solution(best_state, best_cost, s_state, s_cost, c, costs)


def lexico_graphic(opt_orders):
    largest_i = -1
    largest_j = -1

    for i in range(len(opt_orders)):
        if i < len(opt_orders) - 1 and opt_orders[i] < opt_orders[i+1]:
            largest_i = i
        
        if largest_i != -1 and opt_orders[i] > opt_orders[largest_i]:
            largest_j = i

    if largest_i == -1:
        return None

    swap(opt_orders, largest_i, largest_j)
    opt_orders = opt_orders[0:largest_i+1] + list(reversed(opt_orders[largest_i+1:]))

    return opt_orders


def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

# r = ['A', 'B', 'C', 'D']
# v = [i for i in range(len(r))]
# c = 1
# print(r)
# while True:
#     v = perform(v)
#     if v == None: 
#         print(f'{c} trials')
#         break
#     print([r[i] for i in v])
#     c += 1

