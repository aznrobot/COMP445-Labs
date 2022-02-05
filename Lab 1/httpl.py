from urllib.parse import *

def GET(v, h, url):
    parsed = urlparse(url)
    host = parsed.netloc
    if parsed.path == "":
        path = "/"
    else:
        path = parsed.path

    args = dict()
    allArgs = parsed.query
    splittedArgs = allArgs.split(sep="&")
    for i in splittedArgs:
        temp = i.split(sep="=")
        args[temp[0]] = temp[1]

    headers = dict()
    headers["Host"] = host

    output = dict()
    output["args"] = args
    output["headers"] = headers
    output["url"] = url
    if v:
        print(output)
    else:
        print(output)


def POST(v, h, d, f, url):
    parsed = urlparse(url)
    host = parsed.netloc

    args = dict()

    headers = dict()
    headers["Host"] = host

    output = dict()
    output["args"] = args
    output["data"] = d
    output["files"] = f
    output["headers"] = headers
    output["json"] = d # Convert dict to JSON
    output["url"] = url

    if v:
        print(output)
    else:
        print(output)
