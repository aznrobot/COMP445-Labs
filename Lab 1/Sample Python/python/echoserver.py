import socket
import threading
import argparse


def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            # Assigns a thread to manage a client connection
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print ('New client from', addr)
    try:
        while True:
            # receives the user's message
            data = conn.recv(1024)

            # Have something here to read the beginning of the message to see if it's GET or POST or HEAD
            command = data.split(2)[0]
            location = data.split(2)[1]
            # If-statements to distinguish each of the commands that we'll be using
            if command == "GET":
                break
            elif command == "POST":
                break
            elif command == "HEAD":
                break
            else:
                break
            conn.sendall(data)
    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)
