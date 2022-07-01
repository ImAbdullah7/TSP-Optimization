import random
import data_model
from map import Map
from haversine import haversine
from solution import Solution
from copy import deepcopy
import numpy as np

def perform(map, specific_iteration, animate):
    v = deepcopy(map.verticies)
    t = 100
    cr = get_cooling_rate(len(v))
    c = 1
    current_state = get_random_state(v)
    current_cost = evaluation(current_state)
    specific_state = current_state if specific_iteration == c else None
    specific_cost = current_cost if specific_iteration == c else None
    best_state = current_state
    best_cost = current_cost
    best_cost_list = [(c, best_cost)]
    t -= cr
    draw_lines = lambda current_state: map.draw_lines(current_state) if animate else None
    draw_lines(current_state)
    # print(f'({c})\ncurrent state: {[item[0] for item in current_state]} \ncurrent cost: {current_cost}\n********')
    while t > 0:
        c += 1 
        neighbour_state = deepcopy(current_state)
        random_swap(neighbour_state)
        neighbour_cost = evaluation(neighbour_state)
        delta_e = neighbour_cost - current_cost
        
        if delta_e < 0 or np.exp(-delta_e / t) > random.random():
            current_state = neighbour_state
            current_cost = neighbour_cost
            if current_cost < best_cost:
                best_state = current_state 
                best_cost = current_cost 
                best_cost_list.append((c, best_cost))

        if specific_iteration == c:
            specific_state = current_state
            specific_cost = current_cost
        
        draw_lines(current_state)
        # print(f'({c})\ncurrent state: {[item[0] for item in current_state]} \ncurrent cost: {current_cost}\n********')
        
        t -= cr
    
    # print('current cost:', current_cost)
    
    return Solution(best_state, best_cost, specific_state, specific_cost, c, best_cost_list)
sr = 0
def get_random_state(state_space):
    index_state_space = list(range(len(state_space)))
    for i in range(10):
        a = random.randint(sr, len(state_space)-1)
        b = random.randint(sr, len(state_space)-1)
        swap(index_state_space, a, b)
    return [state_space[i] for i in index_state_space]

def evaluation(state_space):
    sum = 0
    for i in range(len(state_space)):
        a = data_model.get_coordinate_of(state_space[i-1][0])
        b = data_model.get_coordinate_of(state_space[i][0])
        sum += haversine((a[1], a[0]), (b[1], b[0]))
    return sum

def random_swap(arr):
    a = random.randint(sr, len(arr)-1)
    b = random.randint(sr, len(arr)-1)
    swap(arr, a, b)

def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

def get_cooling_rate(cities_num):
    if cities_num <= 15:
        return 0.009
    elif cities_num <= 20:
        return 0.005
    else:
        return 0.003

