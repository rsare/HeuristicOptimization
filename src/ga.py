from typing import List
import random
from chromosome import Chromosome
from operators import tournament, crossover, mutate
from graph_loader import load_dimacs

class GeneticAlgorithm:
    def __init__(self, path: str,
                 pop_size: int = 100,
                 max_colors: int = 20,
                 penalty_weight: int = 1000,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.02,
                 generations: int = 500):
        self.n, self.edges = load_dimacs(path)
        self.pop_size = pop_size
        self.max_colors = max_colors
        self.penalty_weight = penalty_weight
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population: List[Chromosome] = [
            Chromosome.random(self.n, self.max_colors)
            for _ in range(pop_size)
        ]
        for ch in self.population:
            ch.evaluate(self.edges, self.penalty_weight)

    # ------------------ Ana Döngü ------------------
    def run(self) -> Chromosome:
        best = min(self.population, key=lambda c: c.fitness)
        for gen in range(self.generations):
            new_pop: List[Chromosome] = []
            while len(new_pop) < self.pop_size:
                p1 = tournament(self.population, k=3)
                p2 = tournament(self.population, k=3)
                # Crossover
                if random.random() < self.crossover_rate:
                    c1, c2 = crossover(p1, p2)
                else:
                    c1, c2 = Chromosome(p1.genes.copy()), Chromosome(p2.genes.copy())
                # Mutasyon
                mutate(c1, self.max_colors, self.mutation_rate)
                mutate(c2, self.max_colors, self.mutation_rate)
                # Fitness
                c1.evaluate(self.edges, self.penalty_weight)
                c2.evaluate(self.edges, self.penalty_weight)
                new_pop.extend([c1, c2])
            # Elitizm: En iyi bireyi koru
            new_pop[random.randrange(self.pop_size)] = best
            self.population = new_pop
            best = min(self.population, key=lambda c: c.fitness)
            # --- TODO: convergence grafiği için tarihçe kaydetmek isterseniz burada ekleyin ---
            print(f"Gen {gen:3d} | Best fitness: {best.fitness}")
            if best.fitness == len(set(best.genes)):  # conflicts=0
                print("Conflict-free boyama bulundu, erken durduruldu.")
                break
        return best
