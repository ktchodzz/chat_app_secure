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
window.title("Chat Server")
window.geometry('{}x{}'.format(600, 900))

# Server info header frame
Connection_info = tkinter.LabelFrame(window, text="Server Information", fg="green", bg="powderblue")
Connection_info.pack(expand=tkinter.YES, fill=tkinter.BOTH)

#  Server info frame
server_info_frame = tkinter.Frame(Connection_info)
server_info_frame.pack(padx=10, pady=10)

serverIpLabel = tkinter.Label(server_info_frame, text="IP-Address: ", relief="groove",
                   anchor="center", width=15).grid(row=0, column=0, ipadx=10, ipady=5)
serverIpLabel = tkinter.Label(server_info_frame, text=host, relief="sunken",
                   anchor="center", width=20).grid(row=0, column=2, ipadx=10, ipady=5)

serverPortLabel = tkinter.Label(server_info_frame, text="Port : ", relief="groove",
                     anchor="center", width=15).grid(row=1, column=0, ipadx=10, ipady=5)
serverPortLabel = tkinter.Label(server_info_frame, text=port, relief="sunken",
                     anchor="center", width=20).grid(row=1, column=2, ipadx=10, ipady=5)

# Server console
server_console_frame = tkinter.LabelFrame(window, text="Console", fg="green", bg="powderblue")
server_console_frame.pack()

server_console = tkinter.Text(server_console_frame, font=("arial 12 bold italic"), width=50, height=15)
server_console.pack()

# Connection history
history_frame = tkinter.LabelFrame(window, text="Connection History", fg="green", bg="powderblue")
history_frame.pack()

history = tkinter.Text(history_frame, font=("arial 12 bold italic"), width=50, height=15)
history.pack()

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(address)
SERVER.listen(10)
ACCEPT_THREAD = Thread(target=handle_incoming_connections)
ACCEPT_THREAD.start()
window.mainloop()
SERVER.close()
