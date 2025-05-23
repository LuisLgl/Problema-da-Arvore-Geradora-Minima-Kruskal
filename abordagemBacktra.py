def particao_numeros_backtracking_util(numeros, indice, soma_atual_sub1, soma_total,
                                       subconjunto1_atual, melhor_diferenca_global,
                                       melhor_subconjunto1_global, melhor_subconjunto2_global):
    """
    Função utilitária recursiva para o backtracking.
    """
    # Se todos os itens foram processados
    if indice == len(numeros):
        soma_atual_sub2 = soma_total - soma_atual_sub1
        diferenca_atual = abs(soma_atual_sub1 - soma_atual_sub2)

        if diferenca_atual < melhor_diferenca_global[0]:
            melhor_diferenca_global[0] = diferenca_atual
            # Armazena a melhor partição encontrada
            melhor_subconjunto1_global[:] = subconjunto1_atual[:]
            # Calcula o subconjunto 2 correspondente
            subconjunto2_temp = []
            todos_numeros_copia = list(numeros) # Copia para poder remover
            for item in melhor_subconjunto1_global:
                if item in todos_numeros_copia: # Verifica para evitar erro se houver duplicados
                    todos_numeros_copia.remove(item)
            melhor_subconjunto2_global[:] = todos_numeros_copia[:]
        return

    # Caso 1: Incluir o elemento atual no primeiro subconjunto
    subconjunto1_atual.append(numeros[indice])
    particao_numeros_backtracking_util(numeros, indice + 1, soma_atual_sub1 + numeros[indice],
                                       soma_total, subconjunto1_atual,
                                       melhor_diferenca_global, melhor_subconjunto1_global,
                                       melhor_subconjunto2_global)
    subconjunto1_atual.pop() # Backtrack

    # Caso 2: Não incluir o elemento atual no primeiro subconjunto (ele irá para o segundo)
    particao_numeros_backtracking_util(numeros, indice + 1, soma_atual_sub1,
                                       soma_total, subconjunto1_atual,
                                       melhor_diferenca_global, melhor_subconjunto1_global,
                                       melhor_subconjunto2_global)


def particao_numeros_backtracking(numeros):
    """
    Particiona uma lista de números em dois subconjuntos usando backtracking
    para encontrar a menor diferença possível entre as somas dos subconjuntos.

    Retorna:
        tuple: (soma_subconjunto1, soma_subconjunto2, diferenca_absoluta,
                subconjunto1, subconjunto2)
    """
    if not numeros:
        return 0, 0, 0, [], []

    soma_total = sum(numeros)
    # Usamos listas para passar por referência e modificar dentro da recursão
    melhor_diferenca_global = [float('inf')]
    melhor_subconjunto1_global = []
    melhor_subconjunto2_global = []

    particao_numeros_backtracking_util(numeros, 0, 0, soma_total, [],
                                       melhor_diferenca_global,
                                       melhor_subconjunto1_global,
                                       melhor_subconjunto2_global)

    soma1_otima = sum(melhor_subconjunto1_global)
    soma2_otima = sum(melhor_subconjunto2_global)

    return (soma1_otima, soma2_otima, melhor_diferenca_global[0],
            melhor_subconjunto1_global, melhor_subconjunto2_global)

# Exemplo de uso:
numeros_exemplo_backtracking = [10, 4, 6, 3, 7, 9, 2]
soma1_bt, soma2_bt, dif_bt, sub1_bt, sub2_bt = particao_numeros_backtracking(numeros_exemplo_backtracking)

print("--- Abordagem de Backtracking ---")
print(f"Números: {numeros_exemplo_backtracking}")
print(f"Subconjunto 1: {sub1_bt} (Soma: {soma1_bt})")
print(f"Subconjunto 2: {sub2_bt} (Soma: {soma2_bt})")
print(f"Melhor Diferença Absoluta: {dif_bt}")
print("-" * 30)

# Comparando com o mesmo exemplo da gulosa:
numeros_exemplo_comp = [10, 4, 6, 3, 7, 9, 2]
soma1_g_comp, soma2_g_comp, dif_g_comp, sub1_g_comp, sub2_g_comp = particao_numeros_gulosa(numeros_exemplo_comp)
soma1_bt_comp, soma2_bt_comp, dif_bt_comp, sub1_bt_comp, sub2_bt_comp = particao_numeros_backtracking(numeros_exemplo_comp)

print("\n--- Comparação para o mesmo conjunto ---")
print(f"Números: {numeros_exemplo_comp}")
print(f"Gulosa -> Dif: {dif_g_comp}, Sub1: {sub1_g_comp}, Sub2: {sub2_g_comp}")
print(f"Backtracking -> Dif: {dif_bt_comp}, Sub1: {sub1_bt_comp}, Sub2: {sub2_bt_comp}")