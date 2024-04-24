# main.py
import pandas as pd
from services.calculate import calculate_cosine_similarity
from services.preprocess import preprocess_data
from services.recommend import recommend_products

# Carregar dados
df = pd.read_csv("db/produtos.csv")

# Pré-processamento dos dados
df = preprocess_data(df)

# Cálculo da similaridade de cossenos
cosine_sim = calculate_cosine_similarity(df)

# Fazer recomendações
price_range = (13, 17)
color = "black"
recommendations = recommend_products(price_range, color, cosine_sim, df)

# Se você ainda não tiver um DataFrame para armazenar as recomendações, você pode criar um vazio
df_recomendacoes = pd.DataFrame(columns=df.columns)

# Lista para armazenar os DataFrames de cada recomendação
dfs_recomendacoes = []

# Adicionando as recomendações ao DataFrame
for product in recommendations:
    # Criando um DataFrame temporário com uma única linha
    df_temp = pd.DataFrame([product], columns=df.columns)
    # Adicionando o DataFrame temporário à lista
    dfs_recomendacoes.append(df_temp)

# Concatenando todos os DataFrames da lista em um único DataFrame
df_recomendacoes = pd.concat(dfs_recomendacoes, ignore_index=True)

# Exibindo o DataFrame com as recomendações
print("DataFrame com as recomendações:")
print(df_recomendacoes)
