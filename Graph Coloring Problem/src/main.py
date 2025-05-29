# src/main.py
from ga import GeneticAlgorithm

if __name__ == "__main__":
    # >>>  path=  satırını burada düzenle  <<<
    ga = GeneticAlgorithm(
        path=r"C:\Projects\HeuristicOptimization\Graph Coloring Problem\data\dimacs-benchmarks\gc_50_9",
        pop_size=200,
        max_colors=30,
        penalty_weight=1000,
        crossover_rate=0.9,
        mutation_rate=0.05,
        generations=1000,
    )

    best = ga.run()
    print("\nBest solution:", best.genes)
    print("Colors used  :", len(set(best.genes)))
