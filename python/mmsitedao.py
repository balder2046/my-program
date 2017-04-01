import os
import sqlite3
class PictureDatabase:
    SQL_CREATETABLE = """
    create table if not exists album_summery (id integer PRIMARY key autoincrement ,title text UNIQUE ,url text UNIQUE,iconurl text,piccount integer );
    create table if not exists tags(id integer  PRIMARY key  autoincrement,name varchar(32) UNIQUE ,description text);
    create table if not exists picturetags(id integer PRIMARY key autoincrement,albumid integer not null,tagid integer not null);
    create table if not exists album_detail(id integer PRIMARY key autoincrement,title text not null,url text not null UNIQUE ,filepath text,count integer,iconfile varchar(32));
    """
    def __init__(self,dbpath):
        self.conn = sqlite3.connect(dbpath)

        pass


class AlbumSummeryDao:
    sql_create_table = "create table if not exists album_summery (id integer PRIMARY key autoincrement ,title text UNIQUE ,url text UNIQUE,iconurl text,piccount integer );"
    sql_create_summery = "insert into album_summery(title,url,iconurl,piccount) values(?,?,?,?)"
    sql_query_url_exist = "select id from album_summery where url = ?"
    sql_query_url = "select id,title,url,iconurl,numpics from album_summery where url = ?"

    def __init__(self,database):
        self.database = database
        self.conn = database.conn
        self.cursor = self.conn.cursor()
        self.cursor.execute(AlbumSummeryDao.sql_create_table);
        self.conn.commit()
        pass

    def add_album(self,title,url,iconurl,numpics):
        self.cursor.execute(AlbumSummeryDao.sql_create_summery,[title,url,iconurl,numpics])
        self.conn.commit()
    def is_exist(self,url):
        res = self.cursor.execute(AlbumSummeryDao.sql_query_url_exist,url)
        return res.fetchone() is not None

