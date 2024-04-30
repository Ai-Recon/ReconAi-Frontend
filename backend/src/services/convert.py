import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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