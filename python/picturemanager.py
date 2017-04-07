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
    def download(self,path):
        pass
