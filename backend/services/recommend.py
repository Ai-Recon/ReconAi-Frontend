# recommendations.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def recommend_products(price_range, color, similarity_matrix, df):
    # Filtrando produtos dentro do intervalo de preço e com a cor desejada
    filtered_products = df[
        (df["Preço"] >= price_range[0])
        & (df["Preço"] <= price_range[1])
        & (df["Cor_do_Produto"] == color)
    ]

    # Imprimindo o número de produtos filtrados
    print("Número de produtos filtrados:", len(filtered_products))

    # Se não houver produtos que correspondam aos critérios, retornar uma mensagem
    if filtered_products.empty:
        return "Não há produtos disponíveis com os critérios selecionados."

    # Convertendo os índices dos produtos filtrados para os índices corretos na matriz de similaridade
    indices_in_similarity_matrix = [
        df.index.get_loc(idx) for idx in filtered_products.index
    ]

    # Calculando a média da similaridade de cossenos e da classificação para cada produto filtrado
    avg_similarity_scores = []
    avg_ratings = []
    for idx in indices_in_similarity_matrix:
        avg_similarity_scores.append(similarity_matrix[idx, :].mean())
        avg_ratings.append(df.iloc[idx]["Classificação"])  # Adicionando a classificação

    # Normalizando as classificações
    rating_scaler = MinMaxScaler()
    avg_ratings_normalized = rating_scaler.fit_transform(
        np.array(avg_ratings).reshape(-1, 1)
    ).flatten()

    # Calculando um score combinado baseado na média da similaridade e na classificação
    combined_scores = [
        0.5 * sim + 0.5 * rating
        for sim, rating in zip(avg_similarity_scores, avg_ratings_normalized)
    ]

    # Ordenando os produtos com base no score combinado
    recommended_indices = sorted(
        zip(filtered_products.index, combined_scores), key=lambda x: x[1], reverse=True
    )

    # Extraindo os títulos dos produtos recomendados
    recommended_titles = [df.loc[idx] for idx, _ in recommended_indices]

    return recommended_titles
