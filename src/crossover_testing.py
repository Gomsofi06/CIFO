from individual import Individual
from crossover import group_based_crossover, greedy_table_merge_crossover
from utils import load_relationship_matrix

def validate_seating(seating) -> bool:
    guests = [guest for table in seating for guest in table]
    return (
        len(guests) == 64 and 
        len(set(guests)) == 64 and 
        all(len(table) == 8 for table in seating)
    )

def test_crossover(crossover_func, relationship_matrix=None):
    parent1 = Individual()
    parent2 = Individual()

    child1_seating, child2_seating = crossover_func(parent1, parent2)

    assert validate_seating(child1_seating), "Invalid child1 seating!"
    assert validate_seating(child2_seating), "Invalid child2 seating!"
    print(f"✅ Test passed for {crossover_func.__name__}!")

csv_path = "../data/seating_data.csv"
relationship_matrix = load_relationship_matrix(csv_path)

print("Testing Group-Based Crossover...")
test_crossover(group_based_crossover)

print("\nTesting Greedy Table Merge Crossover...")
test_crossover(greedy_table_merge_crossover, relationship_matrix)