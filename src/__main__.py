from menu import *
from package import * 
from delivery_schedule import *
from simulated_annealing import *
from tabu_search import *
from genetic_algorithm import *
from solution import *
from hill_climbing import *
from plot import *
from history import *
import time

delivery_schedule = DeliverySchedule(50, 10, 1, 1, 1, 1, 1, 60, 0) # Default delivery schedule
current_solution = delivery_schedule.packages
current_cost = delivery_schedule.total_cost(current_solution)

hc_data = HillClimbingData(1, 3, 1000) # Default hill climbing data
sa_data = SimulatedAnnealingData(3, 1000, 0.99, 2, 1000) # Default simulated annealing data
tb_data = TabuSearchData(50, 3, delivery_schedule.num_packages, 7, 3, 0.3, 1, 0.1) # Default tabu search data
ga_data = GeneticAlgorithmData(10, 100, 150, 0.5, 25, True, False) # Default genetic algorithm data

# Updates the delivery schedule with a new set of packages
def reset_schedule():
    global current_solution, current_cost, delivery_schedule
    delivery_schedule.packages = generate_package_stream(delivery_schedule.num_packages, delivery_schedule.map_size)
    current_solution = delivery_schedule.packages
    current_cost = delivery_schedule.total_cost(current_solution)

# Updates the cost of the current solution
def update_solution_cost():
    global current_solution, current_cost, delivery_schedule
    current_cost = delivery_schedule.total_cost(current_solution)

# Updates the current solution and cost
def update_results(solution, cost):
    global current_solution, current_cost, delivery_schedule
    current_solution = solution
    current_cost = cost
    delivery_schedule.packages = solution

# Main menu
def run_main():
    global current_solution, current_cost, delivery_schedule

    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = main_menu(delivery_schedule_info)

    if option == 1: # Opens the constraints menu
        menu.append("constraints")
    elif option == 2: # Opens the algorithms menu
        menu.append("algorithms")
    elif option == 3: # Displays the information of all packages in the current solution
        for package in delivery_schedule.packages:
            package.display()
        input("Press Enter to continue...")
    elif option == 4: # Updates the delivery schedule with a new set of packages
        reset_schedule()
    elif option == 5: # Shuffles the current solution
        delivery_schedule.packages = random.sample(delivery_schedule.packages, delivery_schedule.num_packages)
        current_solution = delivery_schedule.packages
        current_cost = delivery_schedule.total_cost(current_solution)
    elif option == 6: # Displays the current solution in the map
        annotate = input("Annotate packages on map? (Y/N): ") in ["Y", "y"]
        arrows = input("Draw arrows between packages? (Y/N): ") in ["Y", "y"]
        display_map(delivery_schedule.packages, delivery_schedule.map_size, annotate, arrows)
        input("Press Enter to continue...")
    elif option == 7: # Displays the history of the optimization algorithms
        menu.append("history")
    else:
        std_options(option)

# Constraints menu
## Define the values for the parameters of the problem instance
def run_constraints():
    global tb_data, ga_data, delivery_schedule
    
    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = constraints_menu(delivery_schedule_info)

    if option == 1: # Change the number of packages in the delivery schedule
        delivery_schedule.num_packages = int(input("Enter the number of packages: "))
        reset_schedule()
        tb_data.set_problem_size(delivery_schedule.num_packages)
    elif option == 2: # Change the map size of the delivery schedule
        delivery_schedule.map_size = int(input("Enter the map size: "))
        reset_schedule()
        ga_data.map_size = delivery_schedule.map_size
    elif option == 3: # Change the cost per km of the delivery schedule
        delivery_schedule.cost_per_km = int(input("Enter the cost per km: "))
        update_solution_cost()
    elif option == 4: # Change the cost per min of the delivery schedule
        delivery_schedule.cost_per_min = int(input("Enter the cost per min: "))
        update_solution_cost()
    elif option == 5: # Change the travelling weight of the delivery schedule
        delivery_schedule.travelling_weight = float(input("Enter the travelling weight: "))
        update_solution_cost()
    elif option == 6: # Change the damage weight of the delivery schedule
        delivery_schedule.damage_weight = float(input("Enter the damage weight: "))
        update_solution_cost()
    elif option == 7: # Change the delay weight of the delivery schedule
        delivery_schedule.delay_weight = float(input("Enter the delay weight: "))
        update_solution_cost()
    elif option == 8: # Change the driver's speed of the delivery schedule
        delivery_schedule.driver_speed = int(input("Enter the driver's speed: "))
        update_solution_cost()
    elif option == 9: # Change the delivery delay of the delivery schedule
        delivery_schedule.delivery_delay = int(input("Enter the delivery delay: "))
        update_solution_cost()
    else:
        std_options(option)

