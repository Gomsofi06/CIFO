from individual import Individual
from selection import roulette_selection, ranking_selection, tournament_selection
from crossover import group_based_crossover, greedy_table_merge_crossover
from mutation import swap_mutation, one_point_mutation, multiple_point_mutation
from copy import deepcopy
import random

selection_methods = {
    "roulette": roulette_selection,
    "ranking": ranking_selection,
    "tournament": tournament_selection
}

crossover_methods = {
    "group": group_based_crossover,
    "merge": greedy_table_merge_crossover
}

mutation_methods = {
    "swap": swap_mutation,
    "one_point": one_point_mutation,
    "multiple_point": multiple_point_mutation
}

def run_ga(pop_size=100, generations=200, elite_size=1, use_elitism=True,
           selection_type="tournament", crossover_type="group", mutation_type="swap",
           mutation_prob=0.2, verbose=True, seed=None):
    
    if seed is not None:
        random.seed(seed)

    select = selection_methods[selection_type]
    crossover = crossover_methods[crossover_type]
    mutate = mutation_methods[mutation_type]

    population = [Individual() for _ in range(pop_size)]

    best_fitness_per_gen = []
    avg_fitness_per_gen = []

    for gen in range(generations):
        scored_pop = [(ind, ind.fitness()) for ind in population]
        scored_pop.sort(key=lambda x: x[1], reverse=True)

        if verbose and gen % 10 == 0:
            print(f"Geração {gen} | Best fitness: {scored_pop[0][1]:.2f}")

        best_fitness_per_gen.append(scored_pop[0][1])
        avg_fitness_per_gen.append(sum(score for _, score in scored_pop) / pop_size)

        new_population = []
        if use_elitism:
            elites = [ind for ind, _ in scored_pop[:elite_size]]
            new_population.extend(elites)

        individuals_only = [ind for ind, _ in scored_pop]

        while len(new_population) < pop_size:
            parent1 = select(individuals_only)
            parent2 = select(individuals_only)
            
            child1_seating, child2_seating = crossover(parent1, parent2)

            if mutation_type == "multiple_point":
                child1 = Individual(seating=mutate(child1_seating, num_mutations=5))
                child2 = Individual(seating=mutate(child2_seating, num_mutations=5))
            else:
                child1 = Individual(seating=mutate(child1_seating, mutation_prob))
                child2 = Individual(seating=mutate(child2_seating, mutation_prob))
            new_population.extend([child1, child2])

        population = new_population[:pop_size]

    final_scored = [(ind, ind.fitness()) for ind in population]
    final_scored.sort(key=lambda x: x[1], reverse=True)
    best_solution, best_score = final_scored[0]

    return best_solution, best_score, best_fitness_per_gen
