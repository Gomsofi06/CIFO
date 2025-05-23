# CIFO project

Project for the Computer Inteligence for Optimization course of the Master in Data Science at the NOVA IMS Faculty, Lisbon

Made in collaboration between **Sofia Gomes**, **Marta Boavida**, **David Cascão** and **Jan-Louis Schneider**

## Objective of the Project

This project applies a Genetic Algorithm (GA) to solve the Wedding Seating Optimization problem. The objective is to maximize the total relationship score between guests by optimizing how they are seated across tables, while ensuring all seating constraints are respected.

## How to execute

1.⁠ ⁠Clone the repository and navigate to src folder:

 ```bash
   git clone https://github.com/Gomsofi06/CIFO.git
   cd src
```
    ⁠
2.⁠ ⁠Choose the parameters in grid_search.py

3.⁠ ⁠To run the grid search: 
```bash
    python grid_search.py
````

## Approach

We implemented a genetic algorithm where each individual represents a complete seating plan. The algorithm evolves the population over multiple generations using various genetic operators:

- **Selection**: Tournament, Roulette, Ranking, Stochastic Universal Sampling, Boltzmann
- **Crossover**: Group-Based, Greedy Merge, Table Preservation, PMX
- **Mutation**: Swap, One-Point, Multi-Point, Inversion

## Performance

Performance was measured using a custom composite score balancing:
- Average fitness (solution quality)
- Max fitness (exploration potential)
- Standard deviation (consistency)
- Generations to convergence (efficiency)

## Results

- **Advanced configurations** (e.g., Boltzmann + partial elitism) consistently outperformed simple ones.
- Achieved fitness scores up to **162,500**, although not always reproducible.
- Final advanced configuration converged **3.5x faster** than simple methods.
