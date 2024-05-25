import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def vectorize_features(data, Vectorizer):
    """
    Vetoriza os títulos do DataFrame ou do produto escolhido
    """
    if isinstance(data, pd.DataFrame):
        # Vetorizando os títulos do DataFrame em uma matriz
        matrix = Vectorizer.fit_transform(data["title"])

    elif isinstance(data, dict):
        # Vetorizando o título da roupa escolhida em uma matriz
        matrix = Vectorizer.transform([data["title"]])

    return matrix


def scale_features(data, Scaler):
    """
    Escala (padroniza) as características numéricas (preço e classificação) do DataFrame ou de um único produto escolhido
    """
    if isinstance(data, pd.DataFrame):
        # Seleciona as características do DataFrame
        numeric_features = data[["price", "rating"]]

        # Padronização das características
        numeric_features_scaled = Scaler.fit_transform(numeric_features)

    elif isinstance(data, dict):
        # Seleciona as características da roupa escolhida
        numeric_features = [[data["price"], data["rating"]]]

        # Padronização das características
        numeric_features_scaled = Scaler.transform(numeric_features)

    return numeric_features_scaled


def encode_features(data, Encoder):
    """
    Codifica as cores usando one-hot encoding para o DataFrame ou para um único produto escolhido
    """
    if isinstance(data, pd.DataFrame):
        # Codificação de cores para DataFrame
        color_features = data[["color"]]

        features_encoded = Encoder.fit_transform(color_features).toarray()
    elif isinstance(data, dict):
        # Codificação de cores para um único produto
        color_features = [[data["color"]]]

        features_encoded = Encoder.transform(color_features).toarray()

    return features_encoded


def combine_features(
    vectorized_titles,
    scaled_features,
    encoded_colors,
    Vectorizer,
    Encoder,
    is_dataframe=False,
    is_dict=False,
):
    """
    Combina os títulos, cores, preços e classificações em uma única matriz de características do DataFrame ou de um produto escolhido
    """
    if is_dataframe:
        # Cria um DataFrame das características e insere os títulos vetorizados
        feature_matrix = pd.DataFrame(
            vectorized_titles.toarray(), columns=Vectorizer.get_feature_names_out()
        )

        # Insere os preços e as classificações padronizadas no DataFrame criado
        feature_matrix = feature_matrix.join(
            pd.DataFrame(scaled_features, columns=["price", "rating"])
        )

        # Insere as cores codificadas no Dataframe
        feature_matrix = feature_matrix.join(
            pd.DataFrame(
                encoded_colors,
                columns=Encoder.get_feature_names_out(["color"]),
            )
        )

    if is_dict:
        # Cria um DataFrame das características e insere os títulos vetorizados
        feature_matrix = pd.DataFrame(
            [vectorized_titles.toarray()[0]],
            columns=Vectorizer.get_feature_names_out(),
        )

        # Insere os preços e as classificações padronizadas no DataFrame criado
        feature_matrix = feature_matrix.join(
            pd.DataFrame([scaled_features[0]], columns=["price", "rating"])
        )

        # Insere as cores codificadas no Dataframe
        feature_matrix = feature_matrix.join(
            pd.DataFrame(
                [encoded_colors[0]],
                columns=Encoder.get_feature_names_out(["color"]),
            )
        )

    return feature_matrix


def calculate_cosine_similarity(df_feature_matrix, chosen_product_matrix):
    """
    Calcula a similaridade de cossenos entre a roupa escolhida e todas as roupas no DataFrame
    """
    # Junta as matrizes de características em uma matriz principal
    main_matrix = pd.concat(
        [df_feature_matrix, chosen_product_matrix], ignore_index=True
    )

    # Calcula a similaridade de cossenos entre a roupa escolhida e todas as outras roupas
    similarity = cosine_similarity(main_matrix)

    return similarity[-1][:-1]


def get_cosine_similarity(df_products, chosen_product):
    # Inicializa o vetorizador TF-IDF
    Vectorizer = TfidfVectorizer()
    # Inicializa o escalonador (padronizador)
    Scaler = StandardScaler()
    # Inicializa o codificador one-hot
    Encoder = OneHotEncoder()

    # Vetoriza os títulos das roupas do DataFrame
    vectorized_df_titles = vectorize_features(df_products, Vectorizer)
    # Vetoriza o título da roupa escolhida
    vectorized_product_title = vectorize_features(chosen_product, Vectorizer)

    # Padroniza as classificações e os preços das roupas do DataFrame
    scaled_df_features = scale_features(df_products, Scaler)
    # Padroniza as classificação e o preço da roupa escolhida
    scaled_product_features = scale_features(chosen_product, Scaler)

    # Codifica as cores do DataFrame
    encoded_df_colors = encode_features(df_products, Encoder)
    # Codifica a cor da roupa escolhida
    encoded_product_color = encode_features(chosen_product, Encoder)

    # Combina as características do DataFrame em uma única matriz
    df_feature_matrix = combine_features(
        vectorized_df_titles,
        scaled_df_features,
        encoded_df_colors,
        Vectorizer,
        Encoder,
        is_dataframe=True,
    )
    # Combina as características da roupa escolhida em uma única matriz
    chosen_product_matrix = combine_features(
        vectorized_product_title,
        scaled_product_features,
        encoded_product_color,
        Vectorizer,
        Encoder,
        is_dict=True,
    )

    # Calcula a similaridade de cossenos entre a roupa escolhida e todas as roupas do DataFrame
    similarity = calculate_cosine_similarity(df_feature_matrix, chosen_product_matrix)

    # Cria um DataFrame com os títulos das roupas e suas respectivas similaridades
    df_similarity_clothes = pd.DataFrame(
        {"title": df_products["title"], "similarity": similarity}
    )

    # Ordena as roupas com base na similaridade em ordem decrescente
    df_similarity_clothes = df_similarity_clothes.sort_values(
        by="similarity", ascending=False
    )

    return df_similarity_clothes
