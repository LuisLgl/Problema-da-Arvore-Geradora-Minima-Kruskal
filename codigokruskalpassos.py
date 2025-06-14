import time
import tracemalloc

# --- Estrutura de dados Union-Find para detectar ciclos ---


def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]


def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    if root_x != root_y:
        if rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_x] = root_y
            if rank[root_x] == rank[root_y]:
                rank[root_y] += 1
        return True
    return False

# --- Classe Grafo com a implementação de Kruskal ---


class Grafo:
    def __init__(self, vertices):
        self.V = vertices
        self.arestas = []

    def adiciona_aresta(self, u, v, peso):
        self.arestas.append([u, v, peso])

    def kruskal(self, show_steps=False):
        resultado_agm = []
        custo_total = 0
        i = 0
        e = 0

        # Passo 1: Ordenar todas as arestas em ordem crescente de peso
        self.arestas = sorted(self.arestas, key=lambda item: item[2])

        parent = [i for i in range(self.V)]
        rank = [0] * self.V

        if show_steps:
            print("--- Etapas da Execução de Kruskal ---")

        # Itera sobre as arestas ordenadas
        while e < self.V - 1 and i < len(self.arestas):
            u, v, peso = self.arestas[i]
            i += 1

            # Passo 2: Verifica se a aresta forma um ciclo
            if union(parent, rank, u, v):
                e += 1
                resultado_agm.append([u, v, peso])
                custo_total += peso
                if show_steps:
                    print(f"Aresta adicionada: {u}-{v} (Peso: {peso})")
            else:
                if show_steps:
                    print(
                        f"Aresta descartada (forma ciclo): {u}-{v} (Peso: {peso})")

        if show_steps:
            print("\n--- Resultado Final ---")
            print("Árvore Geradora Mínima (AGM):")
            for u, v, peso in resultado_agm:
                print(f"{u} -- {v} == {peso}")
            print(f"Custo Total da AGM: {custo_total}")

        return resultado_agm, custo_total

# --- Demonstração do Passo a Passo ---


# Criando um grafo de exemplo
num_vertices = 5
g = Grafo(num_vertices)
g.adiciona_aresta(0, 3, 1)  # A-D
g.adiciona_aresta(2, 3, 2)  # C-D
g.adiciona_aresta(0, 1, 3)  # A-B
g.adiciona_aresta(2, 4, 4)  # C-E
g.adiciona_aresta(1, 3, 5)  # B-D
g.adiciona_aresta(1, 4, 6)  # B-E
g.adiciona_aresta(0, 2, 8)  # A-C

# Chamando a função com show_steps=True para ver a mágica acontecer
g.kruskal(show_steps=True)
