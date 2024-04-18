from flask import Flask, render_template, redirect

app = Flask(__name__, static_folder='static')

# Routes
@app.route("/")
def homepage():
    return render_template("login.html")

@app.route("/entrar", methods=['POST'])  # Handle form submission
def login():
    # Simulate login logic (replace with your authentication process)
    if True:  # Assuming successful login
        return redirect("/home")  # Redirect to home page on successful login
    else:
        # Handle unsuccessful login (show error message, etc.)
        return render_template("login.html", error="Invalid credentials")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/usuarios/<nome_usuario>")
def usuarios(nome_usuario):
    return render_template("usuarios.html", nome_usuario=nome_usuario)
    

#colocar site no ar
if __name__ == "__main__":
    app.run(debug=True)