from flask import Flask, jsonify
from dao import DAO

"""
Dati di esempio  ovviamente questo contatta il database e da li prende i film che
hanno determinato genere, attore ecc..
"""
books = [
    {
        "id": 1,
        "title": "Harry Potter and the Goblet of Fire",
        "author": "J.K. Rowling",
        "isbn": "1512379298"
    },
    {
        "id": 2,
        "title": "Lord of the Flies",
        "author": "William Golding",
        "isbn": "0399501487"
    }
]

# Creazione nuova app usando il costruttore
app = Flask(__name__)
dao = DAO()

# Utilizzo del decoratore che ci consente di raggiungere l'app
@app.route("/")
def index():
    return "Le Iene IA"

# Per creare un REST endpoint uso app.route(path, methods=["GET|POST"])
@app.route("/consigliati", methods=["GET"])
def get_consigliati():
    return jsonify({"books": books})

if __name__ == "__main__":
    app.run()