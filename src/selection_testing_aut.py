import random
from copy import deepcopy
from individual import Individual
from selection import roulette_selection, ranking_selection, tournament_selection

# create population of individuals
def generate_population(n=20):
    return [Individual() for _ in range(n)]

# validate structure
def validate_seating(individual):
    seating = individual.seating
    guests = [g for t in seating for g in t]
    assert len(seating) == 8, "should be 8 tables"
    assert all(len(t) == 8 for t in seating), "each table should have 8 guests"
    assert len(guests) == 64, "total of guests should be 64"
    assert len(set(guests)) == 64, "repeated guests"

# === TESTS ===

def test_roulette_selection():
    population = generate_population()
    selected = roulette_selection(population)
    validate_seating(selected)

def test_ranking_selection():
    population = generate_population()
    selected = ranking_selection(population)
    validate_seating(selected)

def test_tournament_selection():
    population = generate_population()
    selected = tournament_selection(population, k=5)
    validate_seating(selected)

if __name__ == "__main__":
    test_roulette_selection()
    test_ranking_selection()
    test_tournament_selection()
    print("all tests worked succesfully")