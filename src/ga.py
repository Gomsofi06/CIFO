# src/grid_search.py
import os
import itertools
import random
from tqdm import tqdm
from .individual import Individual
from .selection import tournament_selection, ranking_selection, roulette_selection
from .crossover import group_based_crossover, greedy_table_merge_crossover
from .mutation import swap_mutation, one_point_mutation, multiple_point_mutation
from .utils import load_relationship_matrix

# Load relationship matrix once
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "seating_data.csv")
relationship_matrix = load_relationship_matrix(csv_path)

# Grid search configuration
PARAM_GRID = {
    'pop_size': [50, 100],          # Population sizes to try
    'num_gens': [100, 150],         # Increased generation counts
    'sel_method': [0, 1, 2],        # 0=tournament, 1=ranking, 2=roulette
    'cx_method': [0, 1],            # 0=group-based, 1=greedy
    'mut_type': [0, 1, 2],          # 0=swap, 1=one-point, 2=multi-point
    'mut_rate': [0.1, 0.2],         # Higher mutation probabilities
    'elitism': [2, 5]               # Added elitism parameter
}

def run_genetic_algorithm(params):
    """Run GA with specified parameters and return best fitness"""
    # Parameter decoding
    selection_map = {
        0: lambda pop: tournament_selection(pop, k=3),
        1: ranking_selection,
        2: roulette_selection
    }
    crossover_map = {
        0: group_based_crossover,
        1: lambda p1, p2: greedy_table_merge_crossover(p1, p2, relationship_matrix)
    }
    
    # Initialize population
    population = [Individual() for _ in range(params['pop_size'])]
    best_fitness = -float('inf')
    stagnation_counter = 0
    prev_best = None

    for gen in range(params['num_gens']):
        # Sort and track progress
        population.sort(key=lambda x: x.fitness(), reverse=True)
        current_best = population[0].fitness()
        
        # Stagnation detection
        if prev_best is not None and current_best <= prev_best:
            stagnation_counter += 1
            if stagnation_counter > 10:  # Reset if no improvement for 10 gens
                population = population[:params['elitism']] + \
                            [Individual() for _ in range(params['pop_size'] - params['elitism'])]
                stagnation_counter = 0
        else:
            stagnation_counter = 0
        prev_best = current_best

        # Selection
        parents = [
            selection_map[params['sel_method']](population)
            for _ in range(params['pop_size'])
        ]

        # Crossover
        offspring = []
        for i in range(0, len(parents), 2):
            if i+1 >= len(parents):
                break  # Handle odd number of parents
            p1, p2 = parents[i], parents[i+1]
            c1, c2 = crossover_map[params['cx_method']](p1.seating, p2.seating)
            offspring.extend([Individual(c1), Individual(c2)])

        # Mutation with adaptive rate
        effective_mut_rate = params['mut_rate'] * (1 + stagnation_counter/10)
        for ind in offspring:
            if random.random() < effective_mut_rate:
                if params['mut_type'] == 0:
                    ind.seating = swap_mutation(ind.seating, pm=0.1)
                elif params['mut_type'] == 1:
                    ind.seating = one_point_mutation(ind.seating)
                else:
                    ind.seating = multiple_point_mutation(ind.seating, 3)

        # Elitism-preserving replacement
        combined = population[:params['elitism']] + offspring
        combined.sort(key=lambda x: x.fitness(), reverse=True)
        population = combined[:params['pop_size']]
        
        best_fitness = max(best_fitness, current_best)

    return best_fitness

def grid_search():
    """Execute grid search over parameter combinations"""
    param_combinations = [
        dict(zip(PARAM_GRID.keys(), values)) 
        for values in itertools.product(*PARAM_GRID.values())
    ]

    results = []
    
    for params in tqdm(param_combinations, desc="Grid Search Progress"):
        try:
            best = run_genetic_algorithm(params)
            results.append((params, best))
        except Exception as e:
            print(f"Error with {params}: {str(e)}")
    
    # Sort and show top results
    results.sort(key=lambda x: x[1], reverse=True)
    print("\nTop 5 Configurations:")
    for i, (params, score) in enumerate(results[:5]):
        print(f"{i+1}. Score: {score}")
        print(f"   Parameters: {params}\n")

grid_search()