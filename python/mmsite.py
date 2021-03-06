from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import argparse
import os
import sys
import re
import time
import mmsitedao
def write_file(url,filename):
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    buffer = urlopen(req).read()
    with open(filename,"wb") as fp:
        fp.write(buffer)

def get_fullurl_from_abbrev(name):
    """return the full url address from a abrev name
    """
    return "http://www.aitaotu.com/guonei/%s.html" % name
    pass


def get_html_content(url):
    response = urlopen(url)
    return response.read().decode('utf-8')


def get_title(bsobj):
    """
    :param content:
    :return:
    """
    name = bsobj.title.string
    index = name.find('(')
    if index >= 0:
        return name[0:index]


def parse_tags(bsobj):
    return [node.text for node in bsobj.find(class_="photo-fbl").find_all("a","blue")]

def parse_nextpageurl(bsobj):
    nexturlnode = bsobj.find(id='nl')
    if nexturlnode is None: return None
    return nexturlnode.a.get("href")

def parse_next_album(bsobj):
    tag = bsobj.find(class_="preandnext connext").a
    return tag.get('href')

def parse_pre_album(bsobj):
    tag = bsobj.find(class_="preandnext").a
    return tag.get('href')

def parse_pics(bsobj):
    pics_node = bsobj.find(id='big-pic')
    picurls = [img.get('src') for img in pics_node.find_all('img')]
    return picurls

def parse_pic_baseurl(bsobj):
    pics_node = bsobj.find(id='big-pic')
    picurls = [img.get('src') for img in pics_node.find_all('img')]
    regex = re.compile('(.*)\\d{2,3}\\.jpg$')
    last = None
    baseurl = ""
    for url in picurls:
        match = regex.search(url)
        if match is None: return None
        baseurl = match.group(1)
    return baseurl

def get_page_iter(bsobj):
    """
    :param content:
    :return:
    """
    sitebase = "http://www.aitaotu.com"
    while bsobj is not None:
        nexturl = parse_nextpageurl(bsobj)
        pics = parse_pics(bsobj)
        if pics is not None:
            for picurl in pics:
                yield  picurl
        if nexturl is not None:
            content = get_html_content(sitebase + nexturl)
            bsobj = BeautifulSoup(content)
        else:
            bsobj = None





def get_mmpicset_info_from_url(url):
    """
    :param url:
    :return:
        get the mm picture set info from url
        tuple:
        (title,pageiter,tags)
    """
    response = urlopen(url)
    bytebuffer = response.read()
    # decode to utf-8 string
    htmlcontent = bytebuffer.decode('utf-8')
    bsobj = BeautifulSoup(htmlcontent)
    # get the title
    title = get_title(bsobj)
    # get the page enumerate
    iterpage = get_page_iter(bsobj)
    # get tags
    tags = parse_tags(bsobj)
    return (title,iterpage,tags)



def parse_meitulu_nextpageurl(bsobj):
    pagesnodes = bsobj.find(id='pages').find_all(class_='a1')
    nexturlnode = None;
    for node in pagesnodes:
        print(node.text)
        if node.text == "下一页":
            nexturlnode = node
    if nexturlnode is None: return None
    return nexturlnode.get("href")

def parse_meitulu_pics(bsobj):
    picnodes = bsobj.find(class_='content').find_all(class_='content_img')
    picurls = [img.get('src') for img in picnodes]
    return picurls

def get_meitulu_page_iter(bsobj,lasturl):
    """
    :param content:
    :return:
    """
    sitebase = "http://www.meitulu.com"

    while bsobj is not None:
        nexturl = parse_meitulu_nextpageurl(bsobj)

        pics = parse_meitulu_pics(bsobj)
        if pics is not None:
            for picurl in pics:
                yield  picurl
        if sitebase + nexturl == lasturl:
            nexturl = None
        if nexturl is not None:
            content = get_html_content(sitebase + nexturl)
            lasturl = sitebase + nexturl
            bsobj = BeautifulSoup(content)
        else:
            bsobj = None

