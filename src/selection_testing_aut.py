import random
from copy import deepcopy
from individual import Individual
from selection import roulette_selection, ranking_selection, tournament_selection

# Gera população de indivíduos
def generate_population(n=20):
    return [Individual() for _ in range(n)]

# Validação de estrutura
def validate_seating(individual):
    seating = individual.seating
    guests = [g for t in seating for g in t]
    assert len(seating) == 8, "Deve haver 8 mesas"
    assert all(len(t) == 8 for t in seating), "Cada mesa deve ter 8 convidados"
    assert len(guests) == 64, "Total de convidados deve ser 64"
    assert len(set(guests)) == 64, "Convidados repetidos"

# === TESTES ===

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
    print("Todos os testes de seleção passaram com sucesso!")