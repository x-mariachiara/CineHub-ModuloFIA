from flask import Flask
from flask import render_template
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
        list_film = DAO.__cursor_instance.fetchall()
        return list_film