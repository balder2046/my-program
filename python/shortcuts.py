#!/usr/bin/python
# coding = utf-8
from os import path
import mmsitedao
import picturemanager

def get_picture_mngr():
    fileparts = path.split(__file__)
    dbfile = path.join(fileparts[0],"album.db")
    database = mmsitedao.PictureDatabase(dbfile)
    albumdao = mmsitedao.AlbumSummeryDao(database)
    tagdao = mmsitedao.AlbumTagsDao(database)
    picturedao = mmsitedao.AlbumPicturesDao(database)
    albums = albumdao.all_picture_details()
    picturemgr = picturemanager.PictureManager()
    picturemgr.reload(albums)
    return picturemgr

def test():
    mgr = get_picture_mngr()
    print(len(mgr.albums))
if __name__ == "__main__":
    test()