from flask import Flask, jsonify
from dao import DAO

from business import printHello
"""
Una possibile idea:
Cluster -> tutti gli elementi nello stesso cluster potrebbero avere gusti simili in termini di film
allora dato un utente, la sua lista delle recensioni e la lista di media che ha recensito

Poi in base a quale cluster si trova gli andiamo a consigliare i film che gli utenti nello 
stesso cluster hanno visto e recensito positivamente. Di quella lista di film ne scegliamo uno andando:
- a scartare quelli che l'utente ha gia' recensito,
- ad assegnare una maggiore probabilita' a quelli che hanno lo stesso genere dei film recensiti dall'utente con più recensioni positive
- ad assegnare una maggiore probabilita' a quelli che hanno attori in comune dei film recensiti dall'utente con più recensioni positive
"""

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
    printHello()
    print(DAO.select_all_film())
    return jsonify({"books": books})

if __name__ == "__main__":
    app.run()