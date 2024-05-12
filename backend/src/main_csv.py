import os

import pandas as pd

from backend.src.services.calculate import calculate_cosine_similarity
from backend.src.services.convert import convert_df_to_json
from backend.src.services.preprocess import preprocess_data
from backend.src.services.recommend import recommend_products

# importações para debug
# from services.calculate import calculate_cosine_similarity
# from services.convert import convert_df_to_json
# from services.preprocess import preprocess_data
# from services.recommend import recommend_products


def create_df():
    """
    Cria um DataFrame a partir dos dados do banco de dados e realiza o pré-processamento.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "db", "database", "produtos.csv")
    df = pd.read_csv(file_path, sep=",")
    df = preprocess_data(df)
    return df


def get_options():
    """
    Retorna as opções para o algoritmo de recomendação.
    """
    price_range = (14, 16)
    color = "black"
    return {"price_range": price_range, "color": color}


def recomend_algorithm(df, price_range, color):
    """
    Algoritmo de recomendação que utiliza similaridade de cossenos.
    Retorna um DataFrame com as recomendações.
    """
    cosine_sim = calculate_cosine_similarity(df)
    recommendations = recommend_products(price_range, color, cosine_sim, df)

    # retornar um DataFrame vazio caso não haja recomendações
    if not recommendations:
        return pd.DataFrame()

    df_recommendations = pd.DataFrame(columns=df.columns)
    dfs_recommendations_list = []

    for product in recommendations:
        df_temp = pd.DataFrame([product], columns=df.columns)
        dfs_recommendations_list.append(df_temp)
    df_recommendations = pd.concat(dfs_recommendations_list, ignore_index=True)

    return df_recommendations


def show_recommendations(df, price_range, color):
    """
    Exibe as recomendações.
    """
    print(
        f"\nRecomendação feita a partir de: {price_range[0]} >= preço <= {price_range[1]} |  Cor = {color}"
    )
    print("\nDataFrame das recomendações:")
    print(df)


def get_recommendations(options):
    # Criação do DataFrame a partir dos dados do banco - dados pré-processados
    df = create_df()

    # Criando o DataFrame das recomendações do sistema
    df_recommendations = recomend_algorithm(
        df, options["price_range"], options["color"]
    )

    if df_recommendations.empty:
        return

    df_recommendations.drop(columns=["normalized_price", "numeric_color"], inplace=True)

    json_recommendations = convert_df_to_json(df_recommendations)

    return json_recommendations
