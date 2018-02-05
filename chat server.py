"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def handle_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        welcomeMessage = "Connected to the server. Please type your name first."
        client.send(bytes(welcomeMessage, "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """Handles a single client connection."""

    name = client.recv(bufSize).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {exit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(bufSize)
        if msg != bytes("{exit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{exit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def handle_incoming_client_message():
    "Handle incoming client message"


def display_clients():
    "Show connected clients"
    

clients = {}
addresses = {}

top = tkinter.Tk()
top.title("Server")

messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

host = '127.0.0.1'
port = 6700
bufSize = 4096
address = (host, port)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(address)

SERVER.listen(10)
print("Server start...")
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=handle_incoming_connections)
ACCEPT_THREAD.start()
tkinter.mainloop()
ACCEPT_THREAD.join()
SERVER.close()
