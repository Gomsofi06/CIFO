import random
import numpy as np

def group_based_crossover(parent1, parent2):
    """Combina mesas dos pais garantindo variedade sem conflitos"""
    if isinstance(parent1, tuple):
        parent1 = parent1[0]
    if isinstance(parent2, tuple):
        parent2 = parent2[0]

    if isinstance(parent1[0], (int, np.integer)):
        raise ValueError("Esperava seating completo, mas parent1 parece ser uma mesa ou indivíduo.")

    parent1 = [list(table) for table in parent1]
    parent2 = [list(table) for table in parent2]

    all_tables = parent1 + parent2
    random.shuffle(all_tables)

    child = []
    used_guests = set()

    for table in all_tables:
        new_table = []
        for guest in table:
            if guest not in used_guests:
                new_table.append(guest)
                used_guests.add(guest)
            if len(new_table) == 8:
                break
        if len(new_table) == 8:
            child.append(new_table)
        if len(child) == 8:
            break

    return child, child.copy()

def greedy_table_merge_crossover(parent1, parent2):
    if isinstance(parent1, tuple):
        parent1 = parent1[0]
    if isinstance(parent2, tuple):
        parent2 = parent2[0]

    parent1 = [list(table) for table in parent1]
    parent2 = [list(table) for table in parent2]

    tables = parent1 + parent2
    random.shuffle(tables)

    used = set()
    child = []

    for table in tables:
        new_table = []
        for guest in table:
            if guest not in used:
                new_table.append(guest)
                used.add(guest)
            if len(new_table) == 8:
                break
        if len(new_table) == 8:
            child.append(new_table)
        if len(child) == 8:
            break

    return child, child.copy()
