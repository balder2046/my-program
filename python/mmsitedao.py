import os
import sqlite3
class PictureDatabase:

    def __init__(self,dbpath):
        self.conn = sqlite3.connect(dbpath)
        pass


class AlbumSummeryDao:
    SQL_CREATE_TABLE = 'create table if not exists album_summery(id INTEGER PRIMARY  KEY autoincrement,' \
                       'title TEXT not null, url TEXT not null UNIQUE,thumburl TEXT not null )'
    SQL_INSERT_ALBUM = 'insert into album_summery(title,url,thumburl) values(?,?,?)'
    SQL_QUERY_ALBUM_EXIST = 'select id from album_summery where url = ?'
    def __init__(self,database):
        self.database = database
        self.conn = database.conn
        self.cursor = self.conn.cursor()
        self.cursor.execute(AlbumSummeryDao.SQL_CREATE_TABLE)
        self.conn.commit()
        pass
    def add_album(self,title,url,thumburl):
        self.cursor.execute(AlbumSummeryDao.SQL_INSERT_ALBUM,(title,url,thumburl))
        self.conn.commit()

    def is_album_exist(self,url):
        print(type(url))
        self.cursor.execute(AlbumSummeryDao.SQL_QUERY_ALBUM_EXIST,(url,))
        res = self.cursor.fetchone()
        return res is not None