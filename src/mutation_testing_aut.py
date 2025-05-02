import copy
from individual import Individual
from mutation import swap_mutation, one_point_mutation, multiple_point_mutation

def validate_seating(seating):
    all_guests = [guest for table in seating for guest in table]
    assert len(all_guests) == 64, "Faltam convidados"
    assert len(set(all_guests)) == 64, "Convidados repetidos"
    assert len(seating) == 8, "Número errado de mesas"
    for table in seating:
        assert len(table) == 8, "Mesa com número errado de convidados"

def test_swap_mutation():
    ind = Individual()
    mutated = swap_mutation(copy.deepcopy(ind.seating), pm=0.2)
    validate_seating(mutated)

def test_one_point_mutation():
    ind = Individual()
    mutated = one_point_mutation(copy.deepcopy(ind.seating))
    validate_seating(mutated)

def test_multiple_point_mutation():
    ind = Individual()
    mutated = multiple_point_mutation(copy.deepcopy(ind.seating), num_mutations=5)
    validate_seating(mutated)

if __name__ == "__main__":
    test_swap_mutation()
    test_one_point_mutation()
    test_multiple_point_mutation()
    print("Todos os testes passaram com sucesso!")
    
    
    
    