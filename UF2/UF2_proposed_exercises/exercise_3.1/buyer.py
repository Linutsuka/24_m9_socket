import socket
import datetime
import sys

def show_text(t):print(f"{datetime.datetime.now()} {t}")

try:

    type = "buyer"

    ip = sys.argv[1]
    port = int(sys.argv[2])

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip,port))
    show_text(f"client connected to {ip} {port}")

    data = type
    client.send(data.encode("utf-8"))


    connected = True
    flag = True
    while connected:
        if flag:
            p = client.recv(1024).decode()
            show_text(f"client recived this product: {p}")
            flag = False
            show_text(f"client send 'Start Conversation' to seller")
            client.send(str("Start Conversation").encode())
        message = client.recv(1024).decode()
        if message != "":
            show_text(f"client recived {message}")
            

except KeyboardInterrupt:
    print("< KeyboardInterrupt error")