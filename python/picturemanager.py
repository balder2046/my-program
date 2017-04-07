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
    def download(self,basepath):
        fullpath = os.path.join(basepath,self.title)
        if os.path.exists(fullpath):
            return
        os.makedir(fullpath)
        for index in range(1,self.piccount + 1):
            fullurl = "%s%02d.jpg" % (basepath,index)
            newfilename = os.path.join(fullpath,"%02d.jpg" % index)
            downloadfile(fullurl,newfilename)
        pass

class PictureManager:
    def __init__(self):
        pass
    def get_by_url(self):
        pass
    def get_by_no(self,number):
        pass
