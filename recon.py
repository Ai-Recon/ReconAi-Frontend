import pandas as pd
from flask import Flask, jsonify, render_template, request

from backend.src.main import get_recommendations

app = Flask(__name__, static_folder="static")

# Carregar os dados pré-processados e calculados de main.py
df_recomendacoes = pd.read_csv("backend\\src\\db\\database\\produtos.csv")


# Defina uma rota para processar a solicitação dos usuários e exibir as recomendações
@app.route("/")
def homepage():
    min_price = 0
    max_price = 1000
    return render_template("home.html", min_price=min_price, max_price=max_price)


# Defina uma rota para processar a solicitação dos usuários e exibir as recomendações
@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if request.method == "POST":
        # Extrair os parâmetros do formulário
        price_min = float(request.form.get("preco-minimo", 0))
        price_max = float(request.form.get("preco-maximo", 1000))
        color = request.form.get("color")

        # RECOMENDAÇÕES SEM AS OPÇÕES(PREÇO E COR) DO FRONT, USANDO AS DO BACK
        recommendations = get_recommendations()
        # DESCOBRIR COMO PEGAR AS OPÇÕES DO FRONT PARA USAR NO BACK
        print(
            "DADOS DO BANCO EM JSON = ", recommendations
        )  # printando as recomendações do back
        return render_template("usuarios.html")

    else:
        # Se for uma solicitação GET, retorne a página HTML
        return render_template("usuarios.html")


if __name__ == "__main__":
    app.run(debug=True)
