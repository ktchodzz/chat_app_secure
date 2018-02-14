from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(bufSize).decode("utf8")
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

# ui window
top = tkinter.Tk()
top.title("Chat Client")

# message frame
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame) 
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack(expand=tkinter.YES, fill=tkinter.BOTH)

# send text frame
send_frame = tkinter.LabelFrame(top, bg="#F2EDD8")
send_frame.pack()

entry_field = tkinter.Entry(send_frame, textvariable=my_msg,width=65)
entry_field.pack(side=tkinter.LEFT)
entry_field.bind("<Return>", send)

send_button = tkinter.Button(send_frame, text="Send", command=send, width=13, bg='#FFAE5D',activebackground='#F8DEBD')
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
