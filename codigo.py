# -*- coding: utf-8 -*-
# Importa o modulo time para medir o tempo de execucao dos algoritmos[cite: 8].
import time
# Importa o modulo tracemalloc para medir o consumo de memoria.
import tracemalloc

# --- Abordagem Gulosa 1: Ordenar em Ordem Decrescente ---
def particao_numeros_gulosa_v1(numeros):
    """
    Particiona uma lista de numeros em dois subconjuntos usando uma abordagem gulosa.
    Este e o primeiro criterio de escolha local[cite: 3].
    Os numeros sao ordenados em ordem decrescente e, em seguida, cada numero e
    atribuido ao subconjunto que atualmente possui a menor soma.
    """
    # Se a lista de entrada estiver vazia, retorna valores zerados.
    if not numeros:
        return 0, 0, 0, [], []

    # Ordena a lista de numeros em ordem decrescente.
    numeros_ordenados = sorted(numeros, reverse=True)

    # Inicializa os subconjuntos e suas somas.
    subconjunto1 = []
    soma1 = 0
    subconjunto2 = []
    soma2 = 0

    # Itera sobre cada numero da lista ordenada.
    for num in numeros_ordenados:
        # A escolha local gulosa: adiciona o numero ao subconjunto de menor soma.
        if soma1 <= soma2:
            subconjunto1.append(num)
            soma1 += num
        else:
            subconjunto2.append(num)
            soma2 += num

    # Calcula a diferenca final entre as somas dos dois subconjuntos.
    diferenca = abs(soma1 - soma2)
    return soma1, soma2, diferenca, subconjunto1, subconjunto2

# --- Abordagem Gulosa 2: Processar na Ordem Fornecida ---
def particao_numeros_gulosa_v2(numeros):
    """
    Particiona uma lista de numeros em dois subconjuntos usando uma abordagem gulosa.
    Este e o segundo criterio de escolha local[cite: 3].
    Os numeros sao processados na ordem em que sao fornecidos, sem ordenacao previa.
    Cada numero e atribuido ao subconjunto com a menor soma atual.
    """
    # Se a lista de entrada estiver vazia, retorna valores zerados.
    if not numeros:
        return 0, 0, 0, [], []

    # Inicializa os subconjuntos e suas somas.
    subconjunto1 = []
    soma1 = 0
    subconjunto2 = []
    soma2 = 0

    # Itera sobre cada numero na ordem original da lista.
    for num in numeros:
        # A escolha local gulosa: adiciona o numero ao subconjunto de menor soma.
        if soma1 <= soma2:
            subconjunto1.append(num)
            soma1 += num
        else:
            subconjunto2.append(num)
            soma2 += num

    # Calcula a diferenca final entre as somas.
    diferenca = abs(soma1 - soma2)
    return soma1, soma2, diferenca, subconjunto1, subconjunto2

# --- Abordagem de Backtracking (Solucao Otima) ---
def particao_numeros_backtracking_util(
    numeros, indice, soma_atual_sub1, soma_total,
    subconjunto1_atual, melhor_diferenca_global,
    melhor_subconjunto1_global_ref
):
    """
    Funcao utilitaria recursiva que implementa a logica do backtracking.
    Explora todas as particoes possiveis de forma exaustiva.
    """
    # Caso base da recursao: todos os numeros foram processados.
    if indice == len(numeros):
        # Calcula a soma do segundo subconjunto.
        soma_atual_sub2 = soma_total - soma_atual_sub1
        # Calcula a diferenca da particao atual.
        diferenca_atual = abs(soma_atual_sub1 - soma_atual_sub2)

        # Se a diferenca encontrada for a menor ate agora, atualiza a melhor solucao.
        if diferenca_atual < melhor_diferenca_global[0]:
            melhor_diferenca_global[0] = diferenca_atual
            # Armazena uma copia do subconjunto que gerou a melhor solucao.
            melhor_subconjunto1_global_ref[0] = list(subconjunto1_atual)
        
        return

    # --- Ramo da arvore de decisao 1 ---
    # Inclui o elemento atual (numeros[indice]) no primeiro subconjunto.
    subconjunto1_atual.append(numeros[indice])
    particao_numeros_backtracking_util(
        numeros, indice + 1, soma_atual_sub1 + numeros[indice],
        soma_total, subconjunto1_atual,
        melhor_diferenca_global, melhor_subconjunto1_global_ref
    )
    
    # --- Backtrack ---
    # Remove o elemento para explorar o outro caminho da arvore.
    subconjunto1_atual.pop()

    # --- Ramo da arvore de decisao 2 ---
    # Nao inclui o elemento atual no primeiro subconjunto (ele vai para o segundo).
    particao_numeros_backtracking_util(
        numeros, indice + 1, soma_atual_sub1,
        soma_total, subconjunto1_atual,
        melhor_diferenca_global, melhor_subconjunto1_global_ref
    )