def get_meitulu_info_from_url(url):
    """
    :param url:
    :return:
        get the mm picture set info from url
        tuple:
        (title,pageiter,tags)
    """
    response = urlopen(url)
    bytebuffer = response.read()
    # decode to utf-8 string
    htmlcontent = bytebuffer.decode('utf-8')
    bsobj = BeautifulSoup(htmlcontent)
    # get the title
    title = bsobj.title.string
    # get the page enumerate
    iterpage = get_meitulu_page_iter(bsobj,url)
    # get tags
    tags = []
    return (title,iterpage,tags)

def download_meitulu_from_url(url):
    title, iterpics, taglist = get_meitulu_info_from_url(url)
    print(title)
    if not os.path.exists(title):
        os.makedirs(title)

    for i, pic in enumerate(iterpics):
        filename = os.path.join(title, "%02d.jpg" % (i + 1))
        print(pic + " ==> " + filename)
        write_file(pic, filename)
    return (title,title)


class AlreadyParseException(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)


def parese_uploaddate(url):
    htmldoc = urlopen(url).read().decode('utf-8')
    bsobj = BeautifulSoup(htmldoc)
    nodes = bsobj.find_all(class_='item masonry_brick')
    ret = []
    for node in nodes:
        url = node.find(class_='img').find('a').get('href')
        notext = node.find(class_='items_likes').text
        dateregex = re.compile(r"DATE:(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})")
       # uploaddate = time.strptime(dateregex.search(notext).group(1), "%Y-%m-%d %H:%M:%S")
        uploaddate = dateregex.search(notext).group(1)
        print(url)
        print(uploaddate)
        ret.append((url,uploaddate))
    return ret

def parse_summery(bsobj,albumdao,tagdao,picturedao,dupcount,dupmax,**kwargs):
    #title
    #url
    #thumb url
    # tags
    print("first dup %d" % dupcount)
    dryrun = False
    if 'dryrun' in kwargs and kwargs['dryrun'] == True:
        dryrun = True
    detail = False
    if 'detail' in kwargs and kwargs['detail'] == True:
        detail = True
    logger = None
    if 'logger' in kwargs:
        logger = kwargs['logger']
    nodes = bsobj.find_all(class_='item masonry_brick')
    for node in nodes:
        title = node.find(class_='title').find('a').text
        url = node.find(class_='img').find('a').get('href')
        thumburl = node.find(class_='img').find('img').get('data-original')
        tags = [tagnode.text for tagnode in node.find_all(class_='blue')]
        notext = node.find(class_='items_likes').text
        regex = re.compile("共(\\d+)张")
        dateregex = re.compile(r"DATE:(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})")
        print(notext)
        match = regex.search(notext)
        piccount = int(match.group(1))
        uploaddate = dateregex.search(notext).group(1)
        print ("title : %s" % title)
        print ("url : %s" % url)
        print("thumburl : %s" % thumburl)
        print("tags : %s" % tags.__str__())
        print("page : %d" % piccount)
        print("date : %s" % uploaddate.__str__())
        if not albumdao.is_album_exist(url):
            print("not found ")
            if logger is not None:
                logger("found new album %s " % title)
            dupcount = 0
            if not dryrun:
                albumdao.add_album(title,url,thumburl,piccount,uploaddate)
            for tag in tags:
                if not tagdao.is_tag_exist(url,tag):
                    if not dryrun:
                        tagdao.insert_tag(url,tag)
            if not dryrun:
                if detail:
                    parse_and_write_pictureurl_byurl(url,picturedao)


        else:
            dupcount = dupcount + 1
            print("Found Dup!!!!!!!!!!!!!!!!" + "%d" % dupcount)
            if dupcount >= dupmax:
                raise AlreadyParseException("dupmaxreached")
        print("\n")
    return dupcount
    pass