# Algorithms menu
def run_algorithms():
    global delivery_schedule, current_solution, current_cost
    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = algorithms_menu(delivery_schedule_info)
    
    if option == 1: # Opens the hill climbing menu
        menu.append("hill_climbing")
    elif option == 2: # Opens the simulated annealing menu
        menu.append("simulated_annealing")
    elif option == 3: # Opens the tabu search menu
        menu.append("tabu_search")
    elif option == 4: # Opens the genetic algorithm menu
        menu.append("genetic_algorithm")
    else:
        std_options(option)

# Hill Climbing menu
## Define the values for the parameters of the hill climbing algorithm or run hill climbing
def run_hill_climbing():   
    global hc_data, current_solution, current_cost, delivery_schedule
    
    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = hill_climbing_menu(delivery_schedule_info, hc_data)

    if option == 1: # Run hill climbing
        initial_time = time.time()
        solution, best_costs = hc_data.run(delivery_schedule)
        execution_time = time.time() - initial_time
        
        cost = delivery_schedule.total_cost(solution)

        register_in_history({
            "algorithm": "Hill Climbing",
            "delivery_schedule": copy.deepcopy(delivery_schedule),
            "algorithm_data": copy.deepcopy(hc_data),
            "initial_solution": copy.deepcopy(current_solution),
            "initial_cost": current_cost,
            "final_solution": copy.deepcopy(solution),
            "final_cost": cost,
            "time": round(execution_time, 3),
            "improvement": round(-(cost - current_cost), 3),
            "improvement_percentage": round((cost - current_cost) / current_cost * 100, 3),
            "plot": (best_costs,)
        })

        # Display the results
        print_results(current_solution, current_cost, execution_time, solution, cost)

        # Plot the results
        plot_hc(best_costs, hc_data)

        # Ask the user if they want to keep the new solution as the current solution
        keep = input("Keep new solution? (Y/N): ")
        if keep == "Y" or keep == "y":
            update_results(solution, cost)
    elif option == 2: # Change the acceptance criterion
        print("1 - First Accept")
        print("2 - Best Accept")
        num = 0
        while num not in [1, 2]:
            num = int(input("Select the acceptance criterion: "))
        hc_data.set_acceptance_criterion(num)
    elif option == 3: # Change the number of iterations
        hc_data.num_iterations = int(input("Enter the number of iterations: "))
    elif option == 4: # Change the neighbour function
        print("1 - Swap two contiguous random packages")
        print("2 - Swap any two random packages")
        print("3 - Pick any of the neighbour functions with equal probability")
        num = 0
        while num not in [1, 2, 3]:
            num = int(input("Select a neighbour function {1, 2 or 3}: "))
        hc_data.set_neighbour_function(num)
    else:
        std_options(option)


# Simulated Annealing menu
## Define the values for the parameters of the simulated annealing algorithm or run simulated annealing
def run_simulated_annealing():
    global sa_data, current_solution, current_cost, delivery_schedule
   
    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = simulated_annealing_menu(delivery_schedule_info, sa_data)

    if option == 1: # Run simulated annealing
        initial_time = time.time()
        solution, best_costs, costs, temperatures = sa_data.run(delivery_schedule)
        execution_time = time.time() - initial_time

        cost = delivery_schedule.total_cost(solution)

        register_in_history({
            "algorithm": "Simulated Annealing",
            "delivery_schedule": copy.deepcopy(delivery_schedule),
            "algorithm_data": copy.deepcopy(sa_data),
            "initial_solution": copy.deepcopy(current_solution),
            "initial_cost": current_cost,
            "final_solution": copy.deepcopy(solution),
            "final_cost": cost,
            "time": round(execution_time, 3),
            "improvement": round(-(cost - current_cost), 3),
            "improvement_percentage": round((cost - current_cost) / current_cost * 100, 3),
            "plot": (costs, best_costs, temperatures),
        })

        # Display the results
        print_results(current_solution, current_cost, execution_time, solution, cost)

        # Plot the results
        plot_sa(costs, best_costs, temperatures, sa_data)

        # Ask the user if they want to keep the new solution as the current solution
        keep = input("Keep new solution? (Y/N): ")
        if keep == "Y" or keep == "y":
            update_results(solution, cost)
    elif option == 2: # Change the starting temperature
        sa_data.start_temp = int(input("Enter the starting temperature: "))
    elif option == 3: # Change the cooling rate
        sa_data.cooling_rate = float(input("Enter the cooling rate: "))
    elif option == 4: # Change the number of iterations for the fixed temperature
        sa_data.fixed_temp_iterations = int(input("Enter the number of iterations for the fixed temperature: "))
    elif option == 5: # Change the number of iterations
        sa_data.num_iterations = int(input("Enter the number of iterations: "))
    elif option == 6: # Change the neighbour function
        print("1 - Swap two contiguous random packages")
        print("2 - Swap any two random packages")
        print("3 - Pick any of the neighbour functions with equal probability")
        num = 0
        while num not in [1, 2, 3]:   
            num = int(input("\Select a neighbour function {1, 2 or 3}: "))
        sa_data.set_neighbour_function(num)
    else:
        std_options(option)

