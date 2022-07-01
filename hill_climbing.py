import random
import data_model
from map import Map
from haversine import haversine
from solution import Solution

def perform(map, specific_iteration, animate):
    v = map.verticies.copy()
    
    current_state = random_state(v)
    current_state_cost = evaluation(current_state)
    # print(f'-------\ncurrent state {[item[0] for item in current_state]} = {current_state_cost}\n')
    best_neighbour_state, best_neighbour_cost = best_neighbour(current_state)
    draw_lines = lambda current_state: map.draw_lines(current_state) if animate else None
    draw_lines(current_state)
    c = 1
    s_cost = current_state_cost if specific_iteration == c else None
    s_state = current_state if specific_iteration == c else None

    while best_neighbour_cost < current_state_cost:
        current_state = best_neighbour_state
        current_state_cost = best_neighbour_cost
        # print(f'-------\ncurrent state {[item[0] for item in current_state]} = {current_state_cost}\n')
        best_neighbour_state, best_neighbour_cost = best_neighbour(current_state)
        draw_lines(current_state)
        c += 1
        if specific_iteration == c:
            s_cost = current_state_cost
            s_state = current_state
    
    return Solution(current_state, current_state_cost, s_state, s_cost, c)

def random_state(state_space):
    index_state_space = list(range(len(state_space)))
    for i in range(10):
        a = random.randint(0, len(state_space)-1)
        b = random.randint(0, len(state_space)-1)
        swap(index_state_space, a, b)
    return [state_space[i] for i in index_state_space]

def swap(arr, i, j):
    # if i == 0 or j == 0: return
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

def evaluation(state_space):
    sum = 0
    for i in range(len(state_space)):
        a = data_model.get_coordinate_of(state_space[i-1][0])
        b = data_model.get_coordinate_of(state_space[i][0])
        sum += haversine((a[1], a[0]), (b[1], b[0]))
    return sum

def best_neighbour(state_space):
    temp = state_space.copy()
    swap(temp, 0, 1)
    cost = evaluation(temp)
    best_state = temp
    best_state_cost = cost

    for i in range(len(state_space)):
        for j in range(i+1, len(state_space)):
            temp = state_space.copy()
            swap(temp, i, j)
            cost = evaluation(temp)
            best_state = temp if cost < best_state_cost else best_state
            best_state_cost = cost if cost < best_state_cost else best_state_cost
            # print([item[0] for item in temp], ' = ', cost)

    # print('\nbest: ', [item[0] for item in best_state], ' =', best_state_cost)
    return best_state, best_state_cost




