import pandas as pd
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# carrega com os dados do csv
from backend.src.main_csv import get_recommendations

# carrega com os dados do banco
# from backend.src.main_db import get_recommendations


app = Flask(__name__, static_folder="static")

app.secret_key = "PUC"

# Carregar os dados pré-processados e calculados de main.py
# df_recomendacoes = pd.read_csv("backend\\src\\db\\database\\produtos.csv")


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

        # Agora você tem acesso ao preço mínimo, preço máximo e cor selecionada pelo usuário
        print("Preço Mínimo:", price_min)
        print("Preço Máximo:", price_max)
        print("Cor Selecionada:", color)

        options = {"price_range": (price_min, price_max), "color": color}

        recommendations = get_recommendations(options)

        if not recommendations:
            return render_template("usuarios.html")

        return recommendations

    else:
        # Se for uma solicitação GET, retorne a página HTML
        return render_template("usuarios.html")


# @app.route(
#     "/autenticar",
#     methods=[
#         "POST",
#     ],
# )
# def autenticar():
#     if "PUC" == request.form["senha"]:
#         session["usuario_logado"] = request.form["usuario"]
#         flash(session["usuario_logado"] + " logado com sucesso!")
#         return redirect("/")
#     else:
#         flash("Usuário não logado")
#         return redirect("/login")


# @app.route("/login")
# def login():
#     return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
