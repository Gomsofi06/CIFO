import random
from copy import deepcopy
from .individual import create_individual
from src.individual import create_individual
from src.fitness import evaluate_fitness

#roulette selection
def roulette_selection(population: list[create_individual]):

    fitness_values = [evaluate_fitness(ind) for ind in population] # get fitness values from population

    total_fitness = sum(fitness_values)  # calculate total fitness
    
    # Generate random number between 0 and total fitness
    random_nr = random.uniform(0, total_fitness)
    box_boundary = 0
    # For each individual check if random number is inside the individuals box
    for ind, fitness in zip(population, fitness_values):
        box_boundary += fitness
        if random_nr <= box_boundary:  # if inside, return (deepcopy) of this individual
            return deepcopy(ind)


#ranking selsction
def ranking_selection(population: list[create_individual]):
    
    sorted_population = sorted(population, key=lambda ind: evaluate_fitness(ind), reverse=True)  #sort population from worst to best (by fitness)
    n = len(sorted_population) # length of ranking

    ranks = list(range(1, n + 1))  # list of range values [1, 2, 3, ...]

    total_rank_sum = sum(ranks) # sum of ranks
    probabilities = [rank / total_rank_sum for rank in ranks] # calculate probabilities for each individual

    selected_index = random.choices(range(n), weights=probabilities, k=1)[0]  # select random individual based on probabilites
    return deepcopy(sorted_population[selected_index]) # return this individual

#tournament selection
def tournament_selection(population, k=3):
    competitors = random.sample(population, k)
    best = max(competitors, key=lambda ind: evaluate_fitness(ind)
)
    return best