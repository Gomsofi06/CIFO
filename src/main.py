import sys
import itertools
from ga_runner import run_ga
from crossover_testing import test_crossover
from mutation_testing import test_mutations
from selection_testing import test_selection
from ga_runner import run_ga

def main_menu():
    print("\n|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|")
    print("|                            MENU PRINCIPAL                         |")
    print("|                    1. Correr testes de mutation                   |")
    print("|                    2. Correr testes de crossover                  |")
    print("|                    3. Correr testes de selection                  |")
    print("|                    4. Executar algoritmo genético                 |")
    print("|                    0. Sair                                        |")
    print("|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|")
    print("\n")

    choice = input("Escolha uma opção: ")
    return choice


def ga_final_run():
    selection_types = ["tournament", "ranking", "roulette"]
    crossover_types = ["group", "merge"]
    mutation_types = ["swap", "one_point", "multiple_point"]
    elitism_options = [True, False]

    results = []

    for sel, cross, mut, elit in itertools.product(selection_types, crossover_types, mutation_types, elitism_options):
        print("\n")
        print(f"Running: {sel} - {cross} - {mut} - elitism={elit}")
        best_solution, best_score, best_fitness_per_gen = run_ga(
            pop_size=100,
            generations=100,
            elite_size=2,
            use_elitism=elit,
            selection_type=sel,
            crossover_type=cross,
            mutation_type=mut,
            mutation_prob=0.2,
            seed=42
        )
        results.append({
            "selection": sel,
            "crossover": cross,
            "mutation": mut,
            "elitism": elit,
            "history": best_fitness_per_gen,
            "final_score": best_score
        })
        
    print("\n")
    melhor = max(results, key=lambda x: x['final_score'])
    print(f"Maior final_score: {melhor['final_score']}")


if __name__ == "__main__":
    while True:
        option = main_menu()

        if option == "1":
            test_mutations()
        elif option == "2":
            test_crossover()
        elif option == "3":
            test_selection()
        elif option == "4":
            ga_final_run()
        elif option == "0":
            print("|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|")
            print("|                                                                   |")
            print("|                              Good bye!                            |")
            print("|                                                                   |")
            print("|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")