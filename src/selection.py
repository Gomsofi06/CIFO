import random
import numpy as np
from individual import Individual
import bisect

def roulette_selection(population, num_selected):
    fitnesses = [indiv.fitness for indiv in population]
    total = sum(fitnesses)
    return [
        population[bisect.bisect_left(np.cumsum(fitnesses), random.uniform(0, total))]
        for _ in range(num_selected)
    ]

def ranking_selection(population, num_selected):
    ranked = sorted(population, key=lambda x: x.fitness)
    weights = np.arange(1, len(ranked)+1)
    return [ranked[i] for i in np.random.choice(len(ranked), size=num_selected, p=weights/weights.sum())]

def tournament_selection(population, num_selected, k=3):
    return [max(random.sample(population, k), key=lambda x: x.fitness) for _ in range(num_selected)]

def stochastic_universal_sampling(population, num_selected):
    fitnesses = [indiv.fitness for indiv in population]
    total = sum(fitnesses)
    interval = total / num_selected
    start = random.uniform(0, interval)
    pointers = [start + i*interval for i in range(num_selected)]
    return [population[bisect.bisect_left(np.cumsum(fitnesses), p % total)] for p in pointers]

def boltzmann_selection(population, num_selected, temp=100):
    fitnesses = np.array([indiv.fitness for indiv in population])
    
    # Handle case where all fitness values are equal
    if np.all(fitnesses == fitnesses[0]):
        return random.sample(population, num_selected)
    
    # Scale values to prevent underflow/overflow
    scaled_fitness = fitnesses - np.max(fitnesses)
    weights = np.exp(scaled_fitness / temp)
    
    # Add epsilon to avoid division by zero
    weights_sum = np.sum(weights) + 1e-10
    probabilities = weights / weights_sum
    
    # Handle any remaining numerical instability
    if np.any(np.isnan(probabilities)):
        probabilities = np.ones_like(probabilities) / len(probabilities)
    
    return [population[i] for i in np.random.choice(
        len(population), 
        size=num_selected, 
        p=probabilities
    )]