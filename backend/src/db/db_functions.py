import os
import time

import psycopg2
from dotenv import load_dotenv


def connect_to_database():
    """
    Conecta com o Postgres
    """
    load_dotenv()
    start_time = time.time()
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )
        if conn:
            print("Sucesso ao conectar com o banco!", end=" | ")
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Tempo de execução: {execution_time:.4f} segundos")
            return conn

    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)
        return None


def fetch_data(sql_query):
    """
    Buscando dados no Banco
    """
    conn = connect_to_database()
    if conn:
        start_time = time.time()
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            if result:
                print("Sucesso na busca dos dados!", end=" | ")

                cursor.close()
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Tempo de execução: {execution_time:.4f} segundos")

                # Fechando a conexão
                conn.close()
                return result

        except psycopg2.Error as e:
            print("Erro ao executar a consulta SQL:", e)
            return None
    else:
        print("Erro com a conexão")
        return None
