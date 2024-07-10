import matplotlib.pyplot as plt

def plot_hc(best_costs, hc_data):
    _, ax1 = plt.subplots(figsize=(8, 8))
    ax1.margins(x=0, y=0.1)
    ax1.plot(best_costs, label="Best Solution", color="blue")
    ax1.plot([0, hc_data.num_iterations], [best_costs[-1], best_costs[-1]], linestyle=':', color='blue')
    ax1.annotate(round(best_costs[0], 2), (0, best_costs[0]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.annotate(round(best_costs[-1], 2), (0, best_costs[-1]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Cost")
    ax1.set_title("Hill Climbing")
    ax1.legend()
    plt.subplots_adjust(bottom=0.3)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, pad=1) 
    plt.annotate(text=hc_data, xy=(0.05, -0.15), xycoords='axes fraction', va="top", ha="left", fontsize=10, bbox=props)
    plt.show(block=False)

def plot_sa(costs, best_costs, temperatures, sa_data):
    _, ax1 = plt.subplots(figsize=(8, 8))
    ax1.margins(x=0, y=0.1)
    ax1.plot(costs, label="Current Solution", color="red")
    ax1.plot(best_costs, label="Best Solution", color="blue")
    ax1.plot([0, sa_data.num_iterations], [best_costs[-1], best_costs[-1]], linestyle=':', color='blue')
    ax1.annotate(round(best_costs[0], 2), (0, best_costs[0]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.annotate(round(best_costs[-1], 2), (0, best_costs[-1]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Cost")
    ax1.set_title("Simulated Annealing")
    ax2 = ax1.twinx()
    ax2.plot(temperatures, label="Temperature", color="orange")
    ax2.set_ylabel("Temperature")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    plt.subplots_adjust(bottom=0.3)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, pad=1) 
    plt.annotate(text=sa_data, xy=(0.05, -0.15), xycoords='axes fraction', va="top", ha="left", fontsize=10, bbox=props)
    plt.show(block=False)

def plot_tabu_search(costs, best_costs, tenures, tabu_search_data):
    _, ax1 = plt.subplots(figsize=(8, 8))
    ax1.margins(x=0, y=0.1)
    ax1.plot(costs, label="Current Solution", color="red")
    ax1.plot(best_costs, label="Best Solution", color="blue")
    ax1.plot([0, tabu_search_data.iteration], [best_costs[-1], best_costs[-1]], linestyle=':', color='blue')
    ax1.annotate(round(best_costs[0], 2), (0, best_costs[0]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.annotate(round(best_costs[-1], 2), (0, best_costs[-1]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Cost")
    ax1.set_title("Tabu Search")
    ax2 = ax1.twinx()
    ax2.plot(tenures, label="Tenures", color="orange")
    ax2.set_ylabel("Tenures")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    plt.subplots_adjust(bottom=0.3)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, pad=1) 
    plt.annotate(text=tabu_search_data, xy=(0.05, -0.15), xycoords='axes fraction', va="top", ha="left", fontsize=10, bbox=props)
    plt.show(block=False)

def plot_ga(best_costs, best_solution_generation, ga_data):
    _, ax1 = plt.subplots(figsize=(8, 8))
    ax1.margins(x=0, y=0.1)
    ax1.plot(best_costs, label="Best Solution", color="blue")
    ax1.plot([0, ga_data.num_iterations], [best_costs[-1], best_costs[-1]], linestyle=':', color='blue')
    ax1.annotate(round(best_costs[0], 2), (0, best_costs[0]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    ax1.annotate(round(best_costs[-1], 2), (0, best_costs[-1]), xytext=(-5, 0), textcoords="offset points", ha='right', va='center', color='blue', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
    arrowprops = dict(arrowstyle = "->", connectionstyle = "angle, angleA = 0, angleB = 90,rad = 10") 
    ax1.annotate(f"Best Solution\nGeneration: {best_solution_generation}", (best_solution_generation, best_costs[-1]), xytext=(50, 50), textcoords="offset points", ha='left', va='top', color='green',arrowprops = arrowprops)
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Cost")
    ax1.set_title("Genetic Algorithm")
    ax1.legend()
    plt.subplots_adjust(bottom=0.3)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, pad=1) 
    plt.annotate(text=ga_data, xy=(0.05, -0.15), xycoords='axes fraction', va="top", ha="left", fontsize=10, bbox=props)
    plt.show(block=False)

# Displays a map of the packages 
def display_map(packages, map_size, annotate=False, arrows=False):
    fig, ax = plt.subplots()
    padding = map_size * 0.1
    ax.set_xlim(-padding, map_size + padding)
    ax.set_ylim(-padding, map_size + padding)

    # Plot the packages
    ax.plot(0,0, 'ko', markersize=10)
    for package in packages:
        if package.package_type == 'fragile':
            ax.plot(package.coordinates_x, package.coordinates_y, 'ro', markersize=10)
        elif package.package_type == 'urgent':
            ax.plot(package.coordinates_x, package.coordinates_y, 'bo', markersize=10)
        else:
            ax.plot(package.coordinates_x, package.coordinates_y, 'go', markersize=10)

    # Plot the arrows between the packages
    if arrows:
        ax.annotate("", xy=(packages[0].coordinates_x, packages[0].coordinates_y), xytext=(0,0), arrowprops=dict(arrowstyle="->", lw=1.5, color='black'), zorder=0) 
        for i in range(1, len(packages)):
            # Take into account markersize so that the arrow does not overlap the marker
            ax.annotate("", xy=(packages[i].coordinates_x, packages[i].coordinates_y), xytext=(packages[i-1].coordinates_x, packages[i-1].coordinates_y), arrowprops=dict(arrowstyle="->", lw=1.5, color='black'), zorder=0) 
    
    # Annotate the packages
    if annotate:
        ax.annotate("origin", (0,0), textcoords="offset points", xytext=(0,-7), ha='center', va='top')
        for i in range(len(packages)):
            ax.annotate(str(i+1), (packages[i].coordinates_x, packages[i].coordinates_y), textcoords="offset points", xytext=(0,10), ha='center')

    # Legend map, showing that red is fragile, blue is urgent, and green is standard
    ax.legend(['Origin', 'Fragile', 'Urgent', 'Normal'], loc='upper right')
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('black')
    leg.legendHandles[1].set_color('red')
    leg.legendHandles[2].set_color('blue')
    leg.legendHandles[3].set_color('green')

    plt.show(block=False)
