import os
import sqlite3
class PictureDatabase:
    SQL_CREATETABLE = """
    create table picturealbum (id integer autoincrement ,)
    """
    def __init__(self,dbpath):
        self.db = sqlite3.connect(dbpath)
        pass
    def on_create_database(self):
        pass

class PictureDao:
    def __init__(self,database):
        self.database = database

        pass