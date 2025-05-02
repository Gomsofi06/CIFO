import random
from fitness import calculate_total_fitness
from utils import load_relationship_matrix

NUM_GUESTS = 64
NUM_TABLES = 8
GUESTS_PER_TABLE = NUM_GUESTS // NUM_TABLES

csv_path = "../data/seating_data.csv"
relationship_matrix = load_relationship_matrix(csv_path) # From utils

# create an array with random tables
# divide the final list in 8 sublists with 8 persons (tables)
def generate_random_seating():
    guests = list(range(NUM_GUESTS))
    random.shuffle(guests)
    seating = []
    
    for i in range(0, NUM_GUESTS, NUM_TABLES):
        seating.append(guests[i:i+NUM_TABLES])
    
    return seating


# create class Individual with init() and fitness()
class Individual:
    def __init__(self, seating=None):
        if seating is None:
            seating = generate_random_seating()
        self.seating = seating
        self._fitness = None

    def fitness(self):
        if self._fitness is None:
            self._fitness = calculate_total_fitness(self.seating, relationship_matrix)
        return self._fitness


