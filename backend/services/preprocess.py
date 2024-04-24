# preprocessing.py
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


def normalize_prices(df):
    scaler = MinMaxScaler()
    df["Preço_Normalizado"] = scaler.fit_transform(df[["Preço"]])
    return df


def encode_colors(df):
    label_encoder = LabelEncoder()
    df["Cor_Numérica"] = label_encoder.fit_transform(df["Cor_do_Produto"])
    return df


def preprocess_data(df):
    df = normalize_prices(df)
    df = encode_colors(df)
    return df
