# calculations.py
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(df):
    features = ["Preço_Normalizado", "Cor_Numérica"]
    X = df[features]
    cosine_sim = cosine_similarity(X, X)

    return cosine_sim
