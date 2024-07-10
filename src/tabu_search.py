from bidict import bidict
from solution import *
from collections import deque
import numpy as np

# Tabu Search Data

## tabu_criteria = 'solution' or 'move' or 'package' | 1 or 2 or 3
## solution: tabu tenure is applied to solutions
## move: tabu tenure is applied to moves
## package: tabu tenure is applied to packages

class TabuSearchData:
    def __init__(self, num_iterations, get_all_neighbour_solutions, problem_size, start_tabu_tenure=7, tenure_mode=2, tenure_parameter=0.5, tabu_criteria=1, shuffle_probability=0.1):
        self.num_iterations = num_iterations # Number of iterations the algorithm will run
        self.set_neighbour_function(get_all_neighbour_solutions) # Neighbour operator function
        self.set_problem_size(problem_size) # Number of packages in a solution
        self.set_start_tabu_tenure(start_tabu_tenure) # Starting tabu tenure
        self.set_tenure_mode(tenure_mode, tenure_parameter) # Tabu tenure update mode
        self.set_tabu_criteria(tabu_criteria) # Tabu criteria
        self.iteration = 0 # Current iteration
        self.shuffle_probability = shuffle_probability # Probability of shuffling the solution when the best neighbour solution is not accepted

    # String representation of the Tabu Search Data
    def __str__(self):
        neighbour_function_str = "Swap two contiguous random packages" if self.neighbour_function_num == 1 else "Swap any two random packages" if self.neighbour_function_num == 2 else "Pick any of the neighbour functions with equal probability"
        tenure_mode_str = "Constant" if self.tenure_mode == 1 else "Random" if self.tenure_mode == 2 else "Iteration-based" if self.tenure_mode == 3 else "Dynamic"
        tabu_criteria_str = "Solution" if self.tabu_criteria == 1 else "Move" if self.tabu_criteria == 2 else "Package"
        if self.tenure_mode == 4 or self.tenure_mode == 3:
            return f"Tabu Search Parameters: \n\nStarting Tabu Tenure: {self.start_tabu_tenure}\nTenure Mode: {tenure_mode_str}\nTenure Parameter: {self.tenure_parameter}\nTabu Criteria: {tabu_criteria_str}\nNumber of Iterations: {self.num_iterations}\nNeighbour Function: {neighbour_function_str}\nShuffle Probability: {self.shuffle_probability}"
        return f"Tabu Search Parameters: \n\nStarting Tabu Tenure: {self.start_tabu_tenure}\nTenure Mode: {tenure_mode_str}\nTabu Criteria: {tabu_criteria_str}\nNumber of Iterations: {self.num_iterations}\nNeighbour Function: {neighbour_function_str}\nShuffle Probability: {self.shuffle_probability}"

    # Adds the solution to the tabu list based on the tabu criteria
    def add_tabu(self, solution):
        if self.tabu_criteria == 1: # Solution - Add the solution to the tabu list
            solution_str = str([item.id for item in solution[0]])
            self.tabu_list[solution_str] = self.tabu_tenure + self.iteration
        elif self.tabu_criteria == 2: # Move - Add the move (swap of two particular packages) to the tabu list
            i, j = solution[1]
            swapped_items = (solution[0][i].id, solution[0][j].id)
            row, col = min(swapped_items), max(swapped_items)
            self.tabu_list[row][col] = self.tabu_tenure + self.iteration
        elif self.tabu_criteria == 3: # Package - Add the packages (swap containing any of the two packages) to the tabu list
            i, j = solution[1]
            swapped_items = (solution[0][i].id, solution[0][j].id)
            self.tabu_list[swapped_items[0]] = self.tabu_tenure + self.iteration
            self.tabu_list[swapped_items[1]] = self.tabu_tenure + self.iteration

    # Checks if the solution is tabu based on the tabu criteria
        if self.tenure_mode == 4: # Dynamic - Check if the solution is already visited
            solution_str = str([item.id for item in solution[0]])
            if solution_str in self.visited_solutions:
                self.duplicate_flag = True
            else:
                self.visited_solutions.add(solution_str)
            
    # Checks if the solution is tabu based on the tabu criteria
    def is_tabu(self, solution):
        if self.tabu_criteria == 1: # Solution - Check if the solution is in the tabu list
            solution_str = str([item.id for item in solution[0]])
            return str(solution_str) in self.tabu_list
        elif self.tabu_criteria == 2: # Move - Check if the move (swap of two particular packages) is in the tabu list
            i, j = solution[1]
            swapped_items = (solution[0][i].id, solution[0][j].id)
            row, col = min(swapped_items), max(swapped_items)
            return self.tabu_list[row][col] >= self.iteration
        elif self.tabu_criteria == 3: # Package - Check if the packages (swap containing any of the two packages) are in the tabu list
            i, j = solution[1]
            swapped_items = (solution[0][i].id, solution[0][j].id)
            return self.tabu_list[swapped_items[0]] >= self.iteration or self.tabu_list[swapped_items[1]] >= self.iteration
    
    # Updates the tabu tenure based on the tenure mode
    # Constant: Tabu tenure remains the same
    def update_constant(self):
        pass

    # Random: Tabu tenure is updated randomly based on the maximum tenure
    def update_random(self):
        self.tabu_tenure = np.random.randint(1, self.max_tenure+1)
    
    # Iteration-based: Tabu tenure is updated based on the iteration number and tenure parameter, increasing faster as the iteration number increases
    def update_iteration_based(self):
        self.tabu_tenure = int(max(1, self.iteration**self.tenure_parameter))

    # Dynamic: Tabu tenure is updated based on the iteration number and tenure parameter, increasing or decreasing based on the visited solutions
    def update_dynamic(self):
        if self.duplicate_flag:
            self.tabu_tenure = max(self.min_tenure, self.tabu_tenure+self.tenure_parameter)
        else:
            self.tabu_tenure = max(self.min_tenure, self.tabu_tenure-self.tenure_parameter)
        self.duplicate_flag = False
    
    # Updates the tabu list based on the tabu criteria
    def update_tabu_list(self):
        if self.tabu_criteria == 1: # Solution - Decrease the tabu tenure of all solutions in the tabu list and remove the ones with tenure 0. This is done via a bidirectional dictionary, where the key is the solution and the value is the iteration where the tabu tenure ends
            list_to_delete = self.tabu_list.inverse.get(self.iteration, [])
            for key in list_to_delete:
                del self.tabu_list[str(key)]
        self.iteration += 1

    # Sets the neighbour function based on the neighbour function number
    def set_neighbour_function(self, get_all_neighbour_solutions):
        self.neighbour_function_num = get_all_neighbour_solutions
        if get_all_neighbour_solutions == 1: # Swap two contiguous random packages
            self.get_all_neighbour_solutions = get_all_neighbour_solutions1
        elif get_all_neighbour_solutions == 2: # Swap any two random packages
            self.get_all_neighbour_solutions = get_all_neighbour_solutions2
        elif get_all_neighbour_solutions == 3: # Pick any of the neighbour functions with equal probability
            self.get_all_neighbour_solutions = get_all_neighbour_solutions3
    
    # Sets the problem size
    def set_problem_size(self, problem_size):
        self.problem_size = problem_size # Number of packages in a solution
        self.max_tenure = int(problem_size**0.5) # Maximum tabu tenure

    # Sets the starting tabu tenure
    def set_start_tabu_tenure(self, start_tabu_tenure):
        self.tabu_tenure = start_tabu_tenure # Tabu tenure
        self.start_tabu_tenure = start_tabu_tenure # Starting tabu tenure
        self.min_tenure = start_tabu_tenure # Minimum tabu tenure

    # Sets the tenure mode
    def set_tenure_mode(self, tenure_mode, tenure_parameter):
        self.tenure_mode = tenure_mode # Tabu tenure update mode
        if tenure_mode == 1: # Constant - Tabu tenure remains the same
            self.update = self.update_constant
        elif tenure_mode == 2: # Random - Tabu tenure is updated randomly based on the maximum tenure
            self.update = self.update_random
        elif tenure_mode == 3: # Iteration-based - Tabu tenure is updated based on the iteration number and tenure parameter, increasing faster as the iteration number increases
            self.tenure_parameter = tenure_parameter # Tenure parameter
            self.update = self.update_iteration_based 
        elif tenure_mode == 4: # Dynamic - Tabu tenure is updated based on the iteration number and tenure parameter, increasing or decreasing based on the visited solutions
            self.visited_solutions = set() # Set of visited solutions
            self.duplicate_flag = False # Flag to check if the solution is already visited
            self.tenure_parameter = tenure_parameter # Tenure parameter
            self.update = self.update_dynamic
    
    # Sets the tabu criteria
    def set_tabu_criteria(self, tabu_criteria):
        self.tabu_criteria = tabu_criteria # Tabu criteria
        if tabu_criteria == 1: # Solution - Tabu tenure is applied to solutions
            self.tabu_list = bidict()
        elif tabu_criteria == 2: # Move - Tabu tenure is applied to moves (swaps of two particular packages)
            self.tabu_list = np.zeros((self.problem_size, self.problem_size))
        elif tabu_criteria == 3: # Package - Tabu tenure is applied to packages (swaps containing any of the two packages)
            self.tabu_list = np.zeros(self.problem_size)
    
    # Resets the tabu search data
    def reset(self):
        self.tabu_tenure = self.start_tabu_tenure # Tabu tenure
        self.iteration = 0
        if self.tabu_criteria == 1: # Solution - Reset the tabu list
            self.tabu_list = bidict()
        elif self.tabu_criteria == 2: # Move - Reset the tabu list
            self.tabu_list = np.zeros((self.problem_size, self.problem_size))
        elif self.tabu_criteria == 3: # Package - Reset the tabu list
            self.tabu_list = np.zeros(self.problem_size)
        if self.tenure_mode == 4: # Dynamic - Reset the visited solutions and duplicate flag
            self.visited_solutions = set()
            self.duplicate_flag = False

    # Runs the tabu search algorithm
    def run(self, delivery_schedule):
        self.reset()
        return tabu_search(delivery_schedule, self, evaluate_solution)         
    
