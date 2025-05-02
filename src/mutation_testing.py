from individual import Individual
from mutation import swap_mutation, one_point_mutation, multiple_point_mutation, build_guest_to_table_map

def print_seating(seating, title="Seating"):
    print(f"\n{title}:")
    for i, table in enumerate(seating):
        print(f"Table {i + 1}: {table}")

def print_swapped_guests(before, after):
    print("\nDetected Guest Swaps:")

    guest_to_table_before = build_guest_to_table_map(before)
    guest_to_table_after = build_guest_to_table_map(after)

    moved = []
    for guest in range(64):
        from_table = guest_to_table_before[guest]
        to_table = guest_to_table_after[guest]
        if from_table != to_table:
            moved.append((guest, from_table, to_table))

    used = set()
    swap_count = 0
    for guest_a, from_a, to_a in moved:
        if guest_a in used:
            continue
        for guest_b, from_b, to_b in moved:
            if guest_b == guest_a or guest_b in used:
                continue
            if from_b == to_a and to_b == from_a:
                print(f"Guest {guest_a} swapped with Guest {guest_b} : Table {from_a + 1} ↔ Table {to_a + 1}")
                used.add(guest_a)
                used.add(guest_b)
                swap_count += 1
                break

    if swap_count == 0:
        print("No clean swaps detected.")

def test_mutations():
    original_individual = Individual()
    initial_seating = original_individual.seating
    print_seating(initial_seating, "Initial Seating")

    # === SWAP MUTATION ===
    pm = 0.1
    swap_mutated = Individual(seating=swap_mutation(initial_seating, pm))
    print_seating(swap_mutated.seating, "Swap Mutated Seating")
    print_swapped_guests(initial_seating, swap_mutated.seating)

    # === ONE-POINT MUTATION ===
    one_point_mutated = Individual(seating=one_point_mutation(initial_seating))
    print_seating(one_point_mutated.seating, "One-Point Mutated Seating")
    print_swapped_guests(initial_seating, one_point_mutated.seating)

    # === MULTI-POINT MUTATION ===
    num_mutations = 5
    multi_point_mutated = Individual(seating=multiple_point_mutation(initial_seating, num_mutations))
    print_seating(multi_point_mutated.seating, f"Multi-Point Mutated Seating (Swaps: {num_mutations})")
    print_swapped_guests(initial_seating, multi_point_mutated.seating)
