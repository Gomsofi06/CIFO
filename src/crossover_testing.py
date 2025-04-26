from .individual import generate_random_seating
from .crossover import group_based_crossover, greedy_table_merge_crossover
from .utils import load_relationship_matrix

def validate_seating(seating) -> bool:
    """
    Validate a seating arrangement:
    - All 64 guests are present exactly once.
    - Exactly 8 tables with 8 guests each.
    """
    guests = [guest for table in seating for guest in table]
    return (
        len(guests) == 64 and 
        len(set(guests)) == 64 and 
        all(len(table) == 8 for table in seating)
    )

def test_crossover(crossover_func, relationship_matrix=None):
    """
    Test a crossover operator.
    """
    parent1 = generate_random_seating()
    parent2 = generate_random_seating()
    
    if crossover_func == greedy_table_merge_crossover:
        child1, child2 = crossover_func(parent1, parent2, relationship_matrix)
    else:
        child1, child2 = crossover_func(parent1, parent2)
    
    assert validate_seating(child1), "Invalid child1 seating!"
    assert validate_seating(child2), "Invalid child2 seating!"
    print(f"Test passed for {crossover_func.__name__}!")

# Load relationship matrix for greedy crossover
csv_path = "data/seating_data.csv"  # Adjust path if needed
relationship_matrix = load_relationship_matrix(csv_path)

# Test both crossovers
print("Testing Group-Based Crossover...")
test_crossover(group_based_crossover)

print("\nTesting Greedy Table Merge Crossover...")
test_crossover(greedy_table_merge_crossover, relationship_matrix)