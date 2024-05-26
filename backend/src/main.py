from backend.src.db.db_functions import fetch_data
from backend.src.services.convert import (
    convert_data_to_df,
    convert_df_to_json,
    convert_dict_to_df,
)
from backend.src.services.recommend import filter_products, recommended_products


def create_df(query):
    """
    Cria um DataFrame a partir dos dados do banco de dados e realiza o pré-processamento.
    """

    data = fetch_data(query)
    df = convert_data_to_df(data)
    return df


def get_filtered_products(options):
    """
    Obtém os produtos filtrados com base nas opções fornecidas pelo usuário.
    """

    # Cria um DataFrame a partir dos dados do banco de dados
    df = create_df("SELECT * FROM PRODUTOS")

    # Filtra os produtos com base nas opções fornecidas pelo usuário
    df_filtered = filter_products(options["price_range"], options["color"], df)

    # Verifica se o DataFrame filtrado está vazio
    if df_filtered.empty:
        return

    # Converte o DataFrame filtrado para formato JSON
    json_filtered = convert_df_to_json(df_filtered)

    return json_filtered


def get_recommendations(dict_chosen_product):
    """
    Obtém recomendações de produtos com base na roupa escolhida pelo usuário.
    """

    # Cria um DataFrame a partir dos dados do banco de dados
    df_products = create_df("SELECT * FROM PRODUTOS")

    # Converte o dicionário do produto escolhido em um DataFrame
    df_chosen_product = convert_dict_to_df(dict_chosen_product)

    # Obtém as recomendações de produtos com base na roupa escolhida
    df_recommendations = recommended_products(df_products, df_chosen_product)

    # Converte o DataFrame das recomendações para formato JSON
    json_recommendations = convert_df_to_json(df_recommendations)

    return json_recommendations
