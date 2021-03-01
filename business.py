from flask import jsonify
from model import Film, Utente
from dao import DAO

def getAllFilm(dao):
    lista_film = DAO.select_all_film()
    lista_json = []
    for film in lista_film:
        lista_json.append(Film.serialize_film(film))
    return lista_json

def getUtenteByID(email: str):
    utente_raw = DAO.select_recensore_by_id(email)
    print(utente_raw)
    utente = Utente(utente_raw[1], utente_raw[3], utente_raw[4], utente_raw[8])
    return utente

def getFasciaEta():
    pass