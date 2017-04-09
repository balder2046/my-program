import os
import urllib
from urllib.request import urlopen
def downloadfile(url,filename):
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        return False
    buffer = response.read()
    with open(filename,'wb') as filep:
        filep.write(buffer)
    return True

class Album:
    def __init__(self,id,title,url,thumburl,piccount,urlbase):
        self.id = id
        self.title = title
        self.url = url
        self.urlbase = urlbase
        self.thumburl = thumburl
        self.piccount = piccount
        pass
    def set_tags(self,tags):
        self.tags = tags
    def get_filepath(self,basepath = '.'):
        fullpath = os.path.join(basepath, self.title)
        return fullpath
    def download(self,basepath,progressinfo = None,logger = None):
        if progressinfo is not None:
            progressinfo(0)
        fullpath = os.path.join(basepath,self.title)
        if os.path.exists(fullpath):
            if logger is not None:
                logger("%s 已经存在" % self.title)
                progressinfo(self.piccount)
            return
        os.makedirs(fullpath)
        if logger is not None:
            logger("开始下载 %s " % self.title)
        for index in range(1,self.piccount + 1):
            fullurl = "%s%02d.jpg" % (self.urlbase,index)
            newfilename = os.path.join(fullpath,"%02d.jpg" % index)
            downloadfile(fullurl,newfilename)
            if progressinfo is not None:
                progressinfo(index)
        if logger is not None:
            logger("下载 %s 完成" %self.title)

        pass

class PictureManager:
    def __init__(self):

        pass

    def reload(self,albums):
        self.albums = albums
        self.albumdic = {}
        for album in albums:
            self.albumdic[album.url] = album
        pass

    def download(self,logger = None):
        pass
    def get_by_url(self,url):
        if url in self.albumdic:
            return self.albumdic[url]
        return None

    def get_by_no(self,number):
        results = []
        for album in self.albums:
            if number in album.url:
                results.append(album)
        return results
