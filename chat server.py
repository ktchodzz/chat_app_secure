"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def handle_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    while True:
        msg = client.recv(bufSize)
        if msg != bytes("{quit}", "utf8"):
            print("recieved : %s" % msg.decode("utf8"))
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            print("client quit")
            break


host = '127.0.0.1'
port = 6700
bufSize = 1024
address = (host, port)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(address)

SERVER.listen(10)
print("Server start...")
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=handle_incoming_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
