import hill_climbing


def perform(map, specific_iteration, animate):
    # TODO:- store solutions list instead of solutions_cost list,
    # then replace best_solution with getting minimum cost from solutions list and test it.
    # (I'm too lazy to do that now).

    solutions_cost = []
    first_iterations = 10
    best_solution, sp_sol = r(map, 0, first_iterations, specific_iteration, animate, solutions_cost)

    current_itr = first_iterations

    second_iterations = 5
    while True:
        a, b = r(map, current_itr, second_iterations, specific_iteration, animate, solutions_cost)
        current_itr += second_iterations
        
        if b:
            sp_sol = b

        if a.best_state_cost >= best_solution.best_state_cost:
            break
        best_solution = a


    
    # for i in range(1, itr):
    #     sol = hill_climbing.perform(map, None)
    #     if sol.best_state_cost < best_solution.best_state_cost:
    #         best_solution = sol
            
    #     if specific_iteration == i+1:
    #         sp_sol = sol
    #     print('*'*10)
    #     print('itr: ', i+1)
    #     print(sol)
    #     print('*'*10)

    best_solution.iterations = current_itr
    best_solution.chart_data = solutions_cost

    if sp_sol:
        best_solution.specific_iteration_cost = sp_sol.best_state_cost
        best_solution.specific_iteration_state = sp_sol.best_state
    
    return best_solution


def r(map, c_itr, itr, sp_itr, animate, solutions_cost):
    c_itr += 1
    best_solution = hill_climbing.perform(map, None, animate)
    sp_sol = best_solution if c_itr == sp_itr else None
    solutions_cost.append((c_itr, best_solution.best_state_cost))

    # print('*'*10)
    # print('itr: ', c_itr)
    # print(best_solution)
    # print('*'*10)

    for i in range(c_itr, itr + c_itr - 1):
        sol = hill_climbing.perform(map, None, animate)
        solutions_cost.append((i+1, sol.best_state_cost))
        if sol.best_state_cost < best_solution.best_state_cost:
            best_solution = sol
            
        if sp_itr == i+1:
            sp_sol = sol

        # print('*'*10)
        # print('itr: ', i+1)
        # print(sol)
        # print('*'*10)

    return (best_solution, sp_sol)

    
