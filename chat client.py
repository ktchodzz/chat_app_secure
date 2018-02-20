from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    """Handles receiving of messages."""
    client_socket.send(bytes(clientName, "utf8"))
    while True:
        try:
            msg = client_socket.recv(bufSize).decode("utf8")
            if len(msg.split("-::-")) > 1:
                online_conn.delete(0, tkinter.END)
                clients = msg.split("-::-")
                for client in clients:
                    online_conn.insert(tkinter.END, client)
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event=None):
     msg = my_msg.get()
     my_msg.set("")  # Clears input field.
     client_socket.send(bytes(msg, "utf8"))

     if msg == "{exit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{exit}")
    send()


host = "127.0.0.1"
port = 6700
bufSize = 4096
address = (host, port)

clientName = input("Enter your name: ")

# ui window
top = tkinter.Tk()
top.title("Chat Client - %s" % clientName)

# Online Connection List
connection_frame = tkinter.LabelFrame(top, text="Online Connections", font=("arial 11 bold"), fg="#5D4C46", bg="#F2EDD8")
scrollbar = tkinter.Scrollbar(connection_frame)
online_conn = tkinter.Listbox(connection_frame, font=("arial 9 bold"), width=20, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
online_conn.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
connection_frame.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

# message frame
chat_frame = tkinter.Frame(top)
messages_frame = tkinter.LabelFrame(top, text="Chatting",font=("arial 11 bold"), fg="#5D4C46", bg="#F2EDD8")
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
messages_frame.pack(expand=tkinter.YES, fill=tkinter.BOTH)

# send text frame
send_frame = tkinter.LabelFrame(top, bg="#F2EDD8")
send_frame.pack()

entry_field = tkinter.Entry(send_frame, textvariable=my_msg,width=55)
entry_field.pack(side=tkinter.LEFT)
entry_field.bind("<Return>", send)

send_button = tkinter.Button(send_frame, text="Send", command=send, width=13, bg='#FFAE5D',activebackground='#F8DEBD')
send_button.pack()
chat_frame.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
