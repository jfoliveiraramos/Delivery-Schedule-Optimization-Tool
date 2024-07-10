from collections import deque

menu = deque()
title_length = 70

# Clear the screen
def clear_screen(): 
    print('\n' * 100)

# Prints a line of characters
def print_line(char="-"):
    print(f"{char * title_length}\n")

# Displays the title of the menu
def print_title(title, line_char="="):
    padding = (title_length - len(title) - 2) // 2 
    if len(title) % 2 == 0:
        left_padding = padding 
        right_padding = padding 
    else:  
        left_padding = padding
        right_padding = padding + 1
    print(f"\n{line_char * left_padding} {title} {line_char * right_padding}\n")

# Displays the options of the menu
def print_options(options, main_menu=False):
    for i,option in enumerate(options):
        print(f"{i + 1} - {option}")
    if not main_menu:
        print("0 - Go back")
    else:
        print("0 - Exit")
    print(f"\n{'=' * title_length}\n")

    raw_option = input("Choose an option: ")
    try:
        option = int(raw_option)
        if (option < 1 or option > len(options)) and option != 0:
            raise ValueError
    except ValueError:
        print("Invalid option\n")
        return print_options(options)
        
    print()
    return option

# Displays the standard options of the menu
def std_options(option):
    if option == 0:
        menu.pop()

# Displays the delivery schedule and the current solution and cost
def print_delivery_schedule(delivery_schedule, current_solution, current_score):
    print(delivery_schedule)
    print(f"Current Solution: {current_solution}")
    print(f"Current Solution Cost: {current_score}\n\n")

# Displays the main menu
def main_menu(delivery_schedule_info):
    print_title("Delivery Schedule")
    print_delivery_schedule(*delivery_schedule_info)
    return print_options(["Alter Problem Constraints",
                          "Optimization Algorithms",
                          "Display Package Information",
                          "Generate New Package Stream",
                          "Shuffle Package Stream",
                          "Display Map",
                          "Display Results History",
                          ], main_menu=True)
    
# Displays the problem constraints menu
def constraints_menu(delivery_schedule_info):
    print_title("Problem Constraints")
    print_delivery_schedule(*delivery_schedule_info)
    print("This is where the problem constraints are altered ")
    return print_options([
                        "Change Number of Packages (WARNING: Generates new package set)",
                        "Change Map Size (WARNING: Generates new package set)",
                        "Change Cost per km",
                        "Change Cost per min",
                        "Change Travelling Weight",
                        "Change Damage Weight",
                        "Change Delay Weight",
                        "Change Driver Speed",
                        "Change Delivery Delay",
                        ])

# Displays the Algorithms menu
def algorithms_menu(delivery_schedule_info):
    print_title("Optimization Algorithms")
    print_delivery_schedule(*delivery_schedule_info)
    return print_options(["Hill Climbing",
                        "Simulated Annealing",
                        "Tabu Search",
                        "Genetic Algorithm"])
   
# Displays the Hill Climbing menu
def hill_climbing_menu(delivery_schedule_info, hc_data):
    print_title("Hill Climbing")
    print_delivery_schedule(*delivery_schedule_info)
    print(f"{hc_data}\n")
    return print_options([
                        "Apply Hill Climbing",
                        "Change Acceptance Criterion",
                        "Change Number of Iterations",
                        "Change Neighbour Function",
                        ])
    
# Displays the Simulated Annealing menu
def simulated_annealing_menu(delivery_schedule_info, sa_data):
    print_title("Simulated Annealing")
    print_delivery_schedule(*delivery_schedule_info)
    print(f"{sa_data}\n")
    return print_options([
                        "Apply Simulated Annealing",
                        "Change Initial Temperature",
                        "Change Cooling Rate",
                        "Change Fixed Temperature Number of Iterations",
                        "Change Number of Iterations",
                        "Change Neighbour Function",
                        ])

# Displays the Tabu Search menu
def tabu_search_menu(delivery_schedule_info, tabu_search_data):
    print_title("Tabu Search")
    print_delivery_schedule(*delivery_schedule_info)
    print(f"{tabu_search_data}\n")
    return print_options([
                        "Apply Tabu Search",
                        "Change Start Tabu Tenure",
                        "Change Tenure Mode",
                        "Change Tabu Criteria",
                        "Change Number of Iterations",
                        "Change Neighbour Function",
                        "Change Shuffle Probability",
                        ])

# Displays the Genetic Algorithm menu
def genetic_algorithm_menu(delivery_schedule_info, ga_data):
    print_title("Genetic Algorithm")
    print_delivery_schedule(*delivery_schedule_info)
    print(f"{ga_data}\n")
    return print_options([
                        "Apply Genetic Algorithm",
                        "Change Tournament Size",
                        "Change Population Size",
                        "Change Number of Iterations",
                        "Change Mutation Probability",
                        "Change Number of Offsprings",
                        "Change Evolution Strategy",
                        "Change Replacement Strategy",
                        ])

# Displays the results history menu
def history_menu(num_entries):
    print_title("Results History")
    print(f"Number of entries: {num_entries}\n")
    return print_options([
                        "Show History",
                        "Reset History",
                        "Save History to File",
                        ])

# Displays the results of the optimization algorithms
def print_results(current_solution, current_cost, time, solution, cost):
    print(f"Initial solution: {current_solution}")
    print(f"Initial cost: {round(current_cost, 3)}\n")
    print(f"Final solution: {list(solution)}")
    print(f"Final cost: {round(cost, 3)}\n")
    print(f"Time: {round(time, 3)}s")
    print(f"Improvement: {round(-(cost - current_cost), 3)} ({round((-(cost - current_cost) / current_cost) * 100, 3)}%)\n")
