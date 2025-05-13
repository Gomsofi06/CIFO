import numpy as np
from utils import load_relationship_matrix

relationship_matrix = load_relationship_matrix()

def calculate_table_score(table):
    table = np.asarray(table).flatten().astype(int)
    return (
        np.sum(relationship_matrix[np.ix_(table, table)])
        - np.sum(np.diag(relationship_matrix[table, table]))
    )

def calculate_total_fitness(seating):
    return sum(calculate_table_score(table) for table in seating)
