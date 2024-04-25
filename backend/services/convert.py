import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db_functions import fetch_data


def convert_data_to_df(data):
    if data:
        # Convertendo para DataFrame
        df = pd.DataFrame(
            data,
            columns=[
                "ID_do_Produto",
                "Título",
                "Preço",
                "Classificação",
                "Cor_do_Produto",
            ],
        )

        print("Sucesso ao converter os dados!")

        return df