# Tabu Search Algorithm
def tabu_search(delivery_schedule, tabu_search_data, evaluate_solution):
    iteration = 0
    best_solution = delivery_schedule.packages # Initial solution
    best_score = evaluate_solution(delivery_schedule, best_solution) # Initial score
    temp_solution = best_solution
    temp_score = best_score
    best_costs = deque([])
    costs = deque([])
    tenures = deque([])

    best_costs.append(-best_score)
    costs.append(-best_score)
    tenures.append(tabu_search_data.tabu_tenure)

    while iteration < tabu_search_data.num_iterations: # Iterates until the number of iterations is reached
        iteration += 1

        # Get the best neighbour solution and Aspiration Criteria (if it is better than the best solution, it is accepted)
        all_neighbour = tabu_search_data.get_all_neighbour_solutions(delivery_schedule, temp_solution)
        all_neighbour_filtered = list(filter(lambda x: not tabu_search_data.is_tabu(x) or evaluate_solution(delivery_schedule, x[0]) > best_score, all_neighbour))
        if len(all_neighbour_filtered) != 0:
            
            # Get the best neighbour solution
            best_neighbour_solution = get_best_solution(delivery_schedule, all_neighbour_filtered)

            if best_neighbour_solution is None:
                print("No best neighbour solution found")
                break

            temp_solution = best_neighbour_solution[0]
            temp_score = evaluate_solution(delivery_schedule, temp_solution)

            # Update the best solution if the neighbour solution is better
            if temp_score > best_score:
                best_solution = temp_solution
                best_score = temp_score
        
            # Diversification - Shuffle the solution if the best neighbour solution is not accepted with a certain probability
            if temp_score < best_score and np.random.rand() < tabu_search_data.shuffle_probability:
                temp_solution = np.random.permutation(temp_solution)
                temp_score = evaluate_solution(delivery_schedule, temp_solution)
            

            # Adds the best neighbour solution to the tabu list
            tabu_search_data.add_tabu(best_neighbour_solution)

        # Update the tabu tenure
        tabu_search_data.update()

        # Update the tabu list and tabu iteration
        tabu_search_data.update_tabu_list()

        costs.append(-temp_score)
        best_costs.append(-best_score)
        tenures.append(tabu_search_data.tabu_tenure)
    
    return best_solution, best_costs, costs, tenures
