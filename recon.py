from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, static_folder='static')

# Carregar os dados pré-processados e calculados de main.py
df_recomendacoes = pd.read_csv('backend\\src\\db\\database\\produtos.csv')

# Defina uma rota para processar a solicitação dos usuários e exibir as recomendações
@app.route("/")
def homepage():
    min_price = 0
    max_price = 1000
    return render_template("home.html", min_price=min_price, max_price=max_price)

# Defina uma rota para processar a solicitação dos usuários e exibir as recomendações
@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        # Extrair os parâmetros do formulário
        price_min = float(request.form.get('preco-minimo', 0))
        price_max = float(request.form.get('preco-maximo', 1000))
        color = request.form.get('color')

        # Filtrar recomendações com base nos parâmetros
        filtered_recommendations = df_recomendacoes[
            (df_recomendacoes['Preço'] >= price_min) &
            (df_recomendacoes['Preço'] <= price_max) &
            (df_recomendacoes['Cor_do_Produto'] == color)
        ]

        # Converter os dados filtrados em uma lista de dicionários
        recommendations = filtered_recommendations.to_dict(orient='records')

        # Retornar os dados no formato JSON
        return jsonify(recommendations)
    else:
        # Se for uma solicitação GET, retorne a página HTML
        return render_template("usuarios.html")

if __name__ == "__main__":
    app.run(debug=True)
