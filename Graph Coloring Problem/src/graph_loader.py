from typing import List, Tuple

def load_dimacs(path: str) -> Tuple[int, List[Tuple[int, int]]]:
    """
    İki formatı da destekler:
    1) DIMACS (.col)   : 'p edge 50 1103', 'e 1 2' ...
    2) Basit sayı list : '50 1103', '0 1' ...
    """
    edges: List[Tuple[int, int]] = []
    n_vertices = 0

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("c"):
                continue

            # --- Basit format mı? ---
            if line[0].isdigit():
                parts = line.split()
                if len(parts) == 2:
                    u, v = parts
                    if edges == [] and n_vertices == 0:
                        # ilk satır tepe & kenar sayısı
                        n_vertices = int(u)
                        continue          # kenar değil, header
                    edges.append((int(u), int(v)))  # zaten 0-index
                continue

            # --- DIMACS formatı ---
            if line.startswith("p"):
                _, _, n_vertices, _ = line.split()
                n_vertices = int(n_vertices)
            elif line.startswith("e"):
                _, u, v = line.split()
                edges.append((int(u) - 1, int(v) - 1))  # 0-index’e çevir

    return n_vertices, edges