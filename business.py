from random import Random

# flask and json
from flask import jsonify
import json
from types import SimpleNamespace
import requests as req

# csv stuff
from csv import writer
import pandas as pd

# Roba nostra
from model import Film, Utente, Spicchio
from clustering import fitModel

class Service:

    def __init__(self):
        #self._dataset_dataframe = pd.read_csv("dataset.csv")
        r = req.get("http://localhost:8080/api/utentecontrol/exportData")
        json_data = json.loads(r.text)
        print(json_data.keys())
        self._dataset_dataframe = pd.DataFrame(json_data["data"], columns = json_data["feature_names"])
        self._scaled_dataframe = None
        self.similarList = []

    def getAllFilm(self, dao):
        lista_film = DAO.select_all_film()
        lista_json = []
        for film in lista_film:
            lista_json.append(Film.serialize_film(film))
        return lista_json

    def getUtenteByID(self, email: str):
        utente_raw = DAO.select_recensore_by_id(email)
        print(utente_raw)
        utente = Utente(utente_raw[1], utente_raw[3], utente_raw[4], utente_raw[8])
        return utente

    def jsonToUtente(self, data: str):
        print("PRE JSONIFY:", data)
        utente_raw = json.loads(data, object_hook= lambda d: SimpleNamespace(**d))
        utente = Utente(utente_raw.email, utente_raw.hobby, utente_raw.sesso, utente_raw.generePreferito, utente_raw.fasciaEta, utente_raw.idFilmVisti, utente_raw.idAttoriPreferiti)
        return utente

    def addLineToCSV(self, utente):
        list_of_elem = [utente.email, "", "", "", utente.sesso, utente.eta, utente.genere_preferito, "", utente.hobby, "", "", "", ""]

        list_email = self._dataset_dataframe['email'].tolist()
        if utente.email in list_email:
            index = list_email.index(utente.email)
            self._dataset_dataframe.iat[index,5] = utente.eta
            self._dataset_dataframe.iat[index, 6] = utente.genere_preferito
            self._dataset_dataframe.to_csv('datasetModificato.csv', index=False)
        else:
            with open('dataset.csv', 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                csv_writer.writerow(list_of_elem)
            *r, self._scaled_dataframe = fitModel(n_cluster=10)
        if(self._scaled_dataframe is None):
            *r, self._scaled_dataframe = fitModel(n_cluster=10)

        self._dataset_dataframe = pd.read_csv("dataset.csv")

    def getSimilar(self, utente_id: str) -> list:
        *r, self._scaled_dataframe = fitModel(n_cluster=10)
        self._dataset_dataframe['cluster'] = self._scaled_dataframe['cluster']
        self._dataset_dataframe.info()
        list_email = self._dataset_dataframe['email'].tolist()
        indice = list_email.index(utente_id)
        cluster_appartenenza = self._dataset_dataframe.iat[indice, 7]
        list_email_simili = self._dataset_dataframe.loc[self._dataset_dataframe['cluster'] == cluster_appartenenza, 'email'].tolist()
        return list_email_simili

    def getPunteggioFilm(self, idFilm, utente, dao):
        list_generi = [i[0] for i in dao.select_generi_film(idFilm)]
        list_attori_film = [i[0] for i in dao.select_attori_film(idFilm)]
        base = 5
        if utente.genere_preferito in list_generi:
            base += 5
        if any(item in list_attori_film for item in utente.id_attori_preferiti[:4]):
            base += 5
        if base == 5:
            base -= 3

        return base

        

    def rouletteWheel(self, lista_simi: list, utente, dao) -> float:

        ruota = []
        posizione = 0.0
        lista_film_consigliati = set()

        for u in lista_simi:
            for film in self._dataset_dataframe.iat[lista_simi.index(u), 5]:
                if not film in utente.id_film_visti:
                    lista_film_consigliati.add(film)
        print(lista_film_consigliati)
        
        totalePunteggi = sum([self.getPunteggioFilm(x, utente, dao) for x in lista_film_consigliati])

        for idFilm in lista_film_consigliati:
            punteggio_film = self.getPunteggioFilm(idFilm, utente, dao)
            ruota.append(Spicchio(posizione, punteggio_film / totalePunteggi, idFilm))
            posizione += punteggio_film / totalePunteggi

        
        randomGenerator = Random()
        
        randomNumber = round(randomGenerator.uniform(0, 1), 6)

        for index, spicchio in enumerate(ruota):
            print("iterazione: ", index, "\tspicchio tra: ", spicchio.posizioneIniziale, "e: ", (spicchio.posizioneIniziale + spicchio.lunghezza), "\testratto:", randomNumber)
            if spicchio.posizioneIniziale <= randomNumber < (spicchio.posizioneIniziale + spicchio.lunghezza):
                return spicchio.idFilm  
