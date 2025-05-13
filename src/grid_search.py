import os
import itertools
import pandas as pd
import numpy as np
from tqdm import tqdm
from ga import GeneticAlgorithm as GA

# Results storage path
RESULTS_PATH = "results/grid_search_results.csv"
os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)

def get_parameters():
    """Generate all parameter combinations"""
    params = {
        'pop_size': [10],                                                                   # Population size
        'generations': [50],                                                                # Number of generations
        'selection': ['ranking', 'tournament', 'roulette', 'stochastic', 'boltzmann'],      # Selection methods ranking, tournament, roulette, stochastic, boltzmann
        'crossover': ['group_based', 'greedy_merge', 'partially', 'table_preserve' ],       # Crossover methods group_based, greedy_merge, partially, table_preserve 
        'mutation': [ 'swap', 'one_point', 'multi_point', 'inversion', 'table_swap'],       # Mutation methods swap, one_point, multi_point, inversion, table_swap
        'cx_rate': [0.2,0.4],                                                               # Crossover rate (0 to 1)
        'mut_rate': [0.1,0.3],                                                              # Mutation rate (0 to 1)
        'elitism_percent': [0,0.05],                                                        # Elitism percentage of pop_size (0 to 1)
        'runs': [30],                                                                       # Number of runs per configuration
        'early_stop_gens': [3],                                                             # Number of generations before early stopping
        'delta': [250],                                                                     # Fitness improvement threshold for early stopping
    }
    return params

def run_experiment(config):
    """Run experiment with enhanced metrics collection"""
    all_runs = []
    
    for run in range(config['runs']):
        ga = GA(config)
        history, best_solution, actual_gens = ga.run()

        run_data = {
            'run': run,
            'final_fitness': float(history[-1]),
            'best_solution': best_solution.seating.tolist(),
            'generations': int(actual_gens),
            'fitness_history': [float(f) for f in history]
        }
        all_runs.append(run_data)
    
    # Ensure all fitness histories have same length by padding with final value
    max_gen = max(len(r['fitness_history']) for r in all_runs)
    for r in all_runs:
        last_value = r['fitness_history'][-1]
        if len(r['fitness_history']) < max_gen:
            r['fitness_history'].extend([last_value] * (max_gen - len(r['fitness_history'])))
    
    # Now all fitness_history lists are equal length
    fitness_matrix = np.array([r['fitness_history'] for r in all_runs])  # shape: (runs, generations)
    avg_fitness_progress = fitness_matrix.mean(axis=0).tolist()

    # Aggregate other metrics
    fitness_values = [r['final_fitness'] for r in all_runs]
    generations = [r['generations'] for r in all_runs]
    
    avg_fitness = float(np.mean(fitness_values))
    max_fitness = max(fitness_values)
    avg_generations = float(np.mean(generations))
    max_generation = max(generations)
    std_fitness = float(np.std(fitness_values))
    std_generations = float(np.std(generations))

    best_solution = max(all_runs, key=lambda x: x['final_fitness'])['best_solution']
    
    return {
        **config,
        'avg_fitness': avg_fitness,
        'max_fitness': max_fitness,
        'avg_generations': avg_generations,
        'max_generations': max_generation,
        'std_fitness': std_fitness,
        'std_generations': std_generations,
        'best_solution': best_solution,
        'avg_fitness_progress': avg_fitness_progress
    }

def save_results(new_results):
    """Save results to CSV and retain top 500 combinations"""
    try:
        existing = pd.read_csv(RESULTS_PATH)
    except FileNotFoundError:
        existing = pd.DataFrame()

    new_df = pd.DataFrame(new_results)
    df = pd.concat([existing, new_df], sort=False)
    
    # Sort by average fitness and retain the top 500 configurations
    df = df.sort_values('avg_fitness', ascending=False).head(500)
    df.to_csv(RESULTS_PATH, index=False)

def execute_grid_search():
    """Execute grid search and save top results"""
    params = get_parameters()
    param_combinations = list(itertools.product(*[v for k, v in params.items()]))

    for idx, values in enumerate(tqdm(param_combinations, desc="Grid Search"), 1):
        config = dict(zip([k for k in params], values))
        print(f"\nConfiguration {idx}/{len(param_combinations)}")
        
        try:
            result = run_experiment(config)
            save_results([result])
        except Exception as e:
            print(f"Failed config {config}: {str(e)}")
            continue


if __name__ == "__main__":
    execute_grid_search()