def parse_and_write_pictureurl_byurl(url,picturedao):
    fullurl = "http://www.aitaotu.com" + url
    if picturedao.is_url_exist(url):
        print("Pass ***")
        return

    htmldoc = urlopen(fullurl).read().decode('utf-8')
    bsobj = BeautifulSoup(htmldoc)
    parse_and_write_pictureurl(url,bsobj,picturedao)
def parse_and_write_pictureurl(url,bsobj,picturedao):
    urlbase = parse_pic_baseurl(bsobj)
    if urlbase is not None:
        picturedao.insert_urlbase(url,urlbase)

dupmax = 5

def fill_urlbase_from_database():
    database = mmsitedao.PictureDatabase('album.db')
    albumdao = mmsitedao.AlbumSummeryDao(database)
    picturedao = mmsitedao.AlbumPicturesDao(database)

    for row,album in enumerate(albumdao.get_all()):
        print("index :%05d max %.2f" % (row,float(row)/13072.0))
        print("title: " + album[1])
        print("url: http://www.aitaotu.com" + album[2])
        parse_and_write_pictureurl_byurl(album[2],picturedao)

def modifyurlbase():
    database = mmsitedao.PictureDatabase('album.db')
    albumdao = mmsitedao.AlbumSummeryDao(database)
    picturedao = mmsitedao.AlbumPicturesDao(database)
    picturedao.reduce_url()

def test_updatesite():
    database = mmsitedao.PictureDatabase('album.db')
    albumdao = mmsitedao.AlbumSummeryDao(database)
    tagdao = mmsitedao.AlbumTagsDao(database)
    picturedao = mmsitedao.AlbumPicturesDao(database)

    updatesite(albumdao,tagdao,picturedao,print)

def updatesite(albumdao,tagdao,picturedao,logger):

    dupcount = 0
    kinds = ['guonei','rihan','meinv','gangtai']
    for kind in kinds:
        for i in range(1, 3):
            logger("parse page %d" % i)
            url = "https://www.aitaotu.com/%s/list_%d.html" % (kind,i)
            htmldoc = get_html_content(url)
            bsobj = BeautifulSoup(htmldoc)
            try:
                dupcount = parse_summery(bsobj, albumdao, tagdao,picturedao, 0, dupmax,detail=True,logger = logger)
            except AlreadyParseException as e:
                logger("%s Found duplication at page %d, stop!!!!" % (kind,i))
                break
        pass
def test():
    # htmldoc = get_html_content("https://www.aitaotu.com/guonei/")
    database = mmsitedao.PictureDatabase('album.db')
    albumdao = mmsitedao.AlbumSummeryDao(database)
    tagdao = mmsitedao.AlbumTagsDao(database)
    picturedao = mmsitedao.AlbumPicturesDao(database)
    dupcount = 0

    for i in range(1,66):
        print("parse page %d" % i)
        url = "https://www.aitaotu.com/guonei/list_%d.html" % i
        htmldoc = get_html_content(url)
        bsobj = BeautifulSoup(htmldoc)
        try:
            dupcount = parse_summery(bsobj,albumdao,tagdao,picturedao,0,dupmax)
        except AlreadyParseException as e:
            print("Found duplication at page %d" % i)
            break


def main():
    parser = argparse.ArgumentParser(description="download the mm picture")
    parser.add_argument("-p", "--pageid", default="30430", help="specify the picture url id")
    args = parser.parse_args()
    url = get_fullurl_from_abbrev(args.pageid)
    title, iterpics, taglist = get_mmpicset_info_from_url(url)
    print(title)
    print(taglist)
    if not os.path.exists(title):
        os.makedirs(title)

    for i, pic in enumerate(iterpics):
        filename = os.path.join(title, "%02d.jpg" % (i + 1))
        print(pic + " ==> " + filename)
        write_file(pic, filename)

if __name__ == "__main__":
    # test()
    # fill_urlbase_from_database()
    #modifyurlbase()
    test_updatesite()




