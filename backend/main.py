# main.py
import pandas as pd
from db.db_functions import fetch_data
from services.calculate import calculate_cosine_similarity
from services.convert import convert_data_to_df
from services.preprocess import preprocess_data
from services.recommend import recommend_products

# df2 = pd.read_csv("db/database/produtos.csv", sep=",")

# Buscar os dados no banco
data = fetch_data("SELECT * FROM PRODUTOS")

df = convert_data_to_df(data)


# Pré-processamento dos dados
df = preprocess_data(df)

# Cálculo da similaridade de cossenos
cosine_sim = calculate_cosine_similarity(df)

# Fazer recomendações
price_range = (10, 17)
color = "navy"
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
print(
    f"\nRecomendação feita a partir de: {price_range[0]} >= preço <= {price_range[1]} |  Cor = {color}"
)
print("\nDataFrame das recomendações:")
print(df_recomendacoes)
