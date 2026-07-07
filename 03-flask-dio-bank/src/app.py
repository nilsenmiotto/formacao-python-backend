from flask import Flask, url_for, request

app = Flask(__name__)


@app.route("/olamundo/<string:usuario>/<int:idade>/<float:altura>")
def hello_world(usuario, idade, altura):
    print("tipo da variável usuario: ", type(usuario))
    print("tipo da variável idade: ", type(idade))
    print("tipo da variável altura: ", type(altura))
    return {
        "usuario" : usuario,
        "idade" : idade,
        "altura" : altura
    }


@app.route("/bem-vindo")
def bem_vindo():
    return {
        "message" : "Sejá bem vindo!"
    }


@app.route("/projects/")
def projects():
    return "The project page"


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return "GET The about page"
    else:
        return "POST The about page"


@app.route("/")
def index():
    return "index"


@app.route("/login")
def login():
    return "login"


@app.route("/user/<username>")
def profile(username):
    return f"{username}'s profile"


with app.test_request_context():
    print(url_for("index"))
    print(url_for("login"))
    print(url_for("login", next="/"))
    print(url_for("profile", username="John Doe"))
    print(url_for("hello_world", usuario="Alice", idade=30, altura=1.65))
