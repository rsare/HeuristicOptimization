import random
from typing import List, Tuple

class Chromosome:
    def __init__(self, genes: List[int]):
        self.genes = genes          # renkler
        self.fitness: int | None = None

    @classmethod
    def random(cls, n_vertices: int, max_colors: int) -> "Chromosome":
        genes = [random.randint(0, max_colors - 1) for _ in range(n_vertices)]
        return cls(genes)

    def evaluate(self, edges: List[Tuple[int, int]], penalty_weight: int) -> int:
        """Fitness’i hesapla ve döndür; küçük değer daha iyi."""
        if self.fitness is not None:
            return self.fitness
        conflicts = sum(1 for u, v in edges if self.genes[u] == self.genes[v])
        n_colors_used = len(set(self.genes))
        self.fitness = conflicts * penalty_weight + n_colors_used
        return self.fitness
