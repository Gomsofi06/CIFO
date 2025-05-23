import random
import numpy as np
from individual import Individual

def swap_mutation(indiv, pm=0.2):
    new_seating = np.copy(indiv.seating)
    seating = indiv.seating
    guest_map = indiv.create_guest_table_map(seating).copy()
    
    for guest in range(64):
        if random.random() < pm:
            ti, idx = guest_map[guest]
            other_ti = random.choice([t for t in range(8) if t != ti])
            other_idx = random.randint(0, 7)
            
            other_guest = new_seating[other_ti, other_idx]
            
            # Swap positions
            new_seating[ti, idx], new_seating[other_ti, other_idx] = other_guest, guest
            
            # Update mappings
            guest_map[guest] = (other_ti, other_idx)
            guest_map[other_guest] = (ti, idx)
    
    return Individual(new_seating)

def one_point_mutation(indiv):
    new_seating = np.copy(indiv.seating)
    guest = random.randint(0, 63)
    seating = indiv.seating
    ti, idx = indiv.create_guest_table_map(seating)[guest]
    new_ti = random.choice([t for t in range(8) if t != ti])
    new_idx = random.randint(0, 7)
    
    other_guest = new_seating[new_ti, new_idx]
    new_seating[ti, idx], new_seating[new_ti, new_idx] = other_guest, guest
    return Individual(new_seating)

def multiple_point_mutation(indiv, mutations=10):
    new_indiv = indiv
    for _ in range(mutations):
        new_indiv = one_point_mutation(new_indiv)
    return new_indiv

def inversion_mutation(indiv):
    flat = indiv.seating.flatten()
    start, end = sorted(random.sample(range(64), 2))
    flat[start:end] = flat[start:end][::-1]
    return Individual(flat.reshape(8, 8))

