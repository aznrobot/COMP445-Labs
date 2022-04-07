import socket
import threading
import argparse
import glob
import os
import ipaddress
from packet import *

def run_server(host, port, path, debug):
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        listener.bind((host, port))
        #listener.listen(5)
        print('Server is listening at', port)
        # Create new path if default is not chosen
        if path != "files":
            if path not in os.listdir("./"):  # if directory is not accessable, create it
                if debug:
                    print("New directory path created: /" + path + "\n")
                os.mkdir(path)
        while True:
            data, sender = listener.recvfrom(1024)
            # Assigns a thread to manage a client connection
            #threading.Thread(target=handle_client, args=(listener, data, sender, path, debug)).start()
            handle_client(listener, data, sender, path, debug)
    finally:
        listener.close()


def handle_client(listener, data, sender, path, debug):
    print ('New client from', sender)
    recv_packet = Packet.from_bytes(data)

    # Send SYN-ACK to client
    if(recv_packet.packet_type == 0):
        syn_ack_packet = recv_packet
        syn_ack_packet.packet_type = 1
        listener.sendto(syn_ack_packet.to_bytes(), sender)
        print("Sent SYN-ACK to client %s %s" %  (syn_ack_packet.peer_ip_addr, syn_ack_packet.peer_port))

    while True:
        try:
            listener.settimeout(2)
            data, sender = listener.recvfrom(1024)
            recv_packet = Packet.from_bytes(data)
            if (recv_packet.packet_type == 2 and recv_packet.seq_num == 2):
                listener.settimeout(None)
                break
        except socket.timeout:
            print("Timeout occurred, resending...")
            listener.sendto(syn_ack_packet.to_bytes(), sender)
            print("Sent SYN-ACK to client %s %s" %  (syn_ack_packet.peer_ip_addr, syn_ack_packet.peer_port))

    # data, sender = listener.recvfrom(1024)
    # recv_packet = Packet.from_bytes(data)
    file_directory = path
    try:
        while True:
            # Decode message
            client_message = recv_packet.payload.decode()
            if len(client_message) < 1: #skip empty messages are received
                break

            lines = client_message.split('\n')
            lines = [x for x in lines if x]
            command, url, httpVersion = lines[0].split(" ")
            print(url)
            if command == "GET":
                # Check file directory path
                if url == "/":
                    if debug:
                        print("Retrieving file list from directory: \n")
                        print(str(glob.glob(file_directory + "/*")) + "\n")
                    sendback = "HTTP/1.1 200 OK\n{\n" + str(glob.glob(file_directory + "/*")) + "\n}"
                else:
                    if url.startswith('/'):
                        url = url[1:]
                    try:
                        if debug:
                            print("Retrieving file " + url + " from directory " + file_directory + ": \n")
                            print(file_directory + "/" + url)

                        with open(file_directory + "/" + url, "r") as file:
                            sendback = "HTTP/1.1 200 OK\n"

                            if url.endswith(".txt"):
                                sendback += "Content-type: text\n"
                            elif url.endswith(".jpeg") or url.endswith(".gif"):
                                sendback += "Content-type: image\n"
                            elif url.endswith("jmpeg"):
                                sendback += "Content-type: video\n"
                            else:
                                sendback += "Content-type: text/plain; charset=us-ascii\n"

                            sendback += "Content-Disposition: inline ; filename=" + url + "\n{\n"
                            sendback += file.readline()
                            sendback += "\n}"

                    except FileNotFoundError:
                        sendback = "HTTP/1.1 405 ERROR\n{\n"
                        listOfAllFiles = list()
                        for (dirpath, dirnames, filenames) in os.walk("./"):
                            listOfAllFiles += filenames
                        if url.startswith('/'):
                            url = url[1:]
                        if url in listOfAllFiles:
                            listOfSubFiles = list()
                            for (dirpath, dirnames, filenames) in os.walk(file_directory):
                                listOfSubFiles += filenames
                            if url in listOfSubFiles:
                                sendback += "Error 405: File located in a sub directory of the working directory \n}"
                            else:
                                sendback += "Error 405: File located outside working directory \n}"
                        else:
                            sendback += "Error 405: File Not Found \n}"

            elif command == "POST":
                if debug:
                    print("Creating File: " + url + " in directory " + file_directory + "\n")
                with open(file_directory + "/" + url, "w") as file:
                    file.write(lines[4])
                sendback = "HTTP/1.1 200 OK\n{\n"
                sendback += "Status: 200, File was successfully uploaded to server\n}"
            if debug:
                print("Return message to client:\n")
                print(sendback)
            break
        res_packet = recv_packet
        res_packet.packet_type = 2
        res_packet.payload = sendback.encode()
        listener.sendto(res_packet.to_bytes(), sender)
        print("Sent response to client %s %s" % (res_packet.peer_ip_addr, res_packet.peer_port))
        while True:
            try:
                listener.settimeout(2)
                data, sender = listener.recvfrom(1024)
                ACK_packet = Packet.from_bytes(data)
                if (ACK_packet.packet_type == 3 and ACK_packet.seq_num == 3):
                    listener.settimeout(None)
                    break
            except socket.timeout:
                print("Timeout occurred, resending...")
                listener.sendto(res_packet.to_bytes(), sender)
                print("Sent response to client %s %s" % (recv_packet.peer_ip_addr, recv_packet.peer_port))
        print("ACK received from client")

        # Sending re-ACK to client
        print("Sent ACK to client")
        listener.sendto(ACK_packet.to_bytes(), sender)
        while True:
            try:
                listener.settimeout(20)
                data, sender = listener.recvfrom(1024)
                Client_ACK_packet = Packet.from_bytes(data)
                if (Client_ACK_packet.packet_type == 3 and Client_ACK_packet.seq_num == 3):
                    print("ACK from client received, resending re-ACK...")
                    listener.sendto(ACK_packet.to_bytes(), sender)
            except socket.timeout:
                listener.settimeout(None)
                break


    finally:
        listener.settimeout(None)
        print("Client serviced")


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

# To run router:
# ./router --port --drop-rate --max-delay
#
# To run server:
# python https.py -port 1000
#
# To run client:
# python httpc.py get  -port 1000 -rport 3000 “text.txt”