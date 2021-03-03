# flask and jsson
from flask import jsonify
import json
from types import SimpleNamespace

# csv stuff
from csv import writer
import pandas as pd

# Roba nostra
from model import Film, Utente
from dao import DAO
from clustering import fitModel

class Service:

    def __init__(self):
        self._dataset_dataframe = pd.read_csv("dataset.csv")
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

        self._dataset_dataframe = pd.read_csv("dataset.csv")

    def getSimilar(self, utente_id: str) -> list:
        self._dataset_dataframe['cluster'] = self._scaled_dataframe['cluster'].tolist()
        list_email = self._dataset_dataframe['email'].tolist()
        indice = list_email.index(utente_id)
        cluster_appartenenza = self._dataset_dataframe.iat[indice, 13]
        list_email_simili = self._dataset_dataframe.loc[self._dataset_dataframe['cluster'] == cluster_appartenenza, 'email'].tolist()
        return list_email_simili