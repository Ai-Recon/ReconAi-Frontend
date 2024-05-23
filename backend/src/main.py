from backend.src.db.db_functions import fetch_data
from backend.src.services.convert import convert_data_to_df, convert_df_to_json
from backend.src.services.recommend import filter_products, recommended_products

# Importações para debug
# from db.db_functions import fetch_data
# from services.convert import convert_data_to_df, convert_df_to_json
# from services.recommend import filter_products, recommended_products


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


def get_recommendations(chosen_product):
    """
    Obtém recomendações de produtos com base na roupa escolhida pelo usuário.
    """

    # Cria um DataFrame a partir dos dados do banco de dados
    df_products = create_df("SELECT * FROM PRODUTOS")

    # Obtém as recomendações de produtos com base na roupa escolhida
    df_recommendations = recommended_products(df_products, chosen_product)

    # Converte o DataFrame das recomendações para formato JSON
    json_recommendations = convert_df_to_json(df_recommendations)

    return json_recommendations
