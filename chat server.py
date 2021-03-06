"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import messagebox
import socketserver
import tkinter
import time

def handle_incoming_connections():
    """Sets up handling for incoming clients."""

    while True:
        welcomeMessage = "Connected to the server."
        exitInstruction = "If you ever want to exit, type {exit}."

        # Firewall goes here
        client, client_address = SERVER.accept()
         # Note: if do this method must implement to close the client window too (Client window stills not close)
        for ban in banned_addr:
            if ban == client_address:
                client.close()
                continue
        result = messagebox.askquestion("Confirm", "Are you sure to accept %s:%s?" % client_address, icon='warning')
        if result == 'no':
            client.send(bytes("{{{exit}}}", "utf8"))
            messagebox.showinfo("Ban", "Banned")
            banned_addr.append(client_address)
            client.close()
            continue
        history.insert(tkinter.END, "%s:%s has connected." % client_address)
        client.send(bytes(welcomeMessage, "utf8"))
        client.send(bytes(exitInstruction, "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(client, client_address):
    """Handles a single client connection."""
    time.sleep(0.5)
    name = client.recv(bufSize).decode("utf8")
    msg = "%s has joined the chat!" % name
    broadcast(msg)

    clientInfo = "%s:%s has choosen name '%s'\n" % (client_address[0], client_address[1], name)
    server_console.insert(tkinter.END, clientInfo)
    
    clients[client] = name
    clientNameList.append(name)
    broadcast("-::-".join(clientNameList))

    while True:
        msg = client.recv(bufSize).decode("utf8")
        if msg != "{exit}":
            msgArray = msg.split(": ")
            if len(msgArray) > 1:
                message = "(Private) %s to %s: %s" % (name, msgArray[0], " ".join(msgArray[1::]))
                sent_individual(name, msgArray[0], message)
                server_console.insert(tkinter.END, message)
            else:
                broadcast(name + ": " + msg)
                server_console.insert(tkinter.END, "%s: %s\n" % (name, msg))
        else:
            client.close()
            del clients[client]
            history.insert(tkinter.END, "%s:%s has disconnected.\n" % client_address)
            clientNameList.remove(name)
            broadcast("%s has left the chat." % name)
            broadcast("-::-".join(clientNameList))
            break


def broadcast(msg):
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(msg, "utf8"))


def announcement(event=None):
    message = my_msg.get()
    my_msg.set("")
    announceText = "Server has announced: \"%s\"" % message
    server_console.insert(tkinter.END,  announceText)
    broadcast(announceText)


def sent_individual(senderName, recieverName, msg):
    "Sent a message to one client"
    isSent = False
    for recieverSock in clients:
        if clients[recieverSock] == recieverName:
            for senderSock in clients:
                if clients[senderSock] == senderName:
                    recieverSock.send(bytes(msg, "utf8"))
                    senderSock.send(bytes(msg, "utf8"))
                    isSent = True
                    break
            break
    if not isSent:
        broadcast("%s: %s" % (senderName, msg.split(": ")[1]))


clients = {}
clientNameList = ["Server (default)"]
addresses = {}

host = "127.0.0.1"
port = 6700
bufSize = 4096
address = (host, port)
banned_addr = []

window = tkinter.Tk()
window.title("Chat Server")

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
scrollbar = tkinter.Scrollbar(server_console_frame)
server_console = tkinter.Listbox(server_console_frame, font=("arial 9 bold"), width=50, height=15, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
server_console.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
server_console_frame.pack(expand=tkinter.YES, fill=tkinter.BOTH)

# Connection history
history_frame = tkinter.LabelFrame(window, text="Connection History",font=("arial 11 bold"), fg="#5D4C46", bg="#F2EDD8")
scrollbar = tkinter.Scrollbar(history_frame)
history = tkinter.Listbox(history_frame, font=("arial 9 bold"), width=50, height=15, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
history.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
history_frame.pack(expand=tkinter.YES, fill=tkinter.BOTH)

# Announcement section
messages_frame = tkinter.Frame(window)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)

send_frame = tkinter.LabelFrame(window, bg="#F2EDD8")
send_frame.pack()

entry_field = tkinter.Entry(send_frame, textvariable=my_msg,width=65)
entry_field.pack(side=tkinter.LEFT)
entry_field.bind("<Return>", announcement)

send_button = tkinter.Button(send_frame, text="send", command=announcement, width=13, bg='#FFAE5D',activebackground='#F8DEBD')
send_button.pack()

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(address)
SERVER.listen(10)
ACCEPT_THREAD = Thread(target=handle_incoming_connections)
ACCEPT_THREAD.start()

window.mainloop()
SERVER.close()
