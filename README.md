# CIFO project

Project for the Computer Inteligence for Optimization course of the Master in Data Science at the NOVA IMS Faculty, Lisbon

Made in collaboration between **Sofia Gomes**, **Marta Boavida**, **David Cascão** and **Jan-Louis Schneider**

## Objective of the Project

This project applies a Genetic Algorithm (GA) to solve the Wedding Seating Optimization problem. The objective is to maximize the total relationship score between guests by optimizing how they are seated across tables, while ensuring all seating constraints are respected.


## How to execute

1. Clone the repository and navigate to src folder:

   ```bash
   git clone https://github.com/Gomsofi06/CIFO.git
   cd src
   ```

2. Run this: 
    ```bash
    python3 main.py
    ```

## What we did

To get the best possible score, we use genetic operators:
- Three Mutation Operators: Swap, One-Point and Multiple-Point 

- Two Crossover Operators: Group-based and Greedy merge

- Three Selection Methods: Roulette, Ranking and Tournament

## Results

The configuration that yielded the best performance used:
* Selection: Tournament
* Crossover: Merge
* Mutation: One-Point

Best final score achieved: 37800