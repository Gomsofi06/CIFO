import random
import numpy as np
from typing import List, Tuple
from .fitness import calculate_table_score

def group_based_crossover(
    parent1: List[List[int]], 
    parent2: List[List[int]]
) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Group-Based Crossover (Set Crossover):
    Combines entire tables from parents, avoiding duplicate guests.
    
    Args:
        parent1: First parent's seating arrangement (list of tables).
        parent2: Second parent's seating arrangement.
    
    Returns:
        Two valid child seating arrangements.
    """
    def _flatten_seating(seating):
        return [guest for table in seating for guest in table]

    # Merge and shuffle tables from both parents
    all_tables = parent1.copy() + parent2.copy()
    random.shuffle(all_tables)

    # Build a child by selecting non-conflicting tables
    def _build_child(tables):
        guests_used = set()
        child = []
        for table in tables:
            if not any(guest in guests_used for guest in table):
                child.append(table)
                guests_used.update(table)
        # Fill remaining guests randomly
        remaining_guests = list(set(range(64)) - guests_used)
        random.shuffle(remaining_guests)
        while remaining_guests:
            child.append(remaining_guests[:8])
            remaining_guests = remaining_guests[8:]
        return child[:8]  # Ensure exactly 8 tables

    child1 = _build_child(all_tables)
    child2 = _build_child(all_tables)  # Alternate strategy could be used
    return (child1, child2)

def greedy_table_merge_crossover(
    parent1: List[List[int]], 
    parent2: List[List[int]], 
    relationship_matrix: np.ndarray
) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Greedy Table Merge Crossover:
    Prioritizes tables with high internal affinity scores from parents.
    
    Args:
        parent1: First parent's seating arrangement.
        parent2: Second parent's seating arrangement.
        relationship_matrix: Preloaded 64x64 affinity matrix.
    
    Returns:
        Two valid child seating arrangements.
    """
    # Combine tables from both parents and calculate their scores
    all_tables = parent1.copy() + parent2.copy()
    table_scores = [
        (table, calculate_table_score(table, relationship_matrix))
        for table in all_tables
    ]
    # Sort tables by score (descending)
    sorted_tables = sorted(table_scores, key=lambda x: x[1], reverse=True)

    # Build a child by selecting high-score tables first
    def _build_child(sorted_tables):
        guests_used = set()
        child = []
        for table, _ in sorted_tables:
            if not any(guest in guests_used for guest in table):
                child.append(table)
                guests_used.update(table)
        # Fill remaining guests randomly
        remaining_guests = list(set(range(64)) - guests_used)
        random.shuffle(remaining_guests)
        while remaining_guests:
            child.append(remaining_guests[:8])
            remaining_guests = remaining_guests[8:]
        return child[:8]

    child1 = _build_child(sorted_tables)
    child2 = _build_child(sorted_tables)  # Could shuffle input for diversity
    return (child1, child2)