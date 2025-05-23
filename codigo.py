import time # Para medir o tempo de execução, conforme sugerido no trabalho [cite: 8]

# --- Abordagem Gulosa 1: Ordenar em ordem decrescente ---
def particao_numeros_gulosa_v1(numeros):
    """
    Particiona uma lista de números em dois subconjuntos usando uma abordagem gulosa.
    Os números são ordenados em ordem decrescente e atribuídos ao subconjunto
    com a menor soma atual.
    """
    if not numeros:
        return 0, 0, 0, [], []

    numeros_ordenados = sorted(numeros, reverse=True)

    subconjunto1 = []
    soma1 = 0
    subconjunto2 = []
    soma2 = 0

    for num in numeros_ordenados:
        if soma1 <= soma2:
            subconjunto1.append(num)
            soma1 += num
        else:
            subconjunto2.append(num)
            soma2 += num

    diferenca = abs(soma1 - soma2)
    return soma1, soma2, diferenca, subconjunto1, subconjunto2

# --- Abordagem Gulosa 2: Processar na ordem fornecida ---
def particao_numeros_gulosa_v2(numeros):
    """
    Particiona uma lista de números em dois subconjuntos usando uma abordagem gulosa.
    Os números são processados na ordem em que são fornecidos e atribuídos
    ao subconjunto com a menor soma atual.
    """
    if not numeros:
        return 0, 0, 0, [], []

    subconjunto1 = []
    soma1 = 0
    subconjunto2 = []
    soma2 = 0

    for num in numeros: # Sem ordenação prévia
        if soma1 <= soma2:
            subconjunto1.append(num)
            soma1 += num
        else:
            subconjunto2.append(num)
            soma2 += num

    diferenca = abs(soma1 - soma2)
    return soma1, soma2, diferenca, subconjunto1, subconjunto2

# --- Abordagem de Backtracking (Solução Ótima) ---
def particao_numeros_backtracking_util(
    numeros, indice, soma_atual_sub1, soma_total,
    subconjunto1_atual, melhor_diferenca_global,
    melhor_subconjunto1_global_ref, melhor_subconjunto2_global_ref
):
    """
    Função utilitária recursiva para o backtracking.
    """
    # Se todos os itens foram processados
    if indice == len(numeros):
        soma_atual_sub2 = soma_total - soma_atual_sub1
        diferenca_atual = abs(soma_atual_sub1 - soma_atual_sub2)

        if diferenca_atual < melhor_diferenca_global[0]:
            melhor_diferenca_global[0] = diferenca_atual
            melhor_subconjunto1_global_ref[0] = list(subconjunto1_atual) # Armazena cópia

            # Calcula o subconjunto 2 correspondente
            subconjunto2_temp = []
            elementos_sub1 = set(melhor_subconjunto1_global_ref[0])
            # Para lidar com duplicados corretamente, iteramos sobre os originais
            copia_numeros = list(numeros)
            temp_s1 = list(melhor_subconjunto1_global_ref[0]) # Cópia para remover

            for item_s1 in temp_s1:
                if item_s1 in copia_numeros:
                    copia_numeros.remove(item_s1)
            melhor_subconjunto2_global_ref[0] = copia_numeros

        return

    # Poda: se a diferença atual já é maior que a melhor encontrada,
    # e estamos considerando apenas adições positivas, pode não ser útil
    # (mas para partição de números genéricos, a poda é mais complexa)

    # Caso 1: Incluir o elemento atual no primeiro subconjunto
    subconjunto1_atual.append(numeros[indice])
    particao_numeros_backtracking_util(
        numeros, indice + 1, soma_atual_sub1 + numeros[indice],
        soma_total, subconjunto1_atual,
        melhor_diferenca_global, melhor_subconjunto1_global_ref, melhor_subconjunto2_global_ref
    )
    subconjunto1_atual.pop() # Backtrack

    # Caso 2: Não incluir o elemento atual no primeiro subconjunto (ele irá para o segundo)
    particao_numeros_backtracking_util(
        numeros, indice + 1, soma_atual_sub1,
        soma_total, subconjunto1_atual,
        melhor_diferenca_global, melhor_subconjunto1_global_ref, melhor_subconjunto2_global_ref
    )

