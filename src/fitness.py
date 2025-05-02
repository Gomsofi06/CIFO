# Wrapper para compatibilidade com GA
from utils import load_relationship_matrix

csv_path = "../data/seating_data.csv"
relationship_matrix = load_relationship_matrix(csv_path) # From utils


# Calcula o score de cada uma das mesas
def calculate_table_score(table, relationship_matrix):
    score = 0
    
    for i in range(len(table)):
        for j in range(i + 1, len(table)):
            a, b = table[i], table[j]
            score += relationship_matrix[a][b]
    
    return score


# Calcula o score total das mesas
def calculate_total_fitness(seating, relationship_matrix):
    total = 0
    
    for table in seating:
        total += calculate_table_score(table, relationship_matrix)
    
    return total
