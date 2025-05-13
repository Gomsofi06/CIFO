import numpy as np
from fitness import calculate_total_fitness

class Individual:
    def __init__(self, seating=None):
        # Initialize seating first
        if seating is None:
            self.seating = np.random.permutation(64).reshape(8, 8)
        else:
            self.seating = np.array(seating)
        
        # Create guest map BEFORE validation
        self._guest_table_map = self.create_guest_table_map(self.seating)
        
        # Validate after creating the map
        if seating is not None:
            self.validate()
        
        self._fitness = None

    def create_guest_table_map(self, seating):
        """Create a mapping of guests to their table and index."""
        return {
            guest: (ti, idx)
            for ti in range(8)
            for idx, guest in enumerate(seating[ti])
        }

    def validate(self):
        """Ensure the individual meets problem constraints"""
        # Check array shape
        if self.seating.shape != (8, 8):
            raise ValueError("Invalid table dimensions")
        
        # Check all guests are present exactly once
        unique = np.unique(self.seating)
        if len(unique) != 64 or not np.all(unique == np.arange(64)):
            raise ValueError("Invalid guest arrangement")
        
        # Check guest-table mapping consistency
        for guest in range(64):
            ti, idx = self._guest_table_map[guest]
            if self.seating[ti, idx] != guest:
                raise ValueError("Guest-table map inconsistency")

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = calculate_total_fitness(self.seating)
        return self._fitness

    def __repr__(self):
        return f"Individual(fitness={self.fitness:.2f})"
