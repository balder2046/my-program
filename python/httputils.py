from urllib.request import urlopen
ret = urlopen("http://www.salttiger.com",None,timeout=10)
print(ret.info())
print(ret.getcode())
content = ret.read()
strcontent = content.decode('UTF-8',errors="replace")
print(strcontent[18057])
print(strcontent)
