import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder


def unify_dfs(df_products, df_chosen_product):
    """
    Unifica o DataFrame dos produtos com o DataFrame do produto escolhido
    """
    unified_df = pd.concat([df_chosen_product, df_products], ignore_index=True)
    return unified_df


def vectorize_features(df, Vectorizer):
    """
    Vetoriza os títulos do DataFrame
    """
    # Vetorizando os títulos do DataFrame em uma matriz
    matrix = Vectorizer.fit_transform(df["title"])
    return matrix


def normalize_features(df, Scaler):
    """
    Normaliza as características numéricas (preço e classificação) do DataFrame
    """
    # Seleciona as características do DataFrame
    numeric_features = df[["price", "rating"]]

    # Normalização das características
    numeric_features_normalized = Scaler.fit_transform(numeric_features)
    return numeric_features_normalized


def encode_features(df, Encoder):
    """
    Codifica as cores usando one-hot encoding para o DataFrame
    """
    # Seleciona as características do DataFrame
    features = df[["color"]]

    # Codifica as características
    features_encoded = Encoder.fit_transform(features).toarray()
    return features_encoded


def combine_features(
    vectorized_titles, normalized_price_and_rating, encoded_colors, Vectorizer, Encoder
):
    """
    Combina os dados tratados (títulos, cores, preços e classificações) em um único Dataframe de características
    """
    # Cria um DataFrame das características e insere os títulos vetorizados
    df_features = pd.DataFrame(
        vectorized_titles.toarray(), columns=Vectorizer.get_feature_names_out()
    )

    # Insere os preços e as classificações normalizadas no DataFrame criado
    df_features = df_features.join(
        pd.DataFrame(normalized_price_and_rating, columns=["price", "rating"])
    )

    # Insere as cores codificadas no Dataframe criado
    df_features = df_features.join(
        pd.DataFrame(
            encoded_colors,
            columns=Encoder.get_feature_names_out(["color"]),
        )
    )
    return df_features


def calculate_cosine_similarity(df_features):
    """
    Calcula a similaridade de cossenos entre todos os produtos do DataFrame
    """
    similarity = cosine_similarity(df_features)

    # Retorna apenas a similaridade do primeiro produto do Dataframe - produto escolhido
    return similarity[0][1:]


def get_cosine_similarity(df_products, df_chosen_product):
    # Inicializa o vetorizador TF-IDF
    Vectorizer = TfidfVectorizer()
    # Inicializa o escalonador (normalizador)
    Scaler = MinMaxScaler()
    # Inicializa o codificador one-hot
    Encoder = OneHotEncoder()

    # Unifica o DataFrame dos produtos com o do produto escolhido
    unified_df = unify_dfs(df_products, df_chosen_product)

    # Vetoriza os títulos do DataFrame
    vectorized_df_titles = vectorize_features(unified_df, Vectorizer)

    # Normaliza as classificações e os preços do DataFrame
    normalized_df_price_and_rating = normalize_features(unified_df, Scaler)

    # Codifica as cores do DataFrame
    encoded_df_colors = encode_features(unified_df, Encoder)

    # Combina as características em um único DataFrame
    df_features = combine_features(
        vectorized_df_titles,
        normalized_df_price_and_rating,
        encoded_df_colors,
        Vectorizer,
        Encoder,
    )

    # Calcula a similaridade de cossenos entre o produto escolhido e todas as roupas do DataFrame
    similarity = calculate_cosine_similarity(df_features)

    # Cria um DataFrame com os títulos das roupas e suas respectivas similaridades
    df_similarity_clothes = pd.DataFrame(
        {"title": df_products["title"], "similarity": similarity}
    )

    return df_similarity_clothes
