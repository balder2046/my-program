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



def get_tags(content):
    """

    :param content:
    :return:
    """
    pass

def parse_overview(bsobj):
    # all album nodes
    nodes = bsobj.find_all(class_="item masonry_brick")
    for node in nodes:
        # get the thumb url
        thumburl = node.find('img').get('data-original')
        # get the title
        titlenode = node.find(class_='title').find('a')
        title = titlenode.text
        # get the url
        url = titlenode.get('href')
        # get the tags
        tags = [tagnode.text for tagnode in node.find_all(class_='blue')]
        notext = node.find(class_='items_likes').text
        regex = re.compile("共(%d+)张")
        match = regex.search(notext)
        piccount = int(match.group(1))



    pass
def testdatabase():
    database = mmsitedao.PictureDatabase("test1.db")
    dao = mmsitedao.AlbumSummeryDao(database)
    pass
def testparse():
    fp = open("bigmenu.html",'rt',encoding='utf-8')
    pass
def test():
    pass

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
    pass


if __name__ == "__main__":
    test()



