import pandas as pd

from backend.src.db.db_functions import fetch_data
from backend.src.services.calculate import calculate_cosine_similarity
from backend.src.services.convert import convert_data_to_df, convert_df_to_json
from backend.src.services.preprocess import preprocess_data
from backend.src.services.recommend import recommend_products

# from db.db_functions import fetch_data
# from services.calculate import calculate_cosine_similarity
# from services.convert import convert_data_to_df, convert_df_to_json
# from services.preprocess import preprocess_data
# from services.recommend import recommend_products


def create_df():
    """
    Cria um DataFrame a partir dos dados do banco de dados e realiza o pré-processamento.
    """
    # df2 = pd.read_csv("db/database/produtos.csv", sep=",")
    data = fetch_data("SELECT * FROM PRODUTOS")
    df = convert_data_to_df(data)
    df = preprocess_data(df)
    return df


def get_options():
    """
    Retorna as opções para o algoritmo de recomendação.
    """
    price_range = (10, 17)
    color = "navy"
    return {"price_range": price_range, "color": color}


def recomend_algorithm(df, price_range, color):
    """
    Algoritmo de recomendação que utiliza similaridade de cossenos.
    Retorna um DataFrame com as recomendações.
    """
    cosine_sim = calculate_cosine_similarity(df)
    recommendations = recommend_products(price_range, color, cosine_sim, df)
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


def get_recommendations():
    # Criação do DataFrame a partir dos dados do banco - dados pré-processados
    df = create_df()

    # Pegando as informações necessárias para o algorítimo de recomendação
    options = get_options()

    # Criando o DataFrame das recomendações do sistema
    df_recommendations = recomend_algorithm(
        df, options["price_range"], options["color"]
    )

    # Exibe as recomendações
    # show_recommendations(df_recommendations, options["price_range"], options["color"])

    json_recommendations = convert_df_to_json(df_recommendations)

    return json_recommendations
