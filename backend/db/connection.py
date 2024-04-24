import os
import time

import psycopg2
from dotenv import load_dotenv

# Carregando as variáveis de ambiente
load_dotenv()

start_time = time.time()

# Conectando ao banco de dados
try:
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )
    # Criando um cursor para executar consultas SQL
    cursor = conn.cursor()

    # Consulta SQL para selecionar todos os dados da tabela "produtos"
    query = "SELECT * FROM produtos;"

    # Executando a consulta SQL
    cursor.execute(query)

    # Recuperando os resultados da consulta
    produtos = cursor.fetchall()

    # Exibindo os resultados
    for produto in produtos:
        print(produto)

    # Fechando o cursor e a conexão
    cursor.close()
    conn.close()

    # Fim da contagem de tempo
    end_time = time.time()
    # Calculando o tempo total de execução
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time:.4f} segundos")

except psycopg2.Error as e:
    print("Erro ao conectar ao PostgreSQL:", e)
