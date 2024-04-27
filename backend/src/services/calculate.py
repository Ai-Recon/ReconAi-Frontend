# calculations.py
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(df):
    """
    Calcula a similaridade de cossenos entre os produtos baseada nas cores e nos preços
    """
    features = ["normalized_price", "numeric_color"]
    X = df[features]
    cosine_sim = cosine_similarity(X, X)

    return cosine_sim
