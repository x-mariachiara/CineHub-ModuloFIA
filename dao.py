from flask import Flask
from flask import render_template

from model import Film
import psycopg2

class DAO:

    # Sigleton per fare in modo che son si creino più connessioni al database
    class __cursor:
        def obtain_cursor():
            t_host = "127.0.0.1"
            t_port = "5432"
            t_dbname = "cinehub"
            t_user = "postgres"
            t_password = "password"

            db_connection = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_password)
            db_cursor = db_connection.cursor()
            return db_cursor

    __cursor_instance = None

    def __init__(self):
        if DAO.__cursor_instance is None:
            DAO.__cursor_instance = DAO.__cursor.obtain_cursor()
        
        self.__dict__['_DAO__cursor_instance'] = DAO.__cursor_instance

    def checkDAO():
        print("Instanza del cursore:", DAO.__cursor_instance)

    def select_all_film() -> list:
        s = "SELECT * FROM film"
        DAO.__cursor_instance.execute(s)
        list_film = []
        for item in DAO.__cursor_instance.fetchall():
            list_film.append(Film(item[0], item[6], item[1], item[5], item[3], item[2], item[4], item[7]))
        
        return list_film

    def select_all_film() -> list:
        s = "SELECT * FROM film"
        DAO.__cursor_instance.execute(s)
        list_film = []
        for item in DAO.__cursor_instance.fetchall():
            list_film.append(Film(item[0], item[6], item[1], item[5], item[3], item[2], item[4], item[7]))
        
        return list_film

    def select_recensioni_by_recensore(recensore_email: str) -> list:
        DAO.__cursor_instance.execute("SELECT punteggio, film_id FROM recensione where recensore_email = %s", (recensore_email,))
        return DAO.__cursor_instance.fetchall()

    def select_attori_film(film_id: int) -> list:
        DAO.__cursor_instance.execute("SELECT cast_id FROM ruolo where media_id = %s", (film_id,))
        return DAO.__cursor_instance.fetchall()

    def select_generi_film(film_id: int) -> list:
        DAO.__cursor_instance.execute("SELECT genere_id FROM media_genere where media_id = %s", (film_id,))
        return DAO.__cursor_instance.fetchall()

    def select_recensore_by_id(email: str):
        DAO.__cursor_instance.execute("SELECT * FROM utente where email = %s", (email,))
        return DAO.__cursor_instance.fetchone()

