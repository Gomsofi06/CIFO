from individual import Individual
from selection import roulette_selection, ranking_selection, tournament_selection

def test_selection():
    # create population
    population = [Individual() for _ in range(10)]

    # order by fitness for visualization
    sorted_population = sorted(population, key=lambda ind: ind.fitness(), reverse=True)
    rank_map = {}
    for rank, ind in enumerate(sorted_population):
        fitness = ind.fitness()
        if fitness not in rank_map:
            rank_map[fitness] = rank + 1

    # show all individuals
    print("\n--- Population ---")
    for i, ind in enumerate(population):
        fitness = ind.fitness()
        rank = rank_map[fitness]
        print(f"Individual {i}: Fitness = {fitness:.2f} | Rank = {rank}")

    # === ROULETTE ===
    selected = roulette_selection(population)
    print("\n Selected (roulette):")
    print(selected.seating)
    print(f"Fitness: {selected.fitness():.2f} | Rank = {rank_map[selected.fitness()]}")

    # === RANKING ===
    selected = ranking_selection(population)
    print("\n Selected (ranking):")
    print(selected.seating)
    print(f"Fitness: {selected.fitness():.2f} | Rank = {rank_map[selected.fitness()]}")

    # === TOURNAMENT ===
    selected = tournament_selection(population, k=3)
    print("\n Selected (tournament):")
    print(selected.seating)
    print(f"Fitness: {selected.fitness():.2f} | Rank = {rank_map[selected.fitness()]}")
