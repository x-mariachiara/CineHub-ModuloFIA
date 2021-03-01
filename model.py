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
    def __init__(self, email, dataNascita, hobby, sesso):
        self.email = email
        self.dataNascita = dataNascita
        self.hobby = hobby
        self.sesso = sesso

class Recensione:
    def __init__(self, createdAt, punteggio, film):
        self.createdAt = createdAt
        self.punteggio = punteggio
        self.film = film