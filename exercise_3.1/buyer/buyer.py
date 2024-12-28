from do_rsa2 import RSA_
import socket
import datetime
from random import randrange as rand
import sys
import time

def show_text(t):print(f"{datetime.datetime.now()} {t}")

try:

    ENCRYPT = RSA_("e","./buyer","")
    DECRYPT = RSA_("d","./seller","")
    
    type = "buyer"

    ip = sys.argv[1]
    port = int(sys.argv[2])

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip,port))
    show_text(f"client connected to {ip} {port}")

    data = type
    client.send(data.encode("utf-8"))


    conversationReady = False

    connected = True
    flag = True


    product = ""

    def election ():
        n = rand(0,3)
        if n == 0: return "Want"
        elif n == 1: return "Low"
        else:   return "Stop"


    
    while connected:
        toSend = ""
        if flag:
            p = client.recv(1024).decode()
            product = p
            show_text(f"client recived this product: {p}")
            flag = False
            show_text(f"client send 'Start Conversation' to seller")
            #
            client.send(str("Start Conversation").encode())
        message = client.recv(1024).decode()
        if message != "":
            show_text(f"client recived {message}")
            #   comença la negocaciacio
            if message == "Accept":
                conversationReady = True
            # SI LA CONVERSACIO ESTA INICIADA
        if conversationReady:

            if message == "Stop":
                toSend = "Stop"
                print("stopping the purchase")
                connected = False
                break
            if message[:4] == "Sale":
                show_text(f"status sale: Sale with Price: {message[4::]}")
                toSend = "Stop"
                connected = False
                break
            
            else:
                if message != "Stop" or message[:4] != "Sale": 
                    toSend = election()
                    client.send(str(toSend).encode())
                    show_text(f"client send {toSend}")



    client.send(str("DISCONNECT").encode("utf-8"))
    print("CLIENT CLOSED")
    client.close()

except KeyboardInterrupt:
    print("< KeyboardInterrupt error")
    client.close()