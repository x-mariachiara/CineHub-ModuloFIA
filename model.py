from collections import namedtuple

class Film:
    def __init__(self, id, titolo, annoUscita, sinossi, linkTrailer, linkLocandina, mediaVoti, visibile):
        self.id = id
        self.titolo = titolo
        self.annoUscita = annoUscita
        self.sinossi = sinossi
        self.linkTrailer = linkTrailer
        self.linkLocandina = linkLocandina
        self.mediaVoti = mediaVoti
        self.visibile = visibile


    def serialize_film(film) -> dict:
        film_dict = {}
        for attr in vars(film):
            attr_value = getattr(film, attr)
            film_dict[attr] = attr_value
        return film_dict

class Utente:
    def __init__(self, email: str, hobby: int, sesso: int, genere_preferito: str, eta: str, id_film_visti: list, id_attori_preferiti: list):
        self.email = email
        self.hobby = hobby
        self.sesso = sesso
        self.genere_preferito = genere_preferito
        self.eta = eta
        self.id_film_visti = id_film_visti
        self.id_attori_preferiti = id_attori_preferiti


class Recensione:
    def __init__(self, createdAt, punteggio, film):
        self.createdAt = createdAt
        self.punteggio = punteggio
        self.film = film