from flask import Flask, jsonify, request
from dao import DAO
import json

from business import  Service 

"""
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
# Inizializzo il service
service = Service()

# Utilizzo del decoratore che ci consente di raggiungere l'app
@app.route("/")
def index():
    return "Le Iene IA"

@app.route("/consigliato", methods=["POST"])
def get_consigliati():
    data = json.dumps(request.get_json())  # DTO con utente, recensioni dell'utente

    utente = service.jsonToUtente(data)

    list_simili = service.getSimilar(utente.email)

    winner = service.rouletteWheel(list_simili, utente, dao)
    
    print("Winner:", winner)
    
    return str(winner)


if __name__ == "__main__":
    app.run()  