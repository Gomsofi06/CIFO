from src.individual import generate_random_seating
from src.utils import load_relationship_matrix
from src.fitness import calculate_total_fitness
import os
csv_path = os.path.join(os.path.dirname(__file__), "data", "seating_data.csv")

relationship_matrix = load_relationship_matrix(csv_path)

seating = generate_random_seating()

fitness = calculate_total_fitness(seating, relationship_matrix)

print(f"Fitness da solução: {fitness}")


