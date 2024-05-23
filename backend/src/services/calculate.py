import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


def vectorize_text(df_products, tfidf_vectorizer):
    """
    Vetoriza os títulos do DataFrame
    """

    # Vetorização dos títulos das roupas usando TF-IDF
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_products["title"])

    return tfidf_matrix


def scale_number(df_products, scaler):
    """
    Escala (padroniza) as características numéricas (preço e classificação) do DataFrame
    """

    # Seleciona as características numéricas (price e rating)
    numeric_features = df_products[["price", "rating"]]

    # Escalonamento das características numéricas (padronização)
    numeric_features_scaled = scaler.fit_transform(numeric_features)

    return numeric_features_scaled


def combine_features(tfidf_matrix, tfidf_vectorizer, numeric_features_scaled):
    """
    Combina os títulos com os preços e classificações em uma única matriz de características
    """

    # Combina os tpitulos, preços e classificações em uma única matriz
    feature_matrix = pd.DataFrame(
        tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out()
    ).join(pd.DataFrame(numeric_features_scaled, columns=["price", "rating"]))

    return feature_matrix


def vectorize_chosen_product(chosen_product, tfidf_vectorizer, scaler):
    """
    Vetoriza as características da roupa escolhida
    """

    # Vetoriza os títulos da roupa escolhida
    vectorized_chosen_product = tfidf_vectorizer.transform([chosen_product["title"]])

    # Converte a matriz vetorizada em um DataFrame
    vectorized_chosen_product = pd.DataFrame(
        vectorized_chosen_product.toarray(),  # Converte para um array utilizando NumPy
        columns=tfidf_vectorizer.get_feature_names_out(),  # Obtém os nomes das características
    )

    # Escala (padroniza) o preço e a classificação da roupa escolhida
    scaled_product_price_and_rating = scaler.transform(
        [[chosen_product["price"], chosen_product["rating"]]]
    )

    # Adiciona a característica de preço normalizada
    vectorized_chosen_product["price"] = scaled_product_price_and_rating[0][0]

    # Adiciona a característica de rating normalizada
    vectorized_chosen_product["rating"] = scaled_product_price_and_rating[0][1]

    # Retorna o DataFrame com as características vetorizadas e padronizadas
    return vectorized_chosen_product


def calculate_cossine_similarity(feature_matrix, vectorized_chosen_product):
    """
    Calcula a similaridade de cossenos entre a roupa escolhida e todas as roupas no DataFrame
    """

    # Concatena a matriz de características e a roupa escolhida
    combined_matrix = pd.concat(
        [feature_matrix, vectorized_chosen_product], ignore_index=True
    )

    # Calcula a similaridade de cossenos entre a roupa escolhida e todas as outras roupas
    similarity = cosine_similarity(combined_matrix)

    return abs(similarity[-1][:-1])  # Transforma os valores em absolutos


def get_cossine_similarity(df_products, chosen_product):
    """
    Calcula a similaridade entre a roupa escolhida e todas as roupas no DataFrame
    """

    # Inicializa o vetorizador TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    # Vetoriza os títulos das roupas do DataFrame
    tfidf_matrix = vectorize_text(df_products, tfidf_vectorizer)

    # Inicializa o escalonador (padronizador)
    scaler = StandardScaler()

    # Escala (padroniza) as classificações e os preçoes das roupas do DataFrame
    numeric_features_scaled = scale_number(df_products, scaler)

    # Combina os títulos com as classificações e os preços das roupas em uma única matriz de características
    feature_matrix = combine_features(
        tfidf_matrix, tfidf_vectorizer, numeric_features_scaled
    )

    # Vetoriza as características da roupa escolhida
    vectorized_chosen_product = vectorize_chosen_product(
        chosen_product, tfidf_vectorizer, scaler
    )

    # Calcula a similaridade de cossenos entre a roupa escolhida e todas as roupas do DataFrame
    similarity = calculate_cossine_similarity(feature_matrix, vectorized_chosen_product)

    # Cria um DataFrame com os títulos das roupas e suas respectivas similaridades
    df_similarity_clothes = pd.DataFrame(
        {"title": df_products["title"], "similarity": similarity}
    )

    # Ordena as roupas com base na similaridade em ordem decrescente
    df_similarity_clothes = df_similarity_clothes.sort_values(
        by="similarity", ascending=False
    )

    return df_similarity_clothes
