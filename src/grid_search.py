# grid_search.py (complete updated code)
import os
import itertools
import pandas as pd
import numpy as np
from tqdm import tqdm
from ga import GeneticAlgorithm as GA

RESULTS_PATH = "results/grid_search_results.csv"
os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)

def get_parameters():
    return {
        'pop_size': [1000],
        'generations': [300],
        'selection': ["tournament"], #"roulette", "ranking", "tournament", "stochastic", "boltzmann"
        'crossover': ["greedy_merge"], #"group_based","greedy_merge", "partially", "table_preserve"
        'mutation': [ 'one_point'], #'swap','one_point','multi_point','inversion'
        'cx_rate': [0.6],
        'mut_rate': [0.6,0.9],
        'elitism_percent': [0.1,0.05],
        'runs': [100],
        'early_stop_gens': [10],
        'delta': [50],
    }

def run_experiment(config):
    all_runs = []
    
    for run in range(config['runs']):
        ga = GA(config)
        (history, best_solution, actual_gens,
         eff_mut, total_mut, eff_cx, total_cx,
         pop_div) = ga.run()

        run_data = {
            'run': run,
            'final_fitness': float(history[-1]),
            'best_solution': str(best_solution.seating.tolist()),
            'generations': int(actual_gens),
            'fitness_history': [float(f) for f in history],
            'effective_mutations': eff_mut,
            'total_mutations': total_mut,
            'effective_crossovers': eff_cx,
            'total_crossovers': total_cx,
            'population_diversity': pop_div,
        }
        all_runs.append(run_data)

    # Calculate convergence rate (95% of max fitness)
    converged_runs = 0
    max_fitness = max(r['final_fitness'] for r in all_runs)
    threshold = 0.95 * max_fitness
    for r in all_runs:
        if any(f >= threshold for f in r['fitness_history']):
            converged_runs += 1
    convergence_rate = converged_runs / len(all_runs)

    # Calculate effective rates
    total_eff_mut = sum(r['effective_mutations'] for r in all_runs)
    total_mut = sum(r['total_mutations'] for r in all_runs)
    avg_mutation_success_rate = total_eff_mut / total_mut if total_mut > 0 else 0.0

    total_eff_cx = sum(r['effective_crossovers'] for r in all_runs)
    total_cx = sum(r['total_crossovers'] for r in all_runs)
    avg_crossover_success_rate = total_eff_cx / total_cx if total_cx > 0 else 0.0

    # Calculate average population diversity
    all_div = [d for r in all_runs for d in r['population_diversity']]
    avg_diversity = np.mean(all_div) if all_div else 0.0

    # Aggregate fitness metrics
    fitness_values = [r['final_fitness'] for r in all_runs]
    avg_fitness = np.mean(fitness_values)
    max_fitness = np.max(fitness_values)
    std_fitness = np.std(fitness_values)

    # Aggregate generation metrics
    generations = [r['generations'] for r in all_runs]
    avg_generations = np.mean(generations)
    max_generations = np.max(generations)
    std_generations = np.std(generations)

    # Prepare fitness progress
    max_len = max(len(r['fitness_history']) for r in all_runs)
    padded = [r['fitness_history'] + [r['fitness_history'][-1]]*(max_len - len(r['fitness_history'])) 
              for r in all_runs]
    avg_progress = np.mean(padded, axis=0).tolist()

    return {
        **config,
        'avg_fitness': round(avg_fitness, 2),
        'max_fitness': round(max_fitness, 2),
        'std_fitness': round(std_fitness, 2),
        'avg_generations': round(avg_generations, 2),
        'max_generations': round(max_generations, 2),
        'std_generations': round(std_generations, 2),
        'convergence_rate': round(convergence_rate, 4),
        'avg_mutation_success_rate': round(avg_mutation_success_rate, 4),
        'avg_crossover_success_rate': round(avg_crossover_success_rate, 4),
        'avg_population_diversity': round(avg_diversity, 4),
        'avg_fitness_progress': str(avg_progress),  # Rounded list
        'best_solution': all_runs[0]['best_solution']
    }

def save_results(new_results):
    # Convert new results to DataFrame
    new_df = pd.DataFrame(new_results)
    
    # Define all expected columns
    columns = [
        'pop_size', 'generations', 'selection', 'crossover', 'mutation',
        'cx_rate', 'mut_rate', 'elitism_percent', 'runs', 'early_stop_gens',
        'delta', 'avg_fitness', 'max_fitness', 'std_fitness', 'avg_generations',
        'max_generations', 'std_generations', 'convergence_rate',
        'avg_mutation_success_rate', 'avg_crossover_success_rate', 'avg_population_diversity',
        'avg_fitness_progress', 'best_solution'
    ]
    
    # Load existing data if available
    if os.path.exists(RESULTS_PATH):
        existing_df = pd.read_csv(RESULTS_PATH)
        # Add missing columns to existing data
        for col in columns:
            if col not in existing_df.columns:
                existing_df[col] = None
        # Combine data
        full_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        full_df = new_df
    
    # Ensure column order and save
    full_df = full_df[columns]
    full_df.to_csv(RESULTS_PATH, index=False)

def execute_grid_search():
    params = get_parameters()
    param_combinations = list(itertools.product(*params.values()))
    print(f"Total configurations: {len(param_combinations)}")

    for combo in tqdm(param_combinations, desc="Grid Search"):
        config = dict(zip(params.keys(), combo))
        try:
            result = run_experiment(config)
            save_results([result])
        except Exception as e:
            print(f"Error with config {config}: {str(e)}")
            continue

if __name__ == "__main__":
    execute_grid_search()