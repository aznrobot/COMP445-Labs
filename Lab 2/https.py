import socket
import threading
import argparse
import glob
import os

def run_server(host, port, path, debug):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Server is listening at', port)
        # Create new path if default is not chosen
        if path != "files":
            if path not in os.listdir("./"):  # if directory is not accessable, create it
                if debug:
                    print("New directory path created: /" + path + "\n")
                os.mkdir(path)
        while True:
            conn, addr = listener.accept()
            # Assigns a thread to manage a client connection
            threading.Thread(target=handle_client, args=(conn, addr, path, debug)).start()
    finally:
        listener.close()


def handle_client(conn, addr, path, debug):
    print ('New client from', addr)
    file_directory = path
    sendback = ""

    try:
        while True:
            # receives the user's message
            data = conn.recv(1024)
            # Decode message
            client_message = data.decode()
            if len(client_message) < 1: #skip empty messages are received
                break

            lines = client_message.split('\n')
            lines = [x for x in lines if x]
            command, url, httpVersion = lines[0].split(" ")
            if command == "GET":
                # Check file directory path
                if url == "/":
                    if debug:
                        print("Retrieving file list from directory: \n")
                        print(str(glob.glob(file_directory + "/*")) + "\n")
                    sendback += "HTTP/1.1 200 OK\n{\n" + str(glob.glob(file_directory + "/*")) + "\n}"
                else:
                    try:
                        if debug:
                            print("Retrieving file " + url + " from directory " + file_directory + ": \n")
                            print(file_directory + "/" + url)

                        with open(file_directory + "/" + url, "r") as file:
                            sendback += "HTTP/1.1 200 OK\n{\n"
                            sendback += file.readline()
                        sendback += "\n}"

                        # f = open(file_directory + request, "r") # Assume only text files
                        # sendback = "Contents of " + request.replace("/", "") + ":\n" + f.read()
                    except FileNotFoundError:
                        listOfAllFiles = list()
                        for (dirpath, dirnames, filenames) in os.walk("./"):
                            listOfAllFiles += filenames
                        if url.startswith('/'):
                            url = url[1:]
                        if url in listOfAllFiles:
                            sendback += "HTTP/1.1 405 ERROR\n{\n"
                            sendback += "Error 405: File located outside working directory \n}"
                        else:
                            sendback += "HTTP/1.1 404 ERROR\n{\n"
                            sendback += "Error 404: File Not Found \n}"

            elif command == "POST":
                if debug:
                    print("Creating File: " + url + " in directory " + file_directory + "\n")
                with open(file_directory + "/" + url, "w") as file:
                    file.write(lines[4])
                sendback += "HTTP/1.1 200 OK\n{\n"
                sendback += "Status: 200, File was successfully uploaded to server\n}"
            if debug:
                print("Return message to client:\n")
                print(sendback)
            conn.sendall(sendback.encode())
    finally:
        conn.close()


parser = argparse.ArgumentParser()
parser.add_argument("-port", help="server port", type=int, default=8080)
parser.add_argument("-d", help="File Directory Path", type=str, default="files")
parser.add_argument("-v", help="Display Debugging Messages", action='store_true') # Work on stock debugging messages
args = parser.parse_args()
if args.v:
    v = True
else:
    v = False
run_server('', args.port, args.d, v)

# To run server:
# python https.py -port 1000
#
# To run client:
# python httpc.py get  -port 1000 “text.txt”