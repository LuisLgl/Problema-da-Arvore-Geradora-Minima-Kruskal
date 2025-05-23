def particao_numeros_gulosa(numeros):
    """
    Particiona uma lista de números em dois subconjuntos usando uma abordagem gulosa.

    A ideia é ordenar os números em ordem decrescente e, em seguida,
    atribuir cada número ao subconjunto que atualmente tem a menor soma.

    Retorna:
        tuple: (soma_subconjunto1, soma_subconjunto2, diferenca_absoluta,
                subconjunto1, subconjunto2)
    """
    if not numeros:
        return 0, 0, 0, [], []

    # Ordena os números em ordem decrescente para a estratégia gulosa
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

# Exemplo de uso:
numeros_exemplo_guloso = [10, 4, 6, 3, 7, 9, 2]
soma1_g, soma2_g, dif_g, sub1_g, sub2_g = particao_numeros_gulosa(numeros_exemplo_guloso)

print("--- Abordagem Gulosa ---")
print(f"Números: {numeros_exemplo_guloso}")
print(f"Subconjunto 1: {sub1_g} (Soma: {soma1_g})")
print(f"Subconjunto 2: {sub2_g} (Soma: {soma2_g})")
print(f"Diferença Absoluta: {dif_g}")
print("-" * 30)