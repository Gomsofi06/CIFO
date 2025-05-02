from crossover import group_based_crossover, greedy_table_merge_crossover
from individual import generate_random_seating

def validate_seating(seating):
    all_guests = [g for t in seating for g in t]
    assert len(seating) == 8, "Deve haver 8 mesas"
    assert all(len(t) == 8 for t in seating), "Cada mesa deve ter 8 convidados"
    assert len(all_guests) == 64, "Total de 64 convidados esperado"
    assert len(set(all_guests)) == 64, "Convidados repetidos!"

def test_group_based_crossover():
    p1 = generate_random_seating()
    p2 = generate_random_seating()
    c1, c2 = group_based_crossover(p1, p2)
    validate_seating(c1)
    validate_seating(c2)

def test_greedy_table_merge_crossover():
    p1 = generate_random_seating()
    p2 = generate_random_seating()
    c1, c2 = greedy_table_merge_crossover(p1, p2)
    validate_seating(c1)
    validate_seating(c2)
    
if __name__ == "__main__":
    test_group_based_crossover()
    print("\nTodos os testes passaram para test_group_based_crossover!\n")
    test_greedy_table_merge_crossover()
    print("Todos os testes passaram para test_greedy_table_merge_crossover!\n")