def particao_numeros_backtracking(numeros):
    """
    Funcao principal que prepara e inicia o processo de backtracking.
    Garante encontrar a particao com a menor diferenca possivel entre as somas,
    ou seja, a solucao otima[cite: 6].
    """
    if not numeros:
        return 0, 0, 0, [], []

    soma_total = sum(numeros)
    # Variaveis para armazenar a melhor solucao encontrada. Usamos listas mutaveis
    # para que possam ser modificadas dentro das chamadas recursivas.
    melhor_diferenca_global = [float('inf')]
    melhor_subconjunto1_global_ref = [[]]

    # Inicia a chamada recursiva.
    particao_numeros_backtracking_util(
        numeros, 0, 0, soma_total, [],
        melhor_diferenca_global, melhor_subconjunto1_global_ref
    )

    # Reconstroi os dois subconjuntos da melhor solucao encontrada.
    subconjunto1_otimo = melhor_subconjunto1_global_ref[0]
    soma1_otima = sum(subconjunto1_otimo)
    
    # Reconstroi o subconjunto 2 a partir dos elementos que nao estao no subconjunto 1.
    # E necessario cuidado para lidar com numeros duplicados.
    copia_numeros = list(numeros)
    subconjunto2_otimo = []
    for item in subconjunto1_otimo:
        copia_numeros.remove(item)
    subconjunto2_otimo = copia_numeros
    soma2_otima = sum(subconjunto2_otimo)

    return (soma1_otima, soma2_otima, melhor_diferenca_global[0],
            subconjunto1_otimo, subconjunto2_otimo)

# --- Secao de Testes ---
if __name__ == "__main__":
    # Conjunto de testes para avaliar os algoritmos em diferentes cenarios[cite: 2].
    conjuntos_de_teste = {
        "Conjunto 1 (Geral)": [10, 4, 6, 3, 7, 9, 2],         # Soma = 41
        "Conjunto 2 (Particao Otima Exata)": [20, 5, 15, 10], # Soma = 50
        "Conjunto 3 (Com Outlier)": [1, 2, 3, 4, 5, 100],     # Soma = 115
    }

    # Itera sobre cada conjunto de teste definido.
    for nome_conjunto, numeros_exemplo in conjuntos_de_teste.items():
        print(f"\n--- Testando para {nome_conjunto}: {numeros_exemplo} (Soma Total: {sum(numeros_exemplo)}) ---")

        # --- Teste da Abordagem Gulosa V1 (Ordenar Decrescente) ---
        tracemalloc.start()
        start_time_g1 = time.perf_counter()
        soma1_g1, soma2_g1, dif_g1, sub1_g1, sub2_g1 = particao_numeros_gulosa_v1(list(numeros_exemplo))
        end_time_g1 = time.perf_counter()
        memoria_g1_pico = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        
        tempo_g1 = (end_time_g1 - start_time_g1) * 1000  # Tempo em milissegundos
        print("\nResultados da Abordagem Gulosa V1 (Ordenar Decrescente):")
        print(f"  Subconjunto 1: {sorted(sub1_g1)} (Soma: {soma1_g1})")
        print(f"  Subconjunto 2: {sorted(sub2_g1)} (Soma: {soma2_g1})")
        print(f"  Diferenca Absoluta: {dif_g1}")
        print(f"  Tempo de execucao: {tempo_g1:.4f} ms")
        print(f"  Pico de memoria: {memoria_g1_pico / 1024:.4f} KB")

        # --- Teste da Abordagem Gulosa V2 (Ordem Fornecida) ---
        tracemalloc.start()
        start_time_g2 = time.perf_counter()
        soma1_g2, soma2_g2, dif_g2, sub1_g2, sub2_g2 = particao_numeros_gulosa_v2(list(numeros_exemplo))
        end_time_g2 = time.perf_counter()
        memoria_g2_pico = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        tempo_g2 = (end_time_g2 - start_time_g2) * 1000  # Tempo em milissegundos
        print("\nResultados da Abordagem Gulosa V2 (Ordem Fornecida):")
        print(f"  Subconjunto 1: {sorted(sub1_g2)} (Soma: {soma1_g2})")
        print(f"  Subconjunto 2: {sorted(sub2_g2)} (Soma: {soma2_g2})")
        print(f"  Diferenca Absoluta: {dif_g2}")
        print(f"  Tempo de execucao: {tempo_g2:.4f} ms")
        print(f"  Pico de memoria: {memoria_g2_pico / 1024:.4f} KB")

        # --- Teste da Abordagem de Backtracking (Otima) ---
        tracemalloc.start()
        start_time_bt = time.perf_counter()
        soma1_bt, soma2_bt, dif_bt, sub1_bt, sub2_bt = particao_numeros_backtracking(list(numeros_exemplo))
        end_time_bt = time.perf_counter()
        memoria_bt_pico = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        tempo_bt = (end_time_bt - start_time_bt) * 1000  # Tempo em milissegundos
        print("\nResultados da Abordagem de Backtracking (Otima):")
        print(f"  Subconjunto 1: {sorted(sub1_bt)} (Soma: {soma1_bt})")
        print(f"  Subconjunto 2: {sorted(sub2_bt)} (Soma: {soma2_bt})")
        # Confirma que o backtracking encontra a melhor solucao possivel[cite: 6].
        print(f"  Melhor Diferenca Absoluta: {dif_bt}")
        print(f"  Tempo de execucao: {tempo_bt:.4f} ms")
        print(f"  Pico de memoria: {memoria_bt_pico / 1024:.4f} KB")
        print("-" * 60)