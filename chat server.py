"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def handle_incoming_connections():
    """Sets up handling for incoming clients."""

    while True:
        welcomeMessage = "Connected to the server. Please type your name first."
        exitInstruction = "If you ever want to exit, type {exit}."

        client, client_address = SERVER.accept()
        history.insert(tkinter.END, "%s:%s has connected.\n" % client_address)
        client.send(bytes(welcomeMessage, "utf8"))
        client.send(bytes(exitInstruction, "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(client, client_address):
    """Handles a single client connection."""
    name = client.recv(bufSize).decode("utf8")
    welcome = 'Welcome %s!' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    server_console.insert(tkinter.END, "%s:%s has choosen name '%s'\n" % (client_address[0], client_address[1], name))
    clients[client] = name

    while True:
        msg = client.recv(bufSize).decode("utf8")
        if msg != "{exit}":
            broadcast(name + ": " + msg)
            server_console.insert(tkinter.END,  "%s: %s\n" % (name, msg))
        else:
            client.close()
            history.insert(tkinter.END, "%s:%s has disconnected.\n" % client_address)
            del clients[client]
            broadcast("%s has left the chat." % name)
            break


def broadcast(msg):
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(msg, "utf8"))


def handle_incoming_client_message():
    "Handle incoming client message"


def display_clients():
    "Show connected clients"


clients = {}
addresses = {}

host = "127.0.0.1"
port = 6700
bufSize = 4096
address = (host, port)

window = tkinter.Tk()
window.title("Chat Server Mode")
#window.geometry('{}x{}'.format(450, 900))

# Server info header frame
Connection_info = tkinter.LabelFrame(window, text="Server Information",font=("arial 11 bold"), fg="#5D4C46", bg="#F2EDD8",height=50)
Connection_info.pack(expand=tkinter.YES, fill=tkinter.BOTH)

#  Server info frame
server_info_frame = tkinter.Frame(Connection_info)
server_info_frame.pack(expand=tkinter.YES,padx=10, pady=10)

serverIpLabel = tkinter.Label(server_info_frame, text="IP-Address: ",font=("arial 11 bold"), fg="#5D4C46", relief="groove",
                   anchor="center", width=20).grid(row=0, column=0, ipadx=10, ipady=5)
serverIpLabel = tkinter.Label(server_info_frame, text=host ,font=("arial 11 bold"), fg="#5D4C46", relief="sunken",
                   anchor="center", width=20).grid(row=0, column=2, ipadx=10, ipady=5)

serverPortLabel = tkinter.Label(server_info_frame, text="Port : ",font=("arial 11 bold"), fg="#5D4C46", relief="groove",
                     anchor="center", width=20).grid(row=1, column=0, ipadx=10, ipady=5)
serverPortLabel = tkinter.Label(server_info_frame, text=port, font=("arial 11 bold"), fg="#5D4C46", relief="sunken",
                     anchor="center", width=20).grid(row=1, column=2, ipadx=10, ipady=5)

# Server console
server_console_frame = tkinter.LabelFrame(window, text="Console",font=("arial 11 bold"), fg="#5D4C46", bg="#F2EDD8")
server_console_frame.pack(expand=tkinter.YES, fill=tkinter.BOTH)

server_console = tkinter.Text(server_console_frame, font=("arial 9 bold"), width=50, height=15)
server_console.pack(expand=tkinter.YES, fill=tkinter.BOTH)

# Connection history
history_frame = tkinter.LabelFrame(window, text="Connection History",font=("arial 11 bold"), fg="#5D4C46", bg="#F2EDD8")
history_frame.pack(expand=tkinter.YES, fill=tkinter.BOTH)

history = tkinter.Text(history_frame, font=("arial 9 bold"), width=50, height=15)
history.pack(expand=tkinter.YES, fill=tkinter.BOTH)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(address)
SERVER.listen(10)
ACCEPT_THREAD = Thread(target=handle_incoming_connections)
ACCEPT_THREAD.start()

window.mainloop()
ACCEPT_THREAD.join()
SERVER.close()
