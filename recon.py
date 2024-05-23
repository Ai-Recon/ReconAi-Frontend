from flask import Flask, render_template, request

from backend.src.main import get_filtered_products, get_recommendations

# Inicializa a aplicação Flask e define o diretório estático
app = Flask(__name__, static_folder="static")


# Define uma rota /recomendacao
@app.route("/recomendacao", methods=["GET", "POST"])
def recomendacao():
    if request.method == "POST":
        # Extrai os parâmetros do formulário enviado pelo método POST
        price_min = float(request.form.get("preco-minimo", 0))
        price_max = float(request.form.get("preco-maximo", 1000))
        color = request.form.get("color")

        # Exibe os parâmetros extraídos
        print("Preço Mínimo:", price_min)
        print("Preço Máximo:", price_max)
        print("Cor Selecionada:", color)

        # Cria uma variável para guardar as opções de filtragem
        options = {"price_range": (float(price_min), float(price_max)), "color": color}

        # Obtém os produtos filtrados com base nas opções fornecidas
        filtered_products = get_filtered_products(options)

        # Verifica se não há produtos filtrados
        if not filtered_products:
            return render_template("recomendacao.html")

        return filtered_products

    else:
        # Se for uma solicitação GET, retorna a página HTML de recomendação
        return render_template("recomendacao.html")


# Define a rota /produto
@app.route("/produto")
def produto():
    # Obtém os dados do produto passadas pela URL
    ID = request.args.get("id")
    title = request.args.get("title")
    color = request.args.get("color")
    rating = request.args.get("rating")
    price = request.args.get("price")
    imagem = request.args.get("imagem")

    # Cria um dicionário contendo as informações da roupa escolhida
    chosen_product = {
        "ID": ID,
        "title": title,
        "color": color,
        "rating": rating,
        "price": price,
    }

    # Obtém as recomendações de produtos com base na roupa escolhida
    recommendations = get_recommendations(chosen_product)

    # Renderiza a página HTML passando os detalhes do produto e as novas recomendações
    return render_template(
        "produto.html",
        id=ID,
        title=title,
        color=color,
        rating=rating,
        price=price,
        imagem=imagem,
        recommendations=recommendations,
    )


# Define a rota inicial da aplicação
@app.route("/")
def inicio():
    # Renderiza a página HTML inicial
    return render_template("inicio.html")


# Inicia a execução da aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
