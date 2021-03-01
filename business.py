from flask import jsonify
from model import Film
from dao import DAO

def getAllFilm(dao):
    lista_film = DAO.select_all_film()
    lista_json = []
    for film in lista_film:
        lista_json.append(Film.serialize_film(film))
    return lista_json