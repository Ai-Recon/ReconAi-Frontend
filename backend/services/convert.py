import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db_functions import fetch_data


def convert_data_to_df():
    produtos = fetch_data("SELECT * FROM PRODUTOS")

    if produtos:
        # Convertendo para DataFrame
        df = pd.DataFrame(
            produtos, columns=["ID", "Titulo", "Preco", "Classificacao", "Cor"]
        )

    return df


if __name__ == "__main__":
    print(convert_data_to_df())
