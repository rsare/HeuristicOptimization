from ga import GeneticAlgorithm

if __name__ == "__main__":
    ga = GeneticAlgorithm(
        path="C:\Projects\HeuristicOptimization\data\dimacs-benchmarks\gc_50_9",
        pop_size=200,
        max_colors=30,
        penalty_weight=1000,
        crossover_rate=0.9,
        mutation_rate=0.05,
        generations=1000
    )
    best = ga.run()
    print("\nBest Solution:", best.genes)
    print("Number of using color:", len(set(best.genes)))
