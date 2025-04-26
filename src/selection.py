import random
from copy import deepcopy
from .individual import Individual

#roulette selection
def roulette_selection(population: list[Individual]):

    fitness_values = [ind.fitness() for ind in population] # get fitness values from population

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
def ranking_selection(population: list[Individual]):
    
    sorted_population = sorted(population, key=lambda ind: ind.fitness(), reverse=True)  #sort population from worst to best (by fitness)
    n = len(sorted_population) # length of ranking

    ranks = list(range(1, n + 1))  # list of range values [1, 2, 3, ...]

    total_rank_sum = sum(ranks) # sum of ranks
    probabilities = [rank / total_rank_sum for rank in ranks] # calculate probabilities for each individual

    selected_index = random.choices(range(n), weights=probabilities, k=1)[0]  # select random individual based on probabilites
    return deepcopy(sorted_population[selected_index]) # return this individual

#tournament selection
def tournament_selection(population: list[Individual], k=3): # k = 3 --> tournament with 3 competitors (recommended value for this data size)

    # randomly choose competitors (with replacement, in order to fulfill one of the principles of selection algorithms, that all individuals even the one with
    #    worst fitness have a chance higher than 0 to be selected. Without replacement, the one with lowest total fitness would always lose against its
    #        competitors, so no chance of selection. With replacement, there is a probability > 0 that the total worst individual based on fitness gets randomly
    #           choosen 3 times for the tournament, meaning it would be selected.
    competitors = [random.choice(population) for n in range(k)]
    best = max(competitors, key=lambda ind: ind.fitness()) # find competitor with highest fitness
    return deepcopy(best) # return this individual
