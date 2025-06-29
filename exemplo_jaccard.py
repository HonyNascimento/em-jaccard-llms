def jaccard_similarity(str1, str2):
    tokens1 = set(str(str1).lower().split())
    tokens2 = set(str(str2).lower().split())
    if not tokens1 or not tokens2:
        return 0.0
    return len(tokens1 & tokens2) / len(tokens1 | tokens2)

# Entrada manual de dois produtos
#print("Digite a descrição do primeiro produto:")
#prod1 = input("Produto 1: ")
#print("Digite a descrição do segundo produto:")
#prod2 = input("Produto 2: ")
prod1 = "Coca Cola 2L Zero" # Produto 1"
prod2 = "Coca Cola Zero 2L" # Produto 2"

prod1 = "Coca Cola 2L zero" # Produto 1"
prod2 = "Coca Cola 1L zero" # Produto 2"

prod1 = "Coca Cola 2L Pet" # Produto 1"
prod2 = "Coca Cola 2L Descartável" # Produto 2"

prod1 = "1 2 3 4 5 6 7 8 9 10"
prod2 = "10 9 8 "

# Calcular similaridade
score = jaccard_similarity(prod1, prod2)
print(f"\nSimilaridade Jaccard entre os produtos: {score:.4f}")

# Sugestão com base em limiares conhecidos
if score >= 0.9:
    interpretacao = "Muito alta (provavelmente correspondem)"
elif score >= 0.7:
    interpretacao = "Alta (potencialmente correspondem)"
elif score >= 0.5:
    interpretacao = "Moderada (pode haver correspondência parcial)"
elif score >= 0.3:
    interpretacao = "Baixa (provavelmente não correspondem)"
else:
    interpretacao = "Muito baixa (itens diferentes)"

print(f"Interpretação: {interpretacao}")
