import random
import numpy as np
from individual import Individual
from itertools import chain
from fitness import calculate_table_score

def group_based_crossover(p1, p2):
    combined = np.concatenate((p1.seating.flatten(), p2.seating.flatten()))
    np.random.shuffle(combined)
    seen = set()
    unique = [x for x in combined if x not in seen and not seen.add(x)]
    child = np.array(unique[:64]).reshape(8, 8)  # Convert to numpy array
    return Individual(child), Individual(child.copy())

def greedy_table_merge_crossover(p1, p2):
    # Combine and shuffle tables from both parents
    all_tables = np.vstack((p1.seating, p2.seating))
    np.random.shuffle(all_tables)
    
    # Track used guests
    used = set()
    child_tables = []
    
    # Phase 1: Build tables from non-overlapping guests
    for table in all_tables:
        if len(child_tables) >= 8:
            break
        new_table = [g for g in table if g not in used]
        if len(new_table) >= 8:
            child_tables.append(new_table[:8])
            used.update(new_table[:8])
        elif 0 < len(new_table) < 8:
            available_slots = 8 - len(new_table)
            child_tables.append(new_table + [-1]*available_slots)
            used.update(new_table)
    
    # Phase 2: Fill remaining guests systematically
    missing = list(set(range(64)) - used)
    np.random.shuffle(missing)
    
    # Create final seating
    final = np.empty((8, 8), dtype=int)
    for ti in range(8):
        if ti < len(child_tables):
            table = child_tables[ti]
            # Replace placeholder -1 with actual guests
            final[ti] = [g if g != -1 else missing.pop() for g in table][:8]
        else:
            final[ti] = missing[:8]
            missing = missing[8:]
    
    # Validate before returning
    assert len(np.unique(final)) == 64, "Crossover produced invalid individual"
    return Individual(final), Individual(final.copy())

def partially_mapped_crossover(p1, p2):
    # Flatten parent arrays
    parent1 = p1.seating.flatten()
    parent2 = p2.seating.flatten()
    
    # Select crossover points
    cx1, cx2 = sorted(random.sample(range(64), 2))
    
    # Initialize children with -1
    child1 = np.full(64, -1, dtype=int)
    child2 = np.full(64, -1, dtype=int)
    
    # Copy crossover segment
    child1[cx1:cx2] = parent2[cx1:cx2]
    child2[cx1:cx2] = parent1[cx1:cx2]
    
    # Create mapping relations
    mapping1 = {}
    mapping2 = {}
    for i in range(cx1, cx2):
        mapping1[parent2[i]] = parent1[i]
        mapping2[parent1[i]] = parent2[i]
    
    # Fill remaining positions
    for i in chain(range(cx1), range(cx2, 64)):
        # Child1
        value = parent1[i]
        while value in child1[cx1:cx2]:
            value = mapping1[value]
        child1[i] = value
        
        # Child2
        value = parent2[i]
        while value in child2[cx1:cx2]:
            value = mapping2[value]
        child2[i] = value
    
    # Reshape and validate
    return (
        Individual(child1.reshape(8, 8)),
        Individual(child2.reshape(8, 8))
    )

def table_preservation_crossover(p1, p2):
    # Combine and shuffle tables from both parents
    all_tables = np.vstack((p1.seating, p2.seating))
    np.random.shuffle(all_tables)  # Remove positional bias
    
    # Score tables using actual fitness contribution (replace with your metric)
    scores = np.array([calculate_table_score(table) for table in all_tables])
    
    # Select best tables without duplicates
    selected_tables = []
    used_guests = set()
    
    # Greedy selection of top tables
    for idx in scores.argsort()[::-1]:
        table = all_tables[idx]
        table_guests = set(table)
        
        if len(table_guests - used_guests) == 8:  # Full table available
            selected_tables.append(table)
            used_guests.update(table_guests)
            if len(selected_tables) == 8:
                break
    
    # Handle remaining seats with missing guests
    missing = list(set(range(64)) - used_guests)
    np.random.shuffle(missing)
    
    # Build complete seating
    child_seating = np.zeros((8, 8), dtype=int)
    table_idx = 0
    
    # Add preserved tables
    for table in selected_tables:
        child_seating[table_idx] = table
        table_idx += 1
    
    # Fill remaining tables
    while table_idx < 8:
        child_seating[table_idx] = missing[:8]
        missing = missing[8:]
        table_idx += 1
    
    # Validate and return
    assert len(np.unique(child_seating)) == 64, "Invalid table preservation"
    return Individual(child_seating), Individual(child_seating.copy())
