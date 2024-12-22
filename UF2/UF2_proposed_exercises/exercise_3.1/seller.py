import socket
import datetime
import sys
import time

def show_text(t): print(f"{datetime.datetime.now()} {t}")


try:

    type = "seller"
    product = "LEGO,12"

    ip = sys.argv[2]
    port = int(sys.argv[3])

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip,port))
    show_text(f"client connected to {ip} {port}")

    data = type +","+product
    client.send(data.encode("utf-8"))

    connected = True
    flag = True
    while connected:
        show_text(". . .")
        message = client.recv(1024).decode()
        if message != "":
            show_text(f"client recived {message}")
            if message == "Start Conversation":
                client.send(str("Accept").encode("utf-8"))
        time.sleep(5)

except KeyboardInterrupt:
    print("< KeyboardInterrupt error")