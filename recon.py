from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

#criar a 1a pagina do site

#route -> caminho que vem depois do dominio
#função -> o que você quer exibir naquela página
#template 

@app.route("/")
def homepage():
    return render_template("login.html")

@app.route("/home")
def login():
    return render_template("home.html")

@app.route("/usuarios/<nome_usuario>")
def usuarios(nome_usuario):
    return render_template("usuarios.html", nome_usuario=nome_usuario)
    

#colocar site no ar
if __name__ == "__main__":
    app.run(debug=True)