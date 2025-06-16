import time
import tracemalloc
import random
import matplotlib.pyplot as plt
import numpy as np

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

        self.arestas = sorted(self.arestas, key=lambda item: item[2])
        
        parent = [i for i in range(self.V)]
        rank = [0] * self.V

        if show_steps:
            print(f"\n--- Executando Kruskal para grafo com {self.V} vértices ---")

        while e < self.V - 1 and i < len(self.arestas):
            u, v, peso = self.arestas[i]
            i += 1

            if union(parent, rank, u, v):
                e += 1
                resultado_agm.append([u, v, peso])
                custo_total += peso
                if show_steps:
                    print(f"Aresta adicionada: {u}-{v} (Peso: {peso})")
        
        if show_steps:
            print(f"Custo Total da AGM: {custo_total}")
            
        return resultado_agm, custo_total

# --- Função para gerar grafos aleatórios ---
def gerar_grafo_aleatorio(num_vertices, densidade=0.5):
    """
    Gera um grafo aleatório e conectado.
    Densidade controla o quão "cheio" o grafo é.
    """
    g = Grafo(num_vertices)
    max_arestas = num_vertices * (num_vertices - 1) // 2
    num_arestas = int(max_arestas * densidade)

    # Garante que o grafo seja conectado
    vertices_conectados = {0}
    vertices_nao_conectados = set(range(1, num_vertices))
    while vertices_nao_conectados:
        u = random.choice(tuple(vertices_conectados))
        v = random.choice(tuple(vertices_nao_conectados))
        peso = random.randint(1, 100)
        g.adiciona_aresta(u, v, peso)
        vertices_conectados.add(v)
        vertices_nao_conectados.remove(v)

    # Adiciona as arestas restantes aleatoriamente
    arestas_existentes = {(min(a[0], a[1]), max(a[0], a[1])) for a in g.arestas}
    while len(g.arestas) < num_arestas:
        u, v = random.sample(range(num_vertices), 2)
        if (min(u, v), max(u, v)) not in arestas_existentes:
            peso = random.randint(1, 100)
            g.adiciona_aresta(u, v, peso)
            arestas_existentes.add((min(u, v), max(u, v)))
            
    return g

# --- Configurações do Teste ---
TAMANHOS_GRAFOS = [5, 20, 50]
NUM_TESTES = 30
resultados = {tamanho: {'tempos': [], 'memorias': []} for tamanho in TAMANHOS_GRAFOS}

# --- Loop Principal de Testes ---
print("Iniciando análise de desempenho...")

for tamanho in TAMANHOS_GRAFOS:
    print(f"\nTestando grafos com {tamanho} vértices...")
    for i in range(NUM_TESTES):
        # Gera um novo grafo aleatório para cada teste
        grafo_teste = gerar_grafo_aleatorio(tamanho)

        # Medição de desempenho
        tracemalloc.start()
        start_time = time.time()

        # Executa o algoritmo (sem mostrar os passos para não poluir a saída)
        grafo_teste.kruskal(show_steps=False)

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Armazena os resultados
        resultados[tamanho]['tempos'].append(end_time - start_time)
        resultados[tamanho]['memorias'].append(peak / 1024) # Convertido para KB

    print(f"Testes para {tamanho} vértices concluídos.")

# --- Processamento e Exibição dos Resultados ---
print("\n--- Resultados Médios da Análise de Desempenho ---")
medias = {}
for tamanho, dados in resultados.items():
    tempo_medio = np.mean(dados['tempos'])
    memoria_media = np.mean(dados['memorias'])
    medias[tamanho] = {'tempo_medio': tempo_medio, 'memoria_media': memoria_media}
    print(f"Tamanho: {tamanho} vértices | Tempo Médio: {tempo_medio:.6f}s | Memória Média de Pico: {memoria_media:.4f} KB")

# --- Plotagem dos Gráficos ---
tamanhos = list(medias.keys())
tempos_medios = [d['tempo_medio'] for d in medias.values()]
memorias_medias = [d['memoria_media'] for d in medias.values()]

# Gráfico de Tempo de Execução
plt.figure(figsize=(10, 6))
plt.plot(tamanhos, tempos_medios, marker='o', linestyle='-', color='b')
plt.title('Tempo Médio de Execução vs. Tamanho do Grafo')
plt.xlabel('Número de Vértices')
plt.ylabel('Tempo Médio (segundos)')
plt.xticks(tamanhos)
plt.grid(True)
plt.savefig('tempo_execucao_vs_tamanho.png')
print("\nGráfico 'tempo_execucao_vs_tamanho.png' foi salvo.")

# Gráfico de Uso de Memória
plt.figure(figsize=(10, 6))
plt.plot(tamanhos, memorias_medias, marker='s', linestyle='--', color='r')
plt.title('Uso Médio de Memória vs. Tamanho do Grafo')
plt.xlabel('Número de Vértices')
plt.ylabel('Memória de Pico Média (KB)')
plt.xticks(tamanhos)
plt.grid(True)
plt.savefig('memoria_vs_tamanho.png')
print("Gráfico 'memoria_vs_tamanho.png' foi salvo.")