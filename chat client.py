from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            msg_list.insert(tkinter.END, "Some client left chat by OSError")
            break

def send(event=None):
    msg = entry_field.get("1.0", "end-1c")
    entry_field.delete("1.0", "end-1c")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{exit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    entry_field.delete("1.0", "end-1c")
    entry_field.insert("end-1c", "{exit}")
    send()


host = "127.0.0.1"
port = 6700
BUFSIZ = 4096
address = (host, port)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

# ui window
top = tkinter.Tk()
top.title("Chat Client")
# top.geometry('{}x{}'.format(400, 400))
messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=20, width=65, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

entry_field =tkinter.Text(top, width=35, height=5)
entry_field.pack(side=tkinter.LEFT)
entry_field.bind("<Return>", send)
send_button=tkinter.Button(top, text='Send', width=15, height=5, bg='orange', command=send , activebackground='lightgreen')
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()