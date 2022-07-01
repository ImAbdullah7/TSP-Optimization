
class Solution:
    def __init__(self, best_state, best_state_cost, specific_iteration_state, specific_iteration_cost, iterations, chart_data=None) -> None:
        self.best_state = best_state
        self.best_state_cost = best_state_cost
        self.specific_iteration_state = specific_iteration_state
        self.specific_iteration_cost = specific_iteration_cost
        self.iterations = iterations
        self.chart_data = chart_data
        self.gas_efficiency = None
        self.verticies = None

    def calculate_money_cost(self, distance):
        liter_price = 2.18
        return distance / self.gas_efficiency * liter_price

    def __str__(self) -> str:
        value = f'Solution:\n\nState: {self.get_states_names(self.best_state)}\n\nDistance: {self.best_state_cost:.2f} km \
                 \n\nCost({self.gas_efficiency}km\liter): {self.calculate_money_cost(self.best_state_cost): .2f} SR'

        if self.specific_iteration_state and self.specific_iteration_cost:
            if isinstance(self.specific_iteration_state[0], list):
                value = value + f'\n\n\nPopulation at a provided iteration:\n'        
                for i in range(len(self.specific_iteration_state)):
                    value = value + f'\n({i+1})\n\nState: {self.get_states_names(self.specific_iteration_state[i])}\n\nDistance: {self.specific_iteration_cost[i]:.2f} km\n\nCost({self.gas_efficiency}km\liter): {self.calculate_money_cost(self.specific_iteration_cost[i]): .2f} SR\n'        
            else:
                value = value + f'\n\n\nSolution at a provided iteration:\n\nState: {self.get_states_names(self.specific_iteration_state)}\n\nDistance: {self.specific_iteration_cost:.2f} km \
                    \n\nCost({self.gas_efficiency}km\liter): {self.calculate_money_cost(self.specific_iteration_cost): .2f} SR'
        return value

    def __eq__(self, __o: object) -> bool:
        return self.best_state_cost > __o.best_state_cost

    def get_states_names(self, states):
        v = [item[0] for item in states]
        v.append(v[0])
        return ' - '.join(v)

