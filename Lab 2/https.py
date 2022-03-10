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
    if file_directory != "/files":
        os.mkdir(file_directory)
    try:
        while True:
            # receives the user's message
            data = conn.recv(-1)
            # Decode message
            client_message = data.decode()

            # Have something here to read the beginning of the message to see if it's GET or POST or HEAD
            command = client_message.split(2)[0]
            rest = client_message.split(2)[1]
            # If-statements to distinguish each of the commands that we'll be using
            if command == "GET":
                request = rest.split()[0]
                # Check file directory path
                if request == "/":
                    sendback = str(glob.glob(file_directory + "/*"))
                else:
                    try:
                        f = open(file_directory + request + ".txt", "r") # Assume only text files
                        sendback = "Contents of " + request.replace("/", "") + ":\n" + f.read()
                    except FileNotFoundError:
                        sendback = "Error 404: File Not Found"

            elif command == "POST":
                filename = rest.split()[0]
                f = open(file_directory + filename + ".txt", "a")
                f.write(rest.split()[1])
                sendback = "Status: 200, File was successfully uploaded to server"
            conn.sendall(sendback.encode())
    finally:
        conn.close()

def server_get():
    placeholder = None

def server_post():
    placeholder = None


parser = argparse.ArgumentParser()
parser.add_argument("-port", help="server port", type=int, default=8080)
parser.add_argument("-d", help="File Directory Path", type=str, default="/files")
parser.add_argument("-v", help="Display Debugging Messages", action='store_true') # Work on stock debugging messages
args = parser.parse_args()
run_server('', args.port, args.d)