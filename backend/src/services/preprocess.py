# preprocessing.py
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


def normalize_prices(df):
    """
    Normaliza a coluna de Preços do DataFrame
    """
    scaler = MinMaxScaler()
    df["normalized_price"] = scaler.fit_transform(df[["price"]])
    return df


def encode_colors(df):
    """
    Tranforma os valores da coluna de Cores do DataFrame em valores numéricos
    """
    label_encoder = LabelEncoder()
    df["numeric_color"] = label_encoder.fit_transform(df["color"])
    return df


def preprocess_data(df):
    df = normalize_prices(df)
    df = encode_colors(df)
    return df
