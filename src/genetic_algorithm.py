from collections import deque
import numpy as np
import random
import copy

from package import *
from solution import *

# Genetic Algorithm Data
class GeneticAlgorithmData:
    def __init__(self, tournament_size, population_size, num_iterations, mutation_prob, num_of_offsprings, replace_with_offspring, replace_random):
        self.tournament_size = tournament_size # Number of individuals that will compete in the tournament
        self.population_size = population_size # Number of individuals in the population
        self.num_iterations = num_iterations # Number of iterations the algorithm will run
        self.mutation_prob = mutation_prob # Probability of mutation
        self.num_of_offsprings = num_of_offsprings # Number of offsprings generated in each iteration
        self.replace_with_offspring = replace_with_offspring # If True, replaces individuals with offsprings. Otherwise, adds offsprings to the population
        self.replace_random = replace_random # If True, replaces a random individual. Otherwise, replaces the least fittest individual

    # String representation of the Genetic Algorithm Data
    def __str__(self):
        text = "Genetic Algorithm Parameters: \n"
        
        text += f"\nTournament size: {self.tournament_size}\nPopulation size: {self.population_size}\nNumber of iterations: {self.num_iterations}\nMutation probability: {self.mutation_prob}\nNumber of offsprings: {self.num_of_offsprings}\n"
        text += "Evolution Strategy: "
        
        if (self.replace_with_offspring):
            text += "Replace individuals with offsprings\n"
        else:
            text += "Add offsprings to the population\n"
        
        text += "Replacement Strategy: "
        if (self.replace_random):
            text += "Replace random individual"
        else:
            text += "Replace least fittest individual"
        
        return text
            
    # Generates the initial population by generating a package stream and creating random solutions
    def generate_population(self, delivery_schedule):
        packages = delivery_schedule.packages 
        population = [packages]

        for _ in range(self.population_size - 1):
            individual = random.sample(packages, len(packages)) 
            population.append(individual)

        return population
    
    # Crossover operator
    ## Builds a child solution by selecting genes from one of the parents with equal probability
    def crossover(self, solution1, solution2):
        child = deque()
        i = 0
        s1 = 0
        s2 = 0

        while (i < len(solution1)):
            rand = np.random.randint(1, 3) # Randomly selects a parent to get the gene from
            if (rand == 1):
                while (solution1[s1] in child): # Ensures that the gene is not already in the child
                    s1 += 1
                child.append(solution1[s1])
                s1 += 1 # Moves to the next gene in the parent
            else:
                while (solution2[s2] in child): # Ensures that the gene is not already in the child
                    s2 += 1
                child.append(solution2[s2])
                s2 += 1 # Moves to the next gene in the parent
            
            i += 1

        return list(child)

    # Mutation operator
    ## Swaps a random pair of contiguous genes with a probability of mutation_prob
    def mutate_solution(self, solution):
        mutant_solution = copy.deepcopy(solution)

        gene = random.randint(0, len(solution) // 2 - 1) # Randomly selects a gene to mutate

        rand = np.random.random() 
        if (rand < self.mutation_prob):
            mutant_solution[2*gene], mutant_solution[2*gene + 1] = solution[2*gene + 1], solution[2*gene]

        return mutant_solution

    # Tournament selection
    ## Selects the best solution from a random sample of the population with size tournament_size
    def tournament_select(self,delivery_schedule, population):
        participants = random.sample(range(self.population_size), self.tournament_size) # Randomly selects participants

        best_solution = population[participants[0]]
        
        for participant in participants:
            if (evaluate_solution(delivery_schedule, population[participant]) > evaluate_solution(delivery_schedule, best_solution)):
                best_solution = population[participant]
        
        return best_solution

    # Returns the solution with the highest score
    def get_greatest_fit(self, delivery_schedule, population):
        best_solution = population[0]
        best_score = evaluate_solution(delivery_schedule, population[0])
        
        for i in range(1, len(population)):
            score = evaluate_solution(delivery_schedule, population[i])
            if score > best_score:
                best_score = score
                best_solution = population[i]
       
        return best_solution, best_score

    # Replaces the least fittest individual with the offspring
    def replace_least_fittest(self, delivery_schedule, population, offspring):
        least_fittest_index = 0 
        least_fittest_value = evaluate_solution(delivery_schedule, population[0])
        
        for i in range(1, self.population_size):
            score = evaluate_solution(delivery_schedule, population[i])
            if score < least_fittest_value:
                least_fittest_value = score
                least_fittest_index = i
        
        population[least_fittest_index] = offspring

        return population
    
    # Replaces a random individual with the offspring
    def replace_random_individual(self, population, offspring):
        rand_index = np.random.randint(0, self.population_size)

        population[rand_index] = offspring

        return population

    # Roulette selection
    ## Selects an individual from the population with probability proportional to its fitness
    def roulette_select(self, delivery_schedule, population):
        total = sum([evaluate_solution(delivery_schedule, x) for x in population]) # Total fitness of the population
        distribution = [evaluate_solution(delivery_schedule, x)/total for x in population] # Probability distribution of the population
        
        rand = random.random()
        cumulative_prob = 0 
        
        for i, prob in enumerate(distribution): # Selects an individual based on the probability distribution
            cumulative_prob += prob
            if rand <= cumulative_prob:
                return population[i]
        
        return population[self.population_size - 1]
    
    # Runs the genetic algorithm
    def run(self, delivery_schedule, log=False):
        return genetic_algorithm(delivery_schedule, self, log)

# Genetic Algorithm
def genetic_algorithm(delivery_schedule, genetic_algorithm_data, log=False):
    population = genetic_algorithm_data.generate_population(delivery_schedule) # Generates the initial population

    best_solution, best_score = genetic_algorithm_data.get_greatest_fit(delivery_schedule, population) # Gets the best solution and its score
    
    best_costs = deque([])
    best_costs.append(-best_score)

    generation_no = 0
    best_solution_generation = 0

    num_iterations = genetic_algorithm_data.num_iterations

    while(num_iterations > 0):

        generation_no += 1
        
        num_offsprings = genetic_algorithm_data.num_of_offsprings

        while (num_offsprings > 0):
            tournment_winner_sol = genetic_algorithm_data.tournament_select(delivery_schedule, population) # Selects the fittest individual from the tournament
            roulette_winner_sol = genetic_algorithm_data.roulette_select(delivery_schedule, population) # Selects an individual from the population with probability proportional to its fitness

            child = genetic_algorithm_data.crossover(tournment_winner_sol, roulette_winner_sol) # Generates a child solution by crossover
            child = genetic_algorithm_data.mutate_solution(child) # Mutates the child solution

            if (genetic_algorithm_data.replace_with_offspring):  
                if (genetic_algorithm_data.replace_random):
                    population = genetic_algorithm_data.replace_random_individual(population, child) # Replaces a random individual with the offspring
                
                else:
                    population = genetic_algorithm_data.replace_least_fittest(delivery_schedule, population, child) # Replaces the least fittest individual with the offspring
 
            else:
                population.append(child) # Adds the offspring to the population

            num_offsprings -= 1

        greatest_fit, greatest_fit_score = genetic_algorithm_data.get_greatest_fit(delivery_schedule, population) # Gets the best solution and its score
        
        if greatest_fit_score > best_score: # Updates the best solution if a better solution is found
            best_solution = greatest_fit
            best_score = greatest_fit_score
            best_solution_generation = generation_no

            if log:
                print(f"Current generation: {generation_no}")
                print(f"Current solution: {best_solution}")
                print(f"Current score: {best_score}\n")
            
        num_iterations -= 1

        best_costs.append(-best_score)

    return best_solution, best_costs, best_solution_generation
