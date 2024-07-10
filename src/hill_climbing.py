from solution import *
import numpy as np

# Hill Climbing Data
class HillClimbingData:
    def __init__(self, acceptance_criterion, neighbourhood_function, num_iterations):
        self.acceptance_criterion = acceptance_criterion 
        self.num_iterations = num_iterations
        self.neighbourhood_function = neighbourhood_function
        self.set_acceptance_criterion(acceptance_criterion)
        self.set_neighbour_function(neighbourhood_function)
    
    # String representation of the Hill Climbing Data
    def __str__(self):
        acceptance_criterion_str = "First Accept" if self.acceptance_criterion == 1 else "Best Accept"
        neighbour_function_str = "Swap two contiguous random packages" if self.neighbourhood_function == 1 else "Swap any two random packages" if self.neighbourhood_function == 2 else "Pick any of the neighbour functions with equal probability"
        return f"Hill Climbing Parameters: \n\nAcceptance Criterion: {acceptance_criterion_str}\nNumber of Iterations: {self.num_iterations}\nNeighbour Function: {neighbour_function_str}\n"

    # Sets the acceptance criterion based on the acceptance criterion number
    def set_acceptance_criterion(self, acceptance_criterion):
        self.acceptance_criterion = acceptance_criterion
        if acceptance_criterion == 1:
            self.function = hill_climbing_fa
        elif acceptance_criterion == 2:
            self.function = hill_climbing_ba
        
        self.set_neighbour_function(self.neighbourhood_function)

    # Sets the neighbour function based on the neighbour function number
    def set_neighbour_function(self, neighbourhood_function):
        self.neighbourhood_function = neighbourhood_function
        if self.acceptance_criterion == 1: # First Accept
            if neighbourhood_function == 1: # Swap two contiguous random packages
                self.get_neighbour_solution = get_neighbour_solution1
            elif neighbourhood_function == 2: # Swap any two random packages
                self.get_neighbour_solution = get_neighbour_solution2
            elif neighbourhood_function == 3: # Pick any of the neighbour functions with equal probability
                self.get_neighbour_solution = get_neighbour_solution3
        elif self.acceptance_criterion == 2: # Best Accept
            if neighbourhood_function == 1: # Swap two contiguous random packages
                self.get_neighbour_solution = get_all_neighbour_solutions1
            elif neighbourhood_function == 2: # Swap any two random packages
                self.get_neighbour_solution = get_all_neighbour_solutions2
            elif neighbourhood_function == 3: # Pick any of the neighbour functions with equal probability
                self.get_neighbour_solution = get_all_neighbour_solutions3

    # Runs the Hill Climbing algorithm
    def run(self, delivery_schedule):
        solution, costs = self.function(delivery_schedule, self.num_iterations, self.get_neighbour_solution, evaluate_solution)
        return solution, costs


# Hill Climbing First Accept
def hill_climbing_fa(delivery_schedule, num_iterations, get_neighbour_solution, evaluate_solution):
    iteration = 0
    best_solution = delivery_schedule.packages # Initial solution
    best_score = evaluate_solution(delivery_schedule, best_solution) # Initial score
    costs = deque([])
    costs.append(-best_score)

    while iteration < num_iterations: # While the number of iterations is less than the number of iterations the algorithm will run
        iteration += 1

        temp_solution = get_neighbour_solution(delivery_schedule, best_solution)[0] # Gets a random neighbour solution
        temp_score = evaluate_solution(delivery_schedule, temp_solution) # Evaluates the neighbour solution

        if temp_score > best_score: # If the neighbour solution is better than the current solution
            best_solution = temp_solution
            best_score = temp_score
        
        costs.append(-best_score)
    
    return best_solution, costs

# Hill Climbing Best Accept
def hill_climbing_ba(delivery_schedule, num_iterations, get_all_neighbour_solutions, evaluate_solution):
    iteration = 0
    best_solution = delivery_schedule.packages # Initial solution
    best_score = evaluate_solution(delivery_schedule, best_solution) # Initial score
    costs = deque([])
    costs.append(-best_score)

    while iteration < num_iterations: # While the number of iterations is less than the number of iterations the algorithm will run
        iteration += 1

        temp_solution = get_best_solution(delivery_schedule, get_all_neighbour_solutions(delivery_schedule, best_solution))[0] # Gets the best neighbour solution
        temp_score = evaluate_solution(delivery_schedule, temp_solution) # Evaluates the neighbour solution
        
        if temp_score > best_score: # If the neighbour solution is better than the current solution
            best_solution = temp_solution
            best_score = temp_score
            
            costs.append(-best_score)
        else:
            break

    return best_solution, costs
