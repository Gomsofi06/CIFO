import random

NUM_GUESTS = 64
NUM_TABLES = 8
GUESTS_PER_TABLE = NUM_GUESTS // NUM_TABLES

# Cria um array random com as mesas
def generate_random_seating():
    guests = list(range(64))
    random.shuffle(guests)
    seating = []
    
    for i in range(0, 64, 8):
        seating.append(guests[i:i+8])
    
    return seating
