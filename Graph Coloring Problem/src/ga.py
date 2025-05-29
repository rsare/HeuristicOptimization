# src/ga.py
from typing import List
import random
import matplotlib.pyplot as plt
from operators import tournament, crossover, mutate, repair

from chromosome import Chromosome
from operators import tournament, crossover, mutate
from graph_loader import load_dimacs


class GeneticAlgorithm:
    """
    A simple GA for Graph Coloring:
    - minimise conflicts first (penalty_weight), then number of colors
    - records best fitness each generation and plots a convergence curve
    """

    def __init__(
        self,
        path: str,
        pop_size: int = 100,
        max_colors: int = 20,
        penalty_weight: int = 1_000,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.02,
        generations: int = 500,
    ):
        # ---------- problem ----------
        self.n, self.edges = load_dimacs(path)

        # ---------- parameters ----------
        self.pop_size = pop_size
        self.max_colors = max_colors
        self.penalty_weight = penalty_weight
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations

        # ---------- initial population ----------
        self.population: List[Chromosome] = [
            Chromosome.random(self.n, self.max_colors) for _ in range(pop_size)
        ]
        for ch in self.population:
            ch.evaluate(self.edges, self.penalty_weight)

        # ---------- convergence history ----------
        self.best_per_gen: list[int] = []

    # ------------------------------------------------------------------ #
    #                                GA LOOP                             #
    # ------------------------------------------------------------------ #
    def run(self) -> Chromosome:
        best = min(self.population, key=lambda c: c.fitness)

        for gen in range(self.generations):
            new_pop: List[Chromosome] = []

            # reproduction
            while len(new_pop) < self.pop_size:
                p1 = tournament(self.population, k=3)
                p2 = tournament(self.population, k=3)

                # crossover
                if random.random() < self.crossover_rate:
                    c1, c2 = crossover(p1, p2)
                else:
                    c1, c2 = (
                        Chromosome(p1.genes.copy()),
                        Chromosome(p2.genes.copy()),
                    )

                # mutation
                mutate(c1, self.max_colors, self.mutation_rate)
                mutate(c2, self.max_colors, self.mutation_rate)

                repair(c1, self.edges, self.max_colors)
                repair(c2, self.edges, self.max_colors)

                # fitness
                c1.evaluate(self.edges, self.penalty_weight)
                c2.evaluate(self.edges, self.penalty_weight)

                new_pop.extend([c1, c2])

            # elitism — keep previous best
            new_pop[random.randrange(self.pop_size)] = best
            self.population = new_pop
            best = min(self.population, key=lambda c: c.fitness)

            # log
            self.best_per_gen.append(best.fitness)
            print(f"Gen {gen:3d} | Best fitness: {best.fitness}")

            # early stop
            if best.fitness == len(set(best.genes)):
                print("Conflict-free coloring found. Stopping early.")
                break

        # plot convergence
        plt.figure()
        plt.plot(self.best_per_gen)
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness")
        plt.title("GA Convergence Curve")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("convergence.png")
        plt.show()

        return best


# ---------------------------------------------------------------------- #
#                         STAND-ALONE TEST HARNESS                       #
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    ga = GeneticAlgorithm(
        path="C:\Projects\HeuristicOptimization\Graph Coloring Problem\data\dimacs-benchmarks\gc_50_9",
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
