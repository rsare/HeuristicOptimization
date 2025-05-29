import random
from typing import List, Tuple

from chromosome import Chromosome


# -------- Seçim --------
def tournament(pop: List[Chromosome], k: int) -> Chromosome:
    """k-lü turnuva seçimi."""
    return min(random.sample(pop, k), key=lambda c: c.fitness)


# -------- Crossover (Uniform Color Exchange) --------
def crossover(p1: Chromosome, p2: Chromosome) -> Tuple[Chromosome, Chromosome]:
    """Her gen için %50 ihtimalle ebeveyn değiştir."""
    child1 = [g1 if random.random() < 0.5 else g2
              for g1, g2 in zip(p1.genes, p2.genes)]
    child2 = [g2 if random.random() < 0.5 else g1
              for g1, g2 in zip(p1.genes, p2.genes)]
    return Chromosome(child1), Chromosome(child2)


# -------- Mutasyon (Random-Reset) --------
def mutate(ch: Chromosome, max_colors: int, pm: float) -> None:
    for i in range(len(ch.genes)):
        if random.random() < pm:
            ch.genes[i] = random.randint(0, max_colors - 1)
    ch.fitness = None  # eski fitness geçersiz

    # ---------- REPAIR (Conflict Fix) ----------


def repair(ch: Chromosome,
               edges: List[Tuple[int, int]],
               max_colors: int) -> None:

        # Komşuluk listesi hazırlamak O(E)
        neighbors: List[List[int]] = [[] for _ in range(len(ch.genes))]
        for u, v in edges:
            neighbors[u].append(v)
            neighbors[v].append(u)

        # Kenarları dolaş ve çatışmaları çöz
        for u, v in edges:
            if ch.genes[u] == ch.genes[v]:
                # U ya da V'den birini rastgele seç, rengini değiştir
                target = u if random.random() < 0.5 else v
                used = {ch.genes[n] for n in neighbors[target]}
                # Komşularda kullanılmayan bir renk bul
                for _ in range(max_colors):
                    new_color = random.randint(0, max_colors - 1)
                    if new_color not in used:
                        ch.genes[target] = new_color
                        break
        ch.fitness = None  # fitness yeniden hesaplanacak
