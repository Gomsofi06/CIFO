import random
import copy

# HELPER FUNCTION (build a lookup dictionary: guest → table index)
def build_guest_to_table_map(seating):
    guest_to_table = {}
    for table_index, table in enumerate(seating):
        for guest in table:
            guest_to_table[guest] = table_index
    return guest_to_table


# STANDARD MUTATION
def swap_mutation(seating, pm):
    mutated = copy.deepcopy(seating)
    guest_to_table = {}

    # Mapeia cada convidado para a mesa onde está
    for table_idx, table in enumerate(mutated):
        for guest in table:
            guest_to_table[guest] = table_idx

    for guest in range(64):
        if guest not in guest_to_table:
            continue  # Ignora se o convidado não estiver atribuído a nenhuma mesa
        if random.random() < pm:
            current_table = guest_to_table[guest]

            # Escolhe uma mesa diferente com convidados
            non_empty_tables = [i for i, table in enumerate(mutated) if len(table) > 0 and i != current_table]
            if not non_empty_tables:
                continue  # ignora a mutação se não houver mesas válidas

            other_table = random.choice(non_empty_tables)
            other_guest = random.choice(mutated[other_table])

            i = mutated[current_table].index(guest)
            j = mutated[other_table].index(other_guest)

            # Faz a troca
            mutated[current_table][i], mutated[other_table][j] = other_guest, guest

            guest_to_table[guest] = other_table
            guest_to_table[other_guest] = current_table

    return mutated




# ONE-POINT MUTATION (BIT FLIP)

def one_point_mutation(seating, mutation_prob):

    # Deep copy the original seating
    mutated = copy.deepcopy(seating)

    # Create a guest-to-table lookup (key: guest, value:table )
    guest_to_table = build_guest_to_table_map(mutated)

    # Randomly select one guest
    guest_A = random.choice(list(guest_to_table.keys()))
    table_A = guest_to_table[guest_A]
  
    # Select a different table
    table_B = table_A
    while table_B == table_A:
        table_B = random.randint(0, len(mutated) - 1)

    # Select a random guest from the other table
    guest_B = random.choice(mutated[table_B])

    # Swap the two guests
    index_A = mutated[table_A].index(guest_A) # guest A position in the current table
    index_B = mutated[table_B].index(guest_B) # guest B position in the other table


    mutated[table_A][index_A], mutated[table_B][index_B] = guest_B, guest_A # swaps the guest position with the other_guest position (from the other table)

    # Update guest_to_table mapping
    guest_to_table[guest_A] = table_B
    guest_to_table[guest_B] = table_A

    return mutated


# MULTIPOINT MUTATION:

def multiple_point_mutation(seating, num_mutations):

    mutated = copy.deepcopy(seating)

    # Create a guest-to-table lookup (key: guest, value:table )
    guest_to_table = build_guest_to_table_map(mutated)

    for _ in range(num_mutations): # Loop through the number of mutations
        guest_A = random.choice(list(guest_to_table.keys()))
        table_A = guest_to_table[guest_A] # Get the guest table 
        

        # Select a different table
        table_B = table_A
        while table_B == table_A:
            table_B = random.randint(0, len(mutated) - 1)


        # Select guest from the other table
        guest_B = random.choice(mutated[table_B]) 

        # Swap their positions
        index_A = mutated[table_A].index(guest_A) # guest A position in the current table
        index_B = mutated[table_B].index(guest_B) # guest B position in the other table
        mutated[table_A][index_A], mutated[table_B][index_B] = guest_B, guest_A # swaps the guest position with the other_guest position (from the other table)

        # Update the map
        guest_to_table[guest_A] = table_B
        guest_to_table[guest_B] = table_A

    return mutated
