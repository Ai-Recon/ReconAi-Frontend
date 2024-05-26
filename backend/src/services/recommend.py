from backend.src.services.calculate import get_cosine_similarity


def recommended_products(df_products, df_chosen_product):
    """
    Obtém os produtos recomendados com base na roupa escolhida pelo usuário
    """
    # Calcula a similaridade de cossenos entre a roupa escolhida e todos os produtos no DataFrame
    cossine_sim = get_cosine_similarity(df_products, df_chosen_product)

    # Adiciona uma coluna de similaridade ao DataFrame original
    df_products["similarity"] = cossine_sim["similarity"]

    # Organiza os produtos com base na similaridade, do maior para o menor
    df_products = df_products.sort_values(by="similarity", ascending=False)

    # Retorna o DataFrame com os produtos recomendados
    return df_products


def filter_products(price_range, color, df_products):
    """
    Filtra os produtos com base na faixa de preço e na cor especificadas
    """
    # Filtragem dos dados (intervalo de preço e cor)
    df_filtered_products = df_products[
        (df_products["price"] >= price_range[0])
        & (df_products["price"] <= price_range[1])
        & (df_products["color"] == color)
    ]

    # Organiza os produtos filtrados com base na classificação, do maior para o menor
    df_filtered_products = df_filtered_products.sort_values(
        by="rating", ascending=False
    )

    # Retorna o DataFrame com os produtos filtrados
    return df_filtered_products
