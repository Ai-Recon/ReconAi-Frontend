from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, static_folder='static')

# Carregar os dados pré-processados e calculados de main.py
df_recomendacoes = pd.read_csv('backend\db\database\produtos.csv')

# Defina uma rota para processar a solicitação dos usuários e exibir as recomendações


@app.route("/")
def homepage():
    min_price = 0
    max_price = 1000
    return render_template("home.html", min_price=min_price, max_price=max_price)

# Defina uma rota para processar a solicitação dos usuários e exibir as recomendações
@app.route("/usuarios/<nome_usuario>")
def usuarios(nome_usuario):
    # Obter os parâmetros da solicitação
    price_min = float(request.args.get('price_min', 0))
    price_max = float(request.args.get('price_max', 1000))
    color = request.args.get('color', 'navy')
    
    # Filtrar recomendações com base nos parâmetros
    filtered_recommendations = df_recomendacoes[
        (df_recomendacoes['Preço'] >= price_min) &
        (df_recomendacoes['Preço'] <= price_max) &
        (df_recomendacoes['Cor_do_Produto'] == color)
    ]
    
    # Converter os dados filtrados em uma lista de dicionários
    recommendations = filtered_recommendations.to_dict(orient='records')
    
    return render_template("usuarios.html", nome_usuario=nome_usuario, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
