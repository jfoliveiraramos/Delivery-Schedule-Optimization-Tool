import random
import math
from solution import *

# Simulated Annealing Data
class SimulatedAnnealingData:
    def __init__(self, neighbourhood_function=3, start_temp=1000, cooling_rate=0.95 , fixed_temp_iterations=2, num_iterations=1000):
        self.start_temp = start_temp # Initial temperature
        self.cooling_rate = cooling_rate # Cooling rate
        self.fixed_temp_iterations = fixed_temp_iterations # Number of iterations with fixed temperature
        self.num_iterations = num_iterations # Number of iterations the algorithm will run
        self.set_neighbour_function(neighbourhood_function) # Neighbour function

    # String representation of the Simulated Annealing Data
    def __str__(self):
        neighbour_function_str = "Swap two contiguous random packages" if self.neighbourhood_function == 1 else "Swap any two random packages" if self.neighbourhood_function == 2 else "Pick any of the neighbour functions with equal probability"
        return f"Simulated Annealing Parameters: \n\nStart temperature: {self.start_temp}\nCooling rate: {self.cooling_rate}\nNumber of iterations until temperature decrease: {self.fixed_temp_iterations}\nNumber of iterations: {self.num_iterations}\nNeighbour Function: {neighbour_function_str}"
    
    # Sets the neighbour function based on the neighbour function number
    def set_neighbour_function(self, neighbourhood_function):
        self.neighbourhood_function = neighbourhood_function
        if neighbourhood_function == 1: # Swap two contiguous random packages
            self.get_neighbour_solution = get_neighbour_solution1 
        elif neighbourhood_function == 2: # Swap any two random packages
            self.get_neighbour_solution = get_neighbour_solution2
        elif neighbourhood_function == 3: # Pick any of the neighbour functions with equal probability
            self.get_neighbour_solution = get_neighbour_solution3
    
    # Runs the Simulated Annealing algorithm
    def run(self, delivery_schedule):
        return simulated_annealing(delivery_schedule, self, evaluate_solution)

# Simulated Annealing Algorithm  
def simulated_annealing(delivery_schedule, sa_data, evaluate_solution):
    iteration = 0
    current_solution = delivery_schedule.packages # Initial solution
    current_score = evaluate_solution(delivery_schedule, current_solution) # Initial score

    best_solution = current_solution
    best_score = current_score

    temperature = sa_data.start_temp # Initial temperature
    cooling_rate = sa_data.cooling_rate # Cooling rate

    best_costs = deque([])
    costs = deque([])
    temperatures = deque([])
    best_costs.append(-best_score)
    costs.append(-best_score)
    temperatures.append(temperature)

    temp_iteration = 0

    while iteration < sa_data.num_iterations: # While the number of iterations is less than the number of iterations the algorithm will run

        if temp_iteration == sa_data.fixed_temp_iterations: # If the number of iterations with fixed temperature is reached
            temp_iteration = 0
            temperature *= cooling_rate
        
        temp_iteration += 1
        iteration += 1

        temp_solution = sa_data.get_neighbour_solution(delivery_schedule, best_solution)[0] # Get a neighbour solution
        temp_score = evaluate_solution(delivery_schedule, temp_solution) # Evaluate the neighbour solution
        
        delta = temp_score - current_score  # Calculate the difference between the neighbour solution and the current solution

        if delta > 0: # If the neighbour solution is better than the current solution, change the current solution
            current_solution = temp_solution
            current_score = temp_score
        elif delta < 0: # If the neighbour solution is worse than the current solution, change the current solution with a certain probability
            rand = random.uniform(0, 1)
            prob = math.e ** (delta / temperature)
            if rand < prob:
                current_solution = temp_solution
                current_score = temp_score
    
        if current_score > best_score: # If the current solution is better than the best solution, change the best solution
            best_solution = current_solution
            best_score = current_score
        
        costs.append(-current_score)
        best_costs.append(-best_score)
        temperatures.append(temperature)
        
    return best_solution, best_costs, costs, temperatures
