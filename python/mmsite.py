from urllib.request import urlopen
import re
def get_fullurl_from_abbrev(name):
    """return the full url address from a abrev name
    """
    pass

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
    # get the title
    title = get_title(htmlcontent)
    # get the page enumerate
    iterpage = get_page_iter(htmlcontent)
    # get tags
    tags = get_tags(htmlcontent)
    return (title,iterpage,tags)

def get_html_content(url):
    response = urlopen(url)
    return response.read().decode('utf-8')


def get_title(content):
    """
    :param content:
    :return:
    """
    title_regex = ''
    pat = re.compile(title_regex)
    result = pat.search(content)
    if result is None:
        raise Exception("Not found title!")
    return result.group(0)
    pass




def get_page_iter(content):
    """
    :param content:
    :return:
    """
    def parsenexturl(content):
        patnext = None
        result = patnext.search(content)
        if result is None:
            return None
        return result.group(0)
    def parsepics(content):
        patpics = None
        result = patpics.search(content)
        if result == None:
            return None
        return result.groups()

    while content is not None:
        nexturl = parsenexturl(content)
        pics = parsepics(content)
        if pics is not None:
            for picurl in pics:
                yield  picurl
        if nexturl is not None:
            content = get_html_content(nexturl)





def get_tags(content):
    """

    :param content:
    :return:
    """
    pass