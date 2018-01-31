from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

host = "127.0.0.1"
port = 6700

address = (host, port)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

while True:
    message = input("Type message here: ")
    if not message: break
    client_socket.send(bytes(message, "utf8"))

client_socket.close()