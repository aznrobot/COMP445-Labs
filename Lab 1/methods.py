import socket
from urllib.parse import urlparse
import json
import pickle

def get(v, h, url):
    urlObj = urlparse(url)
    host = urlObj.netloc
    port = 80
    urlIndex = url.index(host)+len(host)
    tail = url[urlIndex:]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    request = "GET " + tail

    request += " HTTP/1.1\nhost: "
    request += host + "\n"
    request += "Connection: close \n"
    if h != None:
        for key, value in h.items():
            request += "Accept: " + value + "\n"
            request += key + ":" + value + "\n"

    request += "\n"
    print("----------\n" + request+"\n----------" )

    client.send(request.encode())

    # receive some data
    response = client.recv(4096)
    http_response = response.decode()

    # display the response
    if v:
        print(http_response)
    else:
        vIndex = http_response.index('{')
        print(http_response[vIndex:])

# print(get(False,None,"http://httpbin.org/get?course=networking&assignment=1")) # testing v
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

    request += " HTTP/1.1\nhost: "
    request += host + "\n"
    request += "Connection: close \n"
    if h != None:
        for key, value in h.items():
            request += "Accept: " + value + "\n"
            request += key + ":" + value + "\n"

    if d != None:
        content_len = len(str(d))
        request += "Content-Length: " + str(content_len) + "\n"
        request += "\n"
        request += d + "\n"

    if f != None:
        file = open(f,"r")
        content_len = len(file)
        request += "Content-Length: " + str(content_len) + "\n"
        request += "\n"
        request += file.read() + "\n"

    print("----------\n" + request+"\n----------" )

    client.send(request.encode())

    # receive response
    response = client.recv(4096)
    http_response = response.decode()

    # display the response
    if v:
        print(http_response)
    else:
        vIndex = http_response.index('{')
        print(http_response[vIndex:])


# print(post(True,{"Content-Type":"application/json"},'{"Assignment": 1}',None,"http://httpbin.org/post"))
