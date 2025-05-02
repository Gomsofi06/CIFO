import random
import numpy as np
from individual import Individual  # importante to verify type

def extract_seating(parent):
    if isinstance(parent, Individual):
        return parent.seating
    elif isinstance(parent, tuple):
        parent = parent[0]
    return parent

def group_based_crossover(parent1, parent2):
    seating1 = extract_seating(parent1)
    seating2 = extract_seating(parent2)

    # join all guests from both parents, keeping random order
    guests = [guest for table in (seating1 + seating2) for guest in table]
    random.shuffle(guests)

    # remove duplicates keeping the order
    seen = set()
    unique_guests = []
    for guest in guests:
        if guest not in seen:
            seen.add(guest)
            unique_guests.append(guest)

    assert len(unique_guests) == 64, "Error: inccorect number of unique guests"

    # Divide in 8 tables of 8 persons
    child = [unique_guests[i * 8:(i + 1) * 8] for i in range(8)]
    return child, child.copy()



def greedy_table_merge_crossover(parent1, parent2):
    seating1 = extract_seating(parent1)
    seating2 = extract_seating(parent2)

    # join all the tables
    tables = seating1 + seating2
    random.shuffle(tables)

    used = set()
    unique_guests = []

    for table in tables:
        for guest in table:
            if guest not in used:
                used.add(guest)
                unique_guests.append(guest)

    assert len(unique_guests) == 64, "Error: incorrect number of unique guests"

    # divide in 8 tables with 8 persons
    child = [unique_guests[i * 8:(i + 1) * 8] for i in range(8)]
    return child, child.copy()
