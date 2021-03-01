from flask import Flask, jsonify, request
from dao import DAO

from business import getAllFilm

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


# Creazione nuova app usando il costruttore
app = Flask(__name__)
# Inizzializzo connessione al db
dao = DAO()

# Utilizzo del decoratore che ci consente di raggiungere l'app
@app.route("/")
def index():
    return "Le Iene IA"

# Per creare un REST endpoint uso app.route(path, methods=["GET|POST"])
@app.route("/consigliati", methods=["POST"])
def get_consigliati():
    data = request.get_json() # DTO con utente, recensioni dell'utente
    # metodo di business che interroga il cluster prende i film da consigliare
    # metodo di business che sceglie il film

    #ritorniamo il film consigliato
    return jsonify({"films": getAllFilm(dao)})

@app.route("/ciao", methods=["GET"])
def get_recensioni():
    print(DAO.select_recensioni_by_recensore("edrioe@gmail.com"))
    return "ciao"

if __name__ == "__main__":
    app.run()