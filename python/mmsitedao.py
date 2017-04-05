import os
import sqlite3
class PictureDatabase:

    def __init__(self,dbpath):
        self.conn = sqlite3.connect(dbpath)
        pass

class AlbumTagsDao:
    SQL_CREATE_TABLE = 'create table if not exists album_tag(id integer PRIMARY key autoincrement,url text not null,tag text not null);'
    SQL_QUERY_TAG_EXIST = 'select id from album_tag where url = ? and tag = ?'
    SQL_INSERT_ALBUM_TAG = 'insert into album_tag(url,tag) values(?,?)'
    def __init__(self,database):
        self.database = database
        self.conn = database.conn
        self.cursor = self.conn.cursor()
        self.cursor.execute(AlbumTagsDao.SQL_CREATE_TABLE)
        self.conn.commit()
    def insert_tag(self,url,tagname):
        if not self.is_tag_exist(url,tagname):
            self.cursor.execute(AlbumTagsDao.SQL_INSERT_ALBUM_TAG,(url,tagname))
            self.conn.commit()
        pass

    def is_tag_exist(self,url,tagname):
        self.cursor.execute(AlbumTagsDao.SQL_QUERY_TAG_EXIST,(url,tagname))
        return self.cursor.fetchone() is not None

class AlbumSummeryDao:
    SQL_CREATE_TABLE = 'create table if not exists album_summery(id INTEGER PRIMARY  KEY autoincrement,' \
                       'title TEXT not null, url TEXT not null UNIQUE,thumburl TEXT not null ,piccount INTEGER)'
    SQL_INSERT_ALBUM = 'insert into album_summery(title,url,thumburl,piccount) values(?,?,?,?)'
    SQL_QUERY_ALBUM_EXIST = 'select id from album_summery where url = ?'
    def __init__(self,database):
        self.database = database
        self.conn = database.conn
        self.cursor = self.conn.cursor()
        self.cursor.execute(AlbumSummeryDao.SQL_CREATE_TABLE)
        self.conn.commit()
        pass
    def add_album(self,title,url,thumburl,piccount):
        self.cursor.execute(AlbumSummeryDao.SQL_INSERT_ALBUM,(title,url,thumburl,piccount))
        self.conn.commit()

    def is_album_exist(self,url):
        print(type(url))
        self.cursor.execute(AlbumSummeryDao.SQL_QUERY_ALBUM_EXIST,(url,))
        res = self.cursor.fetchone()
        return res is not None
