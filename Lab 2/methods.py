import socket
from urllib.parse import urlparse
import json
import pickle

def get(v, h, o, url, in_port, counter=5):
    if in_port == None:
        in_port = 80

    if counter == 0:
        print("Only 5 redirect attempts are allowed")
        exit()

    urlObj = urlparse(url)
    if bool(urlObj.scheme):
        urlObj = urlparse(url)
        host = urlObj.netloc
        urlIndex = url.index(host) + len(host)
        tail = url[urlIndex:]
    else:
        host = "localhost"
        tail = url
    port = in_port


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

    client.send(request.encode())

    # receive some data
    response = client.recv(1024)
    http_response = response.decode()

    # Check if the response is correct
    http_check = http_response.split("\n", 1)[0]
    http_status = http_check.split(" ")[1]


    if http_status != "200" and counter != 0:
        if v:
            print(http_response)
            vIndex = http_response.index('{')
            if o != None:
                output = open(o, "w")
                output.write(http_response[vIndex:])
                output.close()
        else:
            vIndex = http_response.index('{')
            if o != None:
                output = open(o, "w")
                output.write(http_response[vIndex:])
                output.close()
            print(http_response[vIndex:])

        answer = ""
        while True:
            answer = input("\n Would you like to be redirected to http://httpbin.org? \n Please enter yes or no\n")
            if (answer.lower() != "yes") or (answer.lower() != "no"):
                break

        if answer.lower() == "no":
            return

        print("- URL cannot be reached. HTTP response code: " + http_status + " redirecting to http://httpbin.org -\n")
        urlObj = urlparse(url)
        urlIndex = url.index(urlObj.netloc) + len(urlObj.netloc)
        rest = url[urlIndex:]
        newURL = "http://httpbin.org" + rest
        get(v, h, o, newURL, 80, counter - 1)

    else:
        # display the response
        if v:
            vIndex = http_response.index('{')
            if o != None:
                output = open(o, "w")
                output.write(http_response[vIndex:])
                output.close()
            print(http_response)
        else:
            vIndex = http_response.index('{')
            if o != None:
                output = open(o, "w")
                output.write(http_response[vIndex:])
                output.close()
            print(http_response[vIndex:])



# print(get(False,None,"http://httpbin.org/get?course=networking&assignment=1")) # testing v
# print(get(True,None,"https://httpdump.io/get?course=networking&assignment=1")) # testing redirect
# print(get(False,{'course': 'networking', 'assignment': '1'},"http://httpbin.org")) # testing h
#print(get(False,{'course': 'networking', 'assignment': '1'},"http://httpbin.org")) # testing h and v

def post(v, h, d, f, o, url, in_port):

    if in_port == None:
        in_port = 80

    urlObj = urlparse(url)
    if bool(urlObj.scheme):
        host = urlObj.netloc
        urlIndex = url.index(host) + len(host)
        tail = url[urlIndex:]
    else:
        host = "localhost"
        tail = url
    port = in_port

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
        try:
            with open(f, "r") as file:
                lines = file.readline()
        except:
            print("File could not be opened")
            exit()
        content_len = len(lines)
        request += "Content-Length: " + str(content_len) + "\n"
        request += "\n"
        request += lines + "\n"


    client.send(request.encode())

    # receive response
    response = client.recv(1024)
    http_response = response.decode()

    # display the response
    if v:
        print(http_response)
        vIndex = http_response.index('{')
        if o != None:
            output = open(o, "w")
            output.write(http_response[vIndex:])
            output.close()
    else:
        vIndex = http_response.index('{')
        if o != None:
            output = open(o, "w")
            output.write(http_response[vIndex:])
            output.close()
        print(http_response[vIndex:])


# print(post(True,{"Content-Type":"application/json"},None,"temp.txt","http://httpbin.org/postdsdsd"))
# print(post(True,{"Content-Type":"application/json"},None,"temp.txt","https://httpdump.io/9jr9h"))
