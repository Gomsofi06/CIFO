import random
import numpy as np
from individual import Individual  # importante para verificar o tipo

def extract_seating(parent):
    if isinstance(parent, Individual):
        return parent.seating
    elif isinstance(parent, tuple):
        parent = parent[0]
    return parent

def group_based_crossover(parent1, parent2):
    seating1 = extract_seating(parent1)
    seating2 = extract_seating(parent2)

    # Junta todos os convidados dos dois pais, mantendo a ordem aleatória
    guests = [guest for table in (seating1 + seating2) for guest in table]
    random.shuffle(guests)

    # Remove duplicados mantendo a ordem
    seen = set()
    unique_guests = []
    for guest in guests:
        if guest not in seen:
            seen.add(guest)
            unique_guests.append(guest)

    assert len(unique_guests) == 64, "Erro: número de convidados únicos incorreto!"

    # Divide em 8 mesas de 8
    child = [unique_guests[i * 8:(i + 1) * 8] for i in range(8)]
    return child, child.copy()



def greedy_table_merge_crossover(parent1, parent2):
    seating1 = extract_seating(parent1)
    seating2 = extract_seating(parent2)

    # Junta todas as mesas
    tables = seating1 + seating2
    random.shuffle(tables)

    used = set()
    unique_guests = []

    for table in tables:
        for guest in table:
            if guest not in used:
                used.add(guest)
                unique_guests.append(guest)

    assert len(unique_guests) == 64, "Erro: número de convidados únicos incorreto!"

    # Divide em 8 mesas de 8
    child = [unique_guests[i * 8:(i + 1) * 8] for i in range(8)]
    return child, child.copy()
