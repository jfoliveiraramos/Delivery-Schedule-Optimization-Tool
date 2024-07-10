from package import *
from delivery_schedule import *
from collections import deque
import numpy as np
import copy

# Evaluate the cost of a solution (we are trying to minimize the cost)
def evaluate_solution(delivery_schedule, solution):
    return -delivery_schedule.total_cost(solution)

# Swap two consecutive deliveries in a solution
def get_neighbour_solution1(delivery_schedule, solution):
    neighbour_solution = copy.deepcopy(solution)
    
    num_packages = delivery_schedule.num_packages
    i = np.random.randint(0, num_packages-1)
    
    neighbour_solution[i], neighbour_solution[i+1] = solution[i+1], solution[i]
    
    return (neighbour_solution, (i, i+1))

# Swap two random deliveries in a solution
def get_neighbour_solution2(delivery_schedule, solution):
    neighbour_solution = copy.deepcopy(solution)

    num_packages = delivery_schedule.num_packages
    i = np.random.randint(0, num_packages)
    j = (i + np.random.randint(1, num_packages)) % num_packages

    neighbour_solution[i], neighbour_solution[j] = solution[j], solution[i]

    return (neighbour_solution, (i, j))

# Pick an algorithm to get a neighbour solution randomly
def get_neighbour_solution3(delivery_schedule, solution):
    if (np.random.randint(0,2)==0):
        return get_neighbour_solution1(delivery_schedule, solution)
    else:
        return get_neighbour_solution2(delivery_schedule, solution)

# Get all possible neighbours of a solution following get_neighbour_solution1
def get_all_neighbour_solutions1(delivery_schedule, solution):
    neighbour_solutions = []

    num_packages = delivery_schedule.num_packages
    for i in range(num_packages-1):
        neighbour_solution = copy.deepcopy(solution)
        neighbour_solution[i], neighbour_solution[i+1] = solution[i+1], solution[i]
        neighbour_solutions.append((neighbour_solution, (i, i+1)))

    return neighbour_solutions

# Get all possible neighbours of a solution following get_neighbour_solution2
def get_all_neighbour_solutions2(delivery_schedule, solution):
    neighbour_solutions = []

    num_packages = delivery_schedule.num_packages
    for i in range(num_packages):
        for j in range(i+1, num_packages):
            neighbour_solution = copy.deepcopy(solution)
            neighbour_solution[i], neighbour_solution[j] = solution[j], solution[i]
            neighbour_solutions.append((neighbour_solution, (i, j)))

    return neighbour_solutions

# Get all possible neighbours of a solution following get_neighbour_solution1 and get_neighbour_solution2
def get_all_neighbour_solutions3(delivery_schedule, solution):
    return get_all_neighbour_solutions1(delivery_schedule, solution) + get_all_neighbour_solutions2(delivery_schedule, solution)

# Get the best solution from a list of solutions
def get_best_solution(delivery_schedule, solutions):
    best_solution = solutions[0]
    best_score = evaluate_solution(delivery_schedule, best_solution[0])

    for solution in solutions:
        temp_score = evaluate_solution(delivery_schedule, solution[0])
        if temp_score > best_score:
            best_solution = solution
            best_score = temp_score

    return best_solution
