# PROJ1-IA-2324

## Topic and Theme

Metaheuristics for Optimization/Decision Problems - Delivery Schedule

## Group Members

| Name | Student Number | Email |
| --- | --- | --- |
| [João Ramos](https://github.com/jfoliveiraramos) | 202108743 | up202108743@up.pt |
| [Marco Costa](https://github.com/SpardaMarco) | 202108821 | up202108821@up.pt |
| [Tiago Viana](https://github.com/tiagofcviana) | 201807126 | up201807126@up.pt |

## Usage

We used python 3.10.12 to develop this project.
In order to install the required dependencies, you can run the following command:

```bash
pip install -r requirements.txt
```

If you have installed python and all the needed packages on your machine, you can run the project by moving to its root directory and following the steps below:

- For Ubuntu users:
```bash
python3 src/__main__.py
```

- For Windows users:
```bash
python .\src\__main__.py
```

**Note:** Use `python` or `python3` depending on your python alias.

## Neighbourhood Functions

The neighbourhood functions implemented in this project are the following:
- **NF1** - Swaps two contiguous random packages in the driver's path.
- **NF2** - Swaps two random packages in the driver's path.
- **NF3** - Pick any of the neighbour functions above at random.

## Menu explained

Each menu is divided into two parts: one for the problem constraints and the current solution information, and other for the options of the current menu.
The **Main menu** allows the user to choose between the following options:
- Change Problem Constraints
- Go to the Algorithms menu
- Display information about each package
- Generate a new package list
- Shuffle the current package list
- Display the current solution in a map, showing the path and order of the deliveries
- Go to the Results History menu

In the problem **Constraints menu**, the user can change the following settings:
- Number of Packages *(default: 50)*
- Map Size *(default: 10)*
- Cost per km travelled *(default: 1)*
- Cost per minute of delay *(default: 1)*
- Travelling weight for the evaluation function *(default: 1)*
- Damage weight for the evaluation function *(default: 1)*
- Delay weight for the evaluation function *(default: 1)*
- Driver's speed (in km/h) *(default: 60)*
- Delivery delay for each package delivered (in minutes) *(default: 0)*

In the Algorithm menu, the user can choose between the following algorithms:
- Hill Climbing
- Simulated Annealing
- Tabu Search
- Genetic Algorithm

Each of this algorithms has its own set of parameters that can be changed by the user, in their respective menus.

In the **Hill Climbing** Algorithm menu, the user can change the following settings:
- **Acceptance Criterion** *(default: First Accept)* - The acceptance criterion used by the algorithm, where First Accept accepts the first neighbour that is better than the current solution, and Best Accept accepts the best neighbour found.
- **Neighbourhood Function** *(default: NF3)* - The neighbourhood function used by the algorithm.
- **Number of Iterations** *(default: 1000)* - The number of iterations the algorithm will run.

In the **Simulated Annealing** Algorithm menu, the user can change the following settings:
- **Starting Temperature** *(default: 1000)* - The starting temperature of the algorithm.
- **Cooling Rate** *(default: 0.99)* - The cooling rate of the algorithm.
- **Number of Iterations until Temperature Decrease** *(default: 2)* - The number of iterations until the temperature decreases.
- **Neighbourhood Function** *(default: NF3)* - The neighbourhood function used by the algorithm.
- **Number of Iterations** *(default: 1000)* - The number of iterations the algorithm will run.

In the **Tabu Search** Algorithm menu, the user can change the following settings:
- **Starting Tabu Tenure** *(default: 7)* - The starting tabu tenure of the algorithm.
- **Tenure Mode** *(default: Iteration-based)* - The mode used to update the tabu tenure.
- **Tenure Parameter** *(default: 0.3)* - The parameter used to update the tabu tenure, when the mode uses it.
- **Tabu Criteria** *(default: Solution)* - The criteria used to update the tabu list.
- **Number of Iterations** *(default: 50)* - The number of iterations the algorithm will run.
- **Neighbourhood Function** *(default: NF3)* - The neighbourhood function used by the algorithm.
- **Shuffle Probability** *(default: 0.1)* - The probability of shuffling the current solution in the Tabu Search algorithm.

In the **Genetic Algorithm** menu, the user can change the following settings:
- **Tournament Size** *(default: 10)* - Number of individuals that will compete in the tournament.
- **Population Size** *(default: 100)* - Number of individuals in the population.
- **Number of Iterations** *(default: 150)* - Number of iterations the algorithm will run.
- **Mutation Probability** *(default: 0.5)* - Probability of mutation.
- **Number of Offspring** *(default: 25)* - Number of offspring generated in each iteration.
- **Evolution Strategy** *(default: Replace)* - The evolution strategy used by the algorithm.
- **Replacement Strategy** *(default: Least Fittest)* - The replacement strategy used by the algorithm when the evolution strategy is set to Replace.

In the **Results History** menu, the user can see the history of the results of the algorithms that have been run, and the best solution found by each algorithm, as well as saving the results to a file.

This menu also provides a way to go back to a previous instance of the problem, by selecting the desired solution from the history.