from urllib.request import urlopen
from bs4 import BeautifulSoup
import argparse
import os
import sys
import re
import mmsitedao
def write_file(url,filename):
    buffer = urlopen(url).read()
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


class AlreadyParseException(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)

def parse_summery(bsobj,albumdao,tagdao,dupcount,dupmax,**kwargs):
    #title
    #url
    #thumb url
    # tags
    print("first dup %d" % dupcount)
    dryrun = False
    if 'dryrun' in kwargs and kwargs['dryrun'] == True:
        dryrun = True
    nodes = bsobj.find_all(class_='item masonry_brick')
    for node in nodes:
        title = node.find(class_='title').find('a').text
        url = node.find(class_='img').find('a').get('href')
        thumburl = node.find(class_='img').find('img').get('data-original')
        tags = [tagnode.text for tagnode in node.find_all(class_='blue')]
        notext = node.find(class_='items_likes').text
        regex = re.compile("共(\\d+)张")
        print(notext)
        match = regex.search(notext)
        piccount = int(match.group(1))
        print ("title : %s" % title)
        print ("url : %s" % url)
        print("thumburl : %s" % thumburl)
        print("tags : %s" % tags.__str__())
        print("page : %d" % piccount)
        if not albumdao.is_album_exist(url):
            print("not found ")
            dupcount = 0
            if not dryrun:
                albumdao.add_album(title,url,thumburl,piccount)
            for tag in tags:
                if not tagdao.is_tag_exist(url,tag):
                    if not dryrun:
                        tagdao.insert_tag(url,tag)
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
def test():
    # htmldoc = get_html_content("https://www.aitaotu.com/guonei/")
    database = mmsitedao.PictureDatabase('album.db')
    albumdao = mmsitedao.AlbumSummeryDao(database)
    tagdao = mmsitedao.AlbumTagsDao(database)
    dupcount = 0

    for i in range(1,66):
        print("parse page %d" % i)
        url = "https://www.aitaotu.com/guonei/list_%d.html" % i
        htmldoc = get_html_content(url)
        bsobj = BeautifulSoup(htmldoc)
        try:
            dupcount = parse_summery(bsobj,albumdao,tagdao,0,dupmax)
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
    fill_urlbase_from_database()
    #modifyurlbase()