# Tabu Search menu
## Define the values for the parameters of the tabu search algorithm or run tabu search
def run_tabu_search():

    global tb_data, current_solution, current_cost, delivery_schedule
    
    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = tabu_search_menu(delivery_schedule_info, tb_data)
    
    if option == 1: # Run tabu search
        initial_time = time.time()
        solution, best_costs, costs, tenures = tb_data.run(delivery_schedule)
        execution_time = time.time() - initial_time
        
        cost = delivery_schedule.total_cost(solution)

        register_in_history({
            "algorithm": "Tabu Search",
            "delivery_schedule": copy.deepcopy(delivery_schedule),
            "algorithm_data": copy.deepcopy(tb_data),
            "initial_solution":  copy.deepcopy(current_solution),
            "initial_cost": current_cost,
            "final_solution": copy.deepcopy(solution),
            "final_cost": cost,
            "time": round(execution_time, 3),
            "improvement": round(-(cost - current_cost), 3),
            "improvement_percentage": round((cost - current_cost) / current_cost * 100, 3),
            "plot": (costs, best_costs, tenures)
        })

        # Display the results
        print_results(current_solution, current_cost, execution_time, solution, cost)

        # Plot the results
        plot_tabu_search(costs, best_costs, tenures, tb_data)

        # Ask the user if they want to keep the new solution as the current solution
        keep = input("Keep new solution? (Y/N): ")
        if keep == "Y" or keep == "y":
            update_results(solution, cost)
    elif option == 2: # Change the starting tabu tenure
        tb_data.set_start_tabu_tenure(int(input("Enter the starting tabu tenure: ")))
    elif option == 3: # Change the tabu tenure mode
        print("1. Constant")
        print("2. Random")
        print("3. Iteration Based")
        print("4. Dynamic")
        num = 0
        while num not in [1, 2, 3, 4]:
            num = int(input("Select a tabu tenure mode {1, 2, 3 or 4}: "))
        tenure_paremeter = tb_data.tenure_parameter
        if num == 3 or num == 4: # If the tabu tenure mode is iteration based or dynamic ask for the tenure parameter
            tenure_paremeter = float(input("Enter the value for the tenure parameter: "))
        tb_data.set_tenure_mode(num, tenure_paremeter)
    elif option == 4: # Change the tabu criteria
        print("1 - Solution")
        print("2 - Move")
        print("3 - Package")
        num = 0
        while num not in [1, 2, 3]:
            num = int(input("Select a tabu criteria: "))
        tb_data.set_tabu_criteria(num)
    elif option == 5: # Change the number of iterations
        tb_data.num_iterations = int(input("Enter the number of iterations: "))
    elif option == 6: # Change the neighbour function
        print("1 - Swap two contiguous random packages")
        print("2 - Swap any two random packages")
        print("3 - Pick any of the neighbour functions with equal probability")
        num = 0
        while num not in [1, 2, 3]:
            num = int(input("Select a neighbour function {1, 2 or 3}: "))
        tb_data.set_neighbour_function(num)
    elif option == 7: # Change the shuffle probability
        shuffle_probability = -1
        while shuffle_probability < 0 or shuffle_probability > 1:
            shuffle_probability = float(input("Enter the shuffle probability {0-1}: "))
        tb_data.shuffle_probability = shuffle_probability
    else:
        std_options(option)


# Genetic Algorithm menu
# Define the values for the parameters of the genetic algorithm or run genetic algorithm
def run_genetic_algorithm():
    global ga_data, current_solution, current_cost, delivery_schedule
    
    delivery_schedule_info = (delivery_schedule, current_solution, current_cost)
    option = genetic_algorithm_menu(delivery_schedule_info, ga_data)

    if option == 1: # Run genetic algorithm
        initial_time = time.time()
        solution, best_costs, best_solution_generation = ga_data.run(delivery_schedule)
        execution_time = time.time() - initial_time
        
        cost = delivery_schedule.total_cost(solution)

        register_in_history({
            "algorithm": "Genetic Algorithm",
            "delivery_schedule": copy.deepcopy(delivery_schedule),
            "algorithm_data": copy.deepcopy(ga_data),
            "initial_solution": copy.deepcopy(current_solution),
            "initial_cost": current_cost,
            "final_solution": copy.deepcopy(solution),
            "final_cost": cost,
            "time": round(execution_time, 3),
            "improvement": round(-(cost - current_cost), 3),
            "improvement_percentage": round((cost - current_cost) / current_cost * 100, 3),
            "plot": (best_costs, best_solution_generation)
        })

        # Display the results
        print_results(current_solution, current_cost, execution_time, solution, cost)
        print(f"Best solution found in generation: {best_solution_generation}\n")

        # Plot the results
        plot_ga(best_costs, best_solution_generation, ga_data)
        
        # Ask the user if they want to keep the new solution as the current solution
        keep = input("Keep new solution? (Y/N): ")
        if keep == "Y" or keep == "y":
            update_results(solution, cost)
    elif option == 2: # Change the map size
        ga_data.tournament_size = int(input("Enter the tournament size: "))
    elif option == 3: # Change the population size
        ga_data.population_size = int(input("Enter the population size: "))
    elif option == 4: # Change the number of iterations
        ga_data.num_iterations = int(input("Enter the number of iterations: "))
    elif option == 5: # Change the mutation probability
        mutation_prob = -1
        while mutation_prob < 0 or mutation_prob > 1:
            mutation_prob = float(input("Enter the mutation probability {0-1}: "))
        ga_data.mutation_prob = mutation_prob
    elif option == 6: # Change the number of offsprings
        ga_data.num_of_offsprings = int(input("Enter the number of offsprings: "))
    elif option == 7: # Change the population evolution strategy
        print("1 - Replace individuals with offsprings")
        print("2 - Add offsprings to the population")
        strategy = 0
        while strategy != 1 and strategy != 2:
            strategy = int(input("Select the population evolution strategy {1 or 2}: "))
        ga_data.replace_with_offspring = strategy == 1
    elif option == 8: # Change the replacement strategy
        print("1 - Replace random individual")
        print("2 - Replace least fittest individual")
        strategy = 0
        while strategy != 1 and strategy != 2:
            strategy = int(input("Select the replacement strategy {1 or 2}: "))
        ga_data.replace_random = strategy == 1
    else:
        std_options(option)

# Display the history of the optimization algorithms
def run_history():
    global delivery_schedule, current_solution, current_cost
    option = history_menu(get_num_history_entries())

    if option == 1: 
        while(True):
            clear_screen()
            print_history()
            options = ['q']
            if not empty_history():
                current_entry = get_current_entry() + 1
                print(f"Type \'g\' to plot the results")
                options.append('g')
                print(f"Type \'mi\' to display the map of the entry's initial solution")
                options.append('mi')
                print(f"Type \'mf\' to display the map of the entry's final solution")
                options.append('mf')
                print(f"Type \'ri\' to restore entry's problem instance and initial solution as the current ones")
                options.append('ri')
                print(f"Type \'rf\' to restore entry's problem instance and final solution as the current ones")
                options.append('rf')
                if (current_entry > 1):
                    print(f"Type \'p\' to go to previous entry ({current_entry - 1})")
                    options.append('p')
                if (current_entry < get_num_history_entries()):
                    print(f"Type \'n\' to go to next entry ({current_entry + 1})")
                    options.append('n')
                print(f"\nType \'b\' to go to the first entry")
                options.append('b')
                print(f"Type \'l\' to go to the last entry")
                options.append('l')
            print(f"Type \'q\' to exit\n")
            while (option := input("Enter an option: ")) not in options:
                print("Invalid option")
            if option == 'g':
                plot_history()
            elif option == 'mi':
                display_history_map(final_solution=False)
            elif option == 'mf':
                display_history_map(final_solution=True)
            elif option == 'ri':
                delivery_schedule, current_solution, current_cost, _, _ = current_entry_problem_instance()
                reset_entry()
                menu.pop()
                break
            elif option == 'rf':
                delivery_schedule, _, _, current_solution, current_cost = current_entry_problem_instance()
                update_results(current_solution, current_cost)
                reset_entry()
                menu.pop()
                break
            elif option == 'p':
                previous_entry()
            elif option == 'n':
                next_entry()
            elif option == 'b':
                reset_entry() 
            elif option == 'l':
                last_entry()
            elif option == 'q':
                reset_entry()
                break
    elif option == 2:
        reset_entry()
        reset_history()
    elif option == 3:
        save_history_log()
    else:
        std_options(option)   

# Run the program loop
def run():
    clear_screen()
    if not menu:
        return
    elif menu[-1] == "main":
        run_main()
    elif menu[-1] == "constraints":
        run_constraints()
    elif menu[-1] == "algorithms":
        run_algorithms()
    elif menu[-1] == "hill_climbing":
        run_hill_climbing()
    elif menu[-1] == "simulated_annealing":
        run_simulated_annealing()
    elif menu[-1] == "tabu_search":
        run_tabu_search()
    elif menu[-1] == "genetic_algorithm":
        run_genetic_algorithm()
    elif menu[-1] == "history":
        run_history()
    run()

if __name__ == "__main__":
    menu.append("main")
    run()
    print_title("Program Terminated")
