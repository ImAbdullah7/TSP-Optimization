from copy import deepcopy
import random
import data_model
from haversine import haversine
from solution import Solution

bfi = []
sr = 0

def perform(map, specific_iteration, animate):
    bfi.clear()
    cities = deepcopy(map.verticies)
    population_num = 10
    population = [random_swap(cities, 2) for _ in range(population_num)]
    p_fitness = fitness(population, 1)
    specific_population = population if specific_iteration == 1 else None
    specific_cost = [evaluation(order) for order in population] if specific_iteration == 1 else None
    draw_population = lambda map, population: _draw_population(map, population) if animate else None
    draw_population(map, population)
    # print(f'({1}) {min([evaluation(order) for order in population]):.4f}')

    generations = 0
    mult = len(cities) / 5 
    if mult <= 3 :
        generations = mult * 350
    else:
        generations = mult * 550

    for i in range(2, int(generations)+1):
        create_new_generation(population, p_fitness)
        p_fitness = fitness(population, i)
        
        if specific_iteration == i:
            specific_population = population 
            specific_cost = [evaluation(order) for order in population]
        
        draw_population(map, population)
        # print(f'({i}) {min([evaluation(order) for order in population]):.4f}')
    
    best_order_cost, best_order = min([(evaluation(order), order) for order in population])

    return Solution(best_order, best_order_cost, specific_population, specific_cost, i, bfi)

def random_swap(list, n):
    clist = deepcopy(list)
    for _ in range(n):
        a = random.randint(sr, len(list)-1)
        b = random.randint(sr, len(list)-1)
        temp = list[a]
        list[a] = list[b]
        list[b] = temp
    return clist

def evaluation(state_space):
    sum = 0
    for i in range(len(state_space)):
        a = data_model.get_coordinate_of(state_space[i-1][0])
        b = data_model.get_coordinate_of(state_space[i][0])
        sum += haversine((a[1], a[0]), (b[1], b[0]))
    return sum

def fitness(population, i):
    f_list = [1/(evaluation(order)+1) for order in population]
    bfi.append((i, max(f_list)))
    sum_of_f = sum(f_list)
    normalized_f = [f/sum_of_f for f in f_list]
    return normalized_f

def create_new_generation(population, fitness):
    for i, order in enumerate(population):
        second_order = pick_order(population, fitness)
        crossed_over_order = cross_over(order, second_order)
        mutate(crossed_over_order, 0.1)
        if evaluation(crossed_over_order) < evaluation(order):
            population[i] = crossed_over_order

def pick_order(population, fitness):
    i = 0
    r = random.uniform(0, 1)
    while r > 0:
        r -= fitness[i]
        i += 1
    i -= 1
    return deepcopy(population[i])

def cross_over(first_order, second_order):
    start_index = 0
    end_index = random.randint(start_index+1, len(first_order))
    crossed_over = first_order[start_index:end_index]
    for item in second_order:
        if item not in crossed_over:
            crossed_over.append(item)
    return crossed_over

def mutate(order, rate):
    for _ in range(len(order)):
        if rate > random.uniform(0, 1):
            random_swap(order, 1)

def _draw_population(map, population):
    for order in population:
        map.draw_lines(order)