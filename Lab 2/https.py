import socket
import threading
import argparse
import glob
import os

def run_server(host, port, path):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Server is listening at', port)
        while True:
            conn, addr = listener.accept()
            # Assigns a thread to manage a client connection
            threading.Thread(target=handle_client, args=(conn, addr, path)).start()
    finally:
        listener.close()


def handle_client(conn, addr, path):
    print ('New client from', addr)
    file_directory = path
    # Create new path if default is not chosen
    if file_directory != "files":
        if file_directory not in os.listdir("./"): #if directory is not accessable, create it
            os.mkdir(file_directory)
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
            sendback = ""
            if command == "GET":
                # Check file directory path
                if url == "/":
                    sendback = str(glob.glob(file_directory + "/*"))
                else:
                    try:
                        print(file_directory + "/" + url)
                        sendback += "HTTP/1.1 200 OK\n { \n"
                        with open(file_directory + "/" + url, "r") as file:
                            sendback += file.readline()
                        sendback += " \n }"

                        # f = open(file_directory + request, "r") # Assume only text files
                        # sendback = "Contents of " + request.replace("/", "") + ":\n" + f.read()
                    except FileNotFoundError:
                        listOfAllFiles = list()
                        for (dirpath, dirnames, filenames) in os.walk("./"):
                            listOfAllFiles += filenames
                        if url.startswith('/'):
                            url = url[1:]
                        if url in listOfAllFiles:
                            sendback = "HTTP/1.1 405 ERROR\n"
                            sendback += "Error 405: File located outside working directory"
                        else:
                            sendback = "HTTP/1.1 404 ERROR\n"
                            sendback += "Error 404: File Not Found"

            elif command == "POST":
                print("Here")
                with open(file_directory + "/" + url, "w") as file:
                    file.write(lines[4])
                sendback = "HTTP/1.1 200 OK\n"
                sendback += "Status: 200, File was successfully uploaded to server"
            print(sendback)
            conn.sendall(sendback.encode())
    finally:
        conn.close()


parser = argparse.ArgumentParser()
parser.add_argument("-port", help="server port", type=int, default=8080)
parser.add_argument("-d", help="File Directory Path", type=str, default="files")
parser.add_argument("-v", help="Display Debugging Messages", action='store_true') # Work on stock debugging messages
args = parser.parse_args()
run_server('', args.port, args.d)

# To run server:
# python https.py -port 1000
#
# To run client:
# python httpc.py get  -port 1000 “text.txt”