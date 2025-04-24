from individual import Individual
from selection import roulette_selection, ranking_selection, tournament_selection

# create population with 10 random individuals (seating arrangements)
population = [Individual() for n in range(10)]

#sort population by fitness just for visualization, so easily can be seen which one was selected at the end (2nd highest, 3rd highest etc)
sorted_population = sorted(population, key=lambda ind: ind.fitness(), reverse=True)
rank_map = {}
for rank, ind in enumerate(sorted_population):
    fitness = ind.fitness()
    if fitness not in rank_map:  # take only first one with this fitness (in case of some with exact same fitness)
        rank_map[fitness] = rank + 1

# print fitness values of all individuals, and its rank
for i, ind in enumerate(population):
    fitness = ind.fitness()
    rank = rank_map[fitness]
    print(f"Individual {i}: Fitness = {fitness} | Rank = {rank}")

# Test roulette_selection
selected = roulette_selection(population)
print("\n choosen individual (roulette):")
print(selected.seating)
print(f"Fitness: {selected.fitness()} | Rank = {rank_map[selected.fitness()]}")

# Test Ranking Selection 
selected = ranking_selection(population)
print("\n choosen individual (ranking):")
print(selected.seating)
print(f"Fitness: {selected.fitness()} | Rank = {rank_map[selected.fitness()]}")

# Test tournament
selected = tournament_selection(population, k=3)
print("\n choosen individual (tournament):")
print(selected.seating)
print(f"Fitness: {selected.fitness()} | Rank = {rank_map[selected.fitness()]}")