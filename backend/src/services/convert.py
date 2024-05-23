import pandas as pd


def convert_data_to_df(data):
    """
    Converte os dados dos Banco para um DataFrame
    """
    if data:
        df = pd.DataFrame(
            data,
            columns=[
                "id",
                "title",
                "price",
                "rating",
                "color",
            ],
        )
        print("Sucesso ao converter os dados!")
        return df


def convert_df_to_json(df):
    """
    Converte os dados do DataFrame para JSON
    """
    json_data = df.to_json(orient="records")
    return json_data


def convert_json_to_df(json):
    """
    Converte os dados do DataFrame para JSON
    """
    df = pd.DataFrame(json)
    return df
