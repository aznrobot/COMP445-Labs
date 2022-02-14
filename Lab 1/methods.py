import socket
from urllib.parse import urlparse

def get(v, h, url):
    urlObj = urlparse(url)
    host = urlObj.netloc
    port = 80
    urlIndex = url.index(host)+len(host)
    tail = url[urlIndex:]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    request = "GET " + tail

    if v:
        request += " HTTP/1.1\nHost: "
    else:
        request += "\nHost: "

    request += host + "\n"

    if h != None:
        for key, value in h.items():
            request += key + ":" +value + "\n"


    request += "\n"
    print("***" + request)

    client.send(request.encode())

    # receive some data
    response = client.recv(4096)
    http_response = response.decode()

    # display the response
    print(http_response)

# print(get(True,None,"http://httpbin.org/get?course=networking&assignment=1")) # testing v
# print(get(False,{'course': 'networking', 'assignment': '1'},"http://httpbin.org")) # testing h
#print(get(False,{'course': 'networking', 'assignment': '1'},"http://httpbin.org")) # testing h and v

def post(v, h, d, f, url):
    urlObj = urlparse(url)
    host = urlObj.netloc
    port = 80
    urlIndex = url.index(host) + len(host)
    tail = url[urlIndex:]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    request = "POST " + tail

    if v:
        request += " HTTP/1.1\nhost: "
    else:
        request += "\nhost: "

    request += host + "\n"

    if h != None:
        for key, value in h.items():
            request += key + ":" + value + "\n"

    if d != None:
        request += "\n" + d + "\n"

    if f != None:
        request += "\n" + f + "\n"

    request += "\n"
    print("***" + request)

    client.send(request.encode())

    # receive response
    response = client.recv(4096)
    http_response = response.decode()

    # display the response
    print(http_response)