def particao_numeros_backtracking(numeros):
    """
    Particiona uma lista de números em dois subconjuntos usando backtracking
    para encontrar a menor diferença possível entre as somas dos subconjuntos.
    """
    if not numeros:
        return 0, 0, 0, [], []

    soma_total = sum(numeros)
    # Usamos listas dentro de listas para passar por referência de forma mutável
    melhor_diferenca_global = [float('inf')]
    melhor_subconjunto1_global_ref = [[]]
    melhor_subconjunto2_global_ref = [[]]

    particao_numeros_backtracking_util(
        numeros, 0, 0, soma_total, [],
        melhor_diferenca_global, melhor_subconjunto1_global_ref, melhor_subconjunto2_global_ref
    )

    soma1_otima = sum(melhor_subconjunto1_global_ref[0])
    soma2_otima = sum(melhor_subconjunto2_global_ref[0])
    # Garante que soma1 + soma2 == soma_total, mesmo com duplicados
    if soma1_otima + soma2_otima != soma_total and melhor_subconjunto2_global_ref[0] == []:
        # Recalcula s2 se não foi populado corretamente no caso de todos os itens irem para s1
        # ou se a lógica de reconstrução de s2 falhou por algum motivo
        temp_s1_set = {}
        for x in melhor_subconjunto1_global_ref[0]:
            temp_s1_set[x] = temp_s1_set.get(x, 0) + 1

        temp_s2 = []
        for x in numeros:
            if x in temp_s1_set and temp_s1_set[x] > 0:
                temp_s1_set[x] -=1
            else:
                temp_s2.append(x)
        melhor_subconjunto2_global_ref[0] = temp_s2
        soma2_otima = sum(melhor_subconjunto2_global_ref[0])


    return (soma1_otima, soma2_otima, melhor_diferenca_global[0],
            melhor_subconjunto1_global_ref[0], melhor_subconjunto2_global_ref[0])

# --- Seção de Testes ---
if __name__ == "__main__":
    # Conjuntos de teste (para entradas "pequenas" onde o backtracking é viável) [cite: 2]
    # Para entradas maiores, o backtracking pode ser muito custoso [cite: 2]
    conjuntos_de_teste = [
        ([10, 4, 6, 3, 7, 9, 2], "Conjunto 1"), # Soma = 41
        ([3, 1, 4, 2, 2, 10], "Conjunto 2"),   # Soma = 22
        ([20, 5, 15, 10], "Conjunto 3"),       # Soma = 50
        ([1, 2, 3, 4, 5, 100], "Conjunto 4"), # Soma = 115, com um outlier
        ([7, 7, 7, 7], "Conjunto 5")           # Soma = 28
    ]

    for numeros_exemplo, nome_conjunto in conjuntos_de_teste:
        print(f"\n--- Testando para {nome_conjunto}: {numeros_exemplo} (Soma Total: {sum(numeros_exemplo)}) ---")

        # Teste Gulosa V1
        start_time = time.perf_counter()
        soma1_g1, soma2_g1, dif_g1, sub1_g1, sub2_g1 = particao_numeros_gulosa_v1(list(numeros_exemplo))
        end_time = time.perf_counter()
        tempo_g1 = (end_time - start_time) * 1000 # milissegundos
        print("\nResultados da Abordagem Gulosa V1 (Ordenar Decrescente):")
        print(f"  Subconjunto 1: {sub1_g1} (Soma: {soma1_g1})")
        print(f"  Subconjunto 2: {sub2_g1} (Soma: {soma2_g1})")
        print(f"  Diferença Absoluta: {dif_g1}")
        print(f"  Tempo de execução: {tempo_g1:.4f} ms")

        # Teste Gulosa V2
        start_time = time.perf_counter()
        soma1_g2, soma2_g2, dif_g2, sub1_g2, sub2_g2 = particao_numeros_gulosa_v2(list(numeros_exemplo))
        end_time = time.perf_counter()
        tempo_g2 = (end_time - start_time) * 1000 # milissegundos
        print("\nResultados da Abordagem Gulosa V2 (Ordem Fornecida):")
        print(f"  Subconjunto 1: {sub1_g2} (Soma: {soma1_g2})")
        print(f"  Subconjunto 2: {sub2_g2} (Soma: {soma2_g2})")
        print(f"  Diferença Absoluta: {dif_g2}")
        print(f"  Tempo de execução: {tempo_g2:.4f} ms")

        # Teste Backtracking
        start_time = time.perf_counter()
        soma1_bt, soma2_bt, dif_bt, sub1_bt, sub2_bt = particao_numeros_backtracking(list(numeros_exemplo))
        end_time = time.perf_counter()
        tempo_bt = (end_time - start_time) * 1000 # milissegundos
        print("\nResultados da Abordagem de Backtracking (Ótima):")
        print(f"  Subconjunto 1: {sub1_bt} (Soma: {soma1_bt})")
        print(f"  Subconjunto 2: {sub2_bt} (Soma: {soma2_bt})")
        print(f"  Melhor Diferença Absoluta: {dif_bt}") # O backtracking encontra a melhor solução? [cite: 6]
        print(f"  Tempo de execução: {tempo_bt:.4f} ms")
        print("-" * 40)