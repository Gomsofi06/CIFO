from individual import Individual
from crossover import group_based_crossover, greedy_table_merge_crossover
from utils import load_relationship_matrix

def print_seating(seating, title):
    print(f"\n{title}")
    for i, table in enumerate(seating):
        print(f"  Table {i+1}: {table}")
    total_guests = sum(len(table) for table in seating)
    unique_guests = len(set(guest for table in seating for guest in table))
    print(f"  Total guests: {total_guests}, Unique guests: {unique_guests}")

def validate_seating(seating) -> bool:
    guests = [guest for table in seating for guest in table]
    return (
        len(guests) == 64 and 
        len(set(guests)) == 64 and 
        all(len(table) == 8 for table in seating)
    )

def test_crossover_v1(crossover_func, relationship_matrix=None):
    print(f"\nTesting {crossover_func.__name__}")

    parent1 = Individual()
    parent2 = Individual()

    print_seating(parent1.seating, "Parent 1 Seating")
    print_seating(parent2.seating, "Parent 2 Seating")

    child1_seating, child2_seating = crossover_func(parent1, parent2)

    print_seating(child1_seating, "Child 1 Seating")
    print_seating(child2_seating, "Child 2 Seating")

    assert validate_seating(child1_seating), "Invalid child1 seating!"
    assert validate_seating(child2_seating), "Invalid child2 seating!"
    print("\n")
    print("Seating válido para ambos os filhos!\n")

def test_crossover():
    csv_path = "../data/seating_data.csv"
    relationship_matrix = load_relationship_matrix(csv_path)

    test_crossover_v1(group_based_crossover)
    test_crossover_v1(greedy_table_merge_crossover, relationship_matrix)
