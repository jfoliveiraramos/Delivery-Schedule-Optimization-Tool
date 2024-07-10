from menu import print_title, print_results, print_line
from plot import *
import os
import copy

history = []
current_entry = 0
file_index = 0

def entry_to_string(index):
    entry = history[index]
    result = ""
    result += f"Entry {index + 1}\n\n"
    result += entry["delivery_schedule"].__str__() + "\n"
    result += f"Algorithm: {entry['algorithm']}\n\n"
    result += entry["algorithm_data"].__str__() + "\n"
    result += f"Initial Solution: {entry['initial_solution']}\n"
    result += f"Initial Cost: {entry['initial_cost']}\n"
    result += f"Time: {entry['time']}\n"
    result += f"Final Solution: {entry['final_solution']}\n"
    result += f"Final Cost: {entry['final_cost']}\n"
    result += f"Improvement: {entry['improvement']} ({entry['improvement_percentage']}%)\n"
    result += f"{70 * '-'}\n\n"
    return result

def print_entry(index):
    entry = history[index]
    print_title(f"Entry {index + 1}")
    print(entry["delivery_schedule"])
    print(f"Algorithm: {entry['algorithm']}\n")
    print(entry["algorithm_data"])
    print_results(entry["initial_solution"], entry["initial_cost"], entry["time"], entry["final_solution"], entry["final_cost"])
    print_line()

def print_history():
    if len(history) == 0:
        print("No entries in the Results History\n")
        return
    print_entry(current_entry)

def plot_entry(index):
    entry = history[index]
    plot_data = entry["plot"]
    if entry["algorithm"] == "Hill Climbing":
        plot_hc(*plot_data, entry["algorithm_data"])
    elif entry["algorithm"] == "Simulated Annealing":
        plot_sa(*plot_data, entry["algorithm_data"])
    elif entry["algorithm"] == "Tabu Search":
        plot_tabu_search(*plot_data, entry["algorithm_data"])
    elif entry["algorithm"] == "Genetic Algorithm":
        plot_ga(*plot_data, entry["algorithm_data"])

def plot_history():
    plot_entry(current_entry)

def display_entry_map(index, final_solution=True):
    entry = history[index]
    if final_solution:
        display_map(entry["final_solution"], entry["delivery_schedule"].map_size, True, True)
    else:
        display_map(entry["initial_solution"], entry["delivery_schedule"].map_size, True, True)
    
def display_history_map(final_solution=True):
        display_entry_map(current_entry, final_solution)

def current_entry_problem_instance():
    entry = history[current_entry]
    delivery_schedule_copy = copy.deepcopy(entry["delivery_schedule"])
    initial_solution_copy = copy.deepcopy(entry["initial_solution"])
    final_solution_copy = copy.deepcopy(entry["final_solution"])
    initial_cost = entry["initial_cost"]
    final_cost = entry["final_cost"]

    return delivery_schedule_copy, initial_solution_copy, initial_cost, final_solution_copy, final_cost

def register_in_history(entry):
    history.append(entry)

def reset_history():
    global history
    history = []

def empty_history():
    return len(history) == 0

def get_current_entry():
    return current_entry

def next_entry():
    global current_entry
    current_entry += 1
    if current_entry >= len(history):
        current_entry = 0

def previous_entry():
    global current_entry
    current_entry -= 1
    if current_entry < 0:
        current_entry = len(history) - 1

def reset_entry():
    global current_entry
    current_entry = 0   

def last_entry():
    global current_entry
    current_entry = len(history) - 1

def get_num_history_entries():
    return len(history)

def save_history_log():
    global file_index
    file_index += 1
    if not os.path.exists("history_logs"):
        os.makedirs("history_logs")
    with open(f"history_logs/history_log_{file_index}.txt", "w") as file:
        for i in range(len(history)):
            file.write(entry_to_string(i))
