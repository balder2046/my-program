import os
import sqlite3
import picturemanager
class PictureDatabase:

    def __init__(self,dbpath):
        self.conn = sqlite3.connect(dbpath)
        pass

class AlbumPicturesDao:
    SQL_CREATE_TABLE = 'create table if not exists pictures(id INTEGER  PRIMARY  key autoincrement,url text not null,urlbase not null)'
    SQL_QUERY_URLBASE_EXIST = 'select id from pictures where url = ?'
    SQL_QUERY_URLBASE = 'select url from pictures where url = ?'
    SQL_INSERT_URLBASE = 'insert into pictures(url,urlbase) values(?,?)'
    SQL_UPDATE_URL = 'update pictures set url = ? where id = ? '
    SQL_UPDATE_URLBASE = 'update pictures set urlbase = ? where id = ? '
    def __init__(self,database):
        self.conn = database.conn
        self.cursor = self.conn.cursor()
        self.cursor.execute(AlbumPicturesDao.SQL_CREATE_TABLE)
        self.conn.commit()

    def is_url_exist(self,url):
        self.cursor.execute(AlbumPicturesDao.SQL_QUERY_URLBASE_EXIST,(url,))
        return self.cursor.fetchone() is not None

    def insert_urlbase(self,url,urlbase):
        if not self.is_url_exist(url):
            self.cursor.execute(self.SQL_INSERT_URLBASE,(url,urlbase))
            self.conn.commit()
        pass
    def reduce_url(self):
        self.cursor.execute("select id,url,urlbase from pictures")
        updatecursor = self.conn.cursor()
        pics = self.cursor.fetchone()
        while pics is not None:
            id = pics[0]
            url = pics[1]
            urlbase = pics[2]
            print(url)
            newurl = url.replace('http://www.aitaotu.com','')
            updatecursor.execute(AlbumPicturesDao.SQL_UPDATE_URL,(newurl,id))
            self.conn.commit()
            if urlbase[-1] == '0':
                newurlbase = urlbase[:-1]
                updatecursor.execute(AlbumPicturesDao.SQL_UPDATE_URLBASE, ( newurlbase,id))
                self.conn.commit()
            pics = self.cursor.fetchone()


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
    SQL_ALL_QUERY_ALBUM = 'select * from album_summery'
    SQL_ALL_QUERY_ALBUM_DETAILS = "select album_summery.id,title,album_summery.url,thumburl,piccount,urlbase from album_summery ,pictures where album_summery.url = pictures.url "
    SQL_ALL_QUERY_ALBUM_TAGS = "select tag  from album_tag where url = ?"
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
        cursor = self.conn.cursor()
        cursor.execute(AlbumSummeryDao.SQL_QUERY_ALBUM_EXIST,(url,))
        res = cursor.fetchone()
        return res is not None

    def all_picture_details(self):
        self.cursor.execute(AlbumSummeryDao.SQL_ALL_QUERY_ALBUM_DETAILS)
        res = self.cursor.fetchone()
        albums = []
        index = 0
        while res is not None:
            album = picturemanager.Album(res[0],res[1],res[2],res[3],res[4],res[5])
            albums.append(album)
            print(index)
            index += 1
            res = self.cursor.fetchone()
        print("get all album done")
        print('get details')
        return albums
        # for every album ,prepare tags
        for album in albums:
            self.cursor.execute(AlbumSummeryDao.SQL_ALL_QUERY_ALBUM_TAGS,(album.url,))
            res = self.cursor.fetchone()
            tags = []
            while res is not None:
                tags.append(res[0])
                index +=1
                print(index)
                res = self.cursor.fetchone()
            album.set_tags(tags)
        return albums
        pass
    def get_all(self):
        self.cursor.execute(AlbumSummeryDao.SQL_ALL_QUERY_ALBUM)
        result = self.cursor.fetchone()
        while result is not None:
            yield result
            result = self.cursor.fetchone()

