import os
import time

import pandas as pd
import psycopg2
from dotenv import load_dotenv


# Conexão com o Postgres
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )
        return conn

    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)
        return None


def fetch_data(conn):
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM produtos;"
            cursor.execute(query)
            produtos = cursor.fetchall()
            cursor.close()
            return produtos

        except psycopg2.Error as e:
            print("Erro ao executar a consulta SQL:", e)
            return None
    else:
        print("Erro com a conexão", conn)
        return None


def main():
    # Carregando as variáveis de ambiente
    load_dotenv()

    start_time = time.time()

    # Conectando ao banco de dados
    conn = connect_to_database()

    # Recuperando os resultados da consulta
    produtos = fetch_data(conn)

    if produtos:
        # Convertendo para DataFrame
        df = pd.DataFrame(
            produtos, columns=["ID", "Titulo", "Preco", "Classificacao", "Cor"]
        )
        print(df)

    # Fechando a conexão
    if conn:
        conn.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time:.4f} segundos")


if __name__ == "__main__":
    main()
