import socket
import datetime
import math
import sys
import time
from random import randrange as rand
from SellerManagment import Product 

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
    conversationReady = False
    connected = True
    flag = True
    #
    show_text(f"{client.getsockname()[0]}:{client.getsockname()[1]}")
    # Producte Class
    product = product.split(",")
    product = Product(product[0],product[1],"-",client.getsockname()[0])
        
    
    toSend = ""
    while connected:
        
        #show_text(". . .")
        message = client.recv(1024).decode()
        if message != "":
            show_text(f"client recived {message}")
            if message == "Start Conversation":
                show_text(f"client send 'Accept' to seller")
                client.send(str("Accept").encode("utf-8"))
                conversationReady = True
            if message != "Start Conversation":
                
                if message == "Low": # SI RECIBE LOW -> BAJA EL PRECIO O SE PARA
                    r = rand(0,2)
                    if r == 0: # bajar
                        price = float(product.getPrice()) - 1
                        product.setPrice(price)
                        if math.trunc(price) <= 0:
                            toSend += "Stop"
                        else:
                            toSend += "Sale"+str(price)
                            show_text(f"status sale: {toSend}")
                            connected = False
                    if r == 1:
                        toSend += "Sale"+str(product.getPrice())
                        show_text(f"status sale: {toSend}")
                        connected = False
                if message == "Want":   # SI RECIBE WANT -> VENDE PRODUCTO O NO VENDE
                    # venderselo o parar
                    r = rand(0,2)
                    if r == 0 or 1:
                        toSend += "Sale" +str(product.getPrice())
                        connected = False
                    else:
                        toSend += "Stop"
                    show_text(f"status sale: {toSend}")
                    connected = False
                if message == "Stop": # SI RECIBE STOP ENVIA STOP Y MUERE
                    toSend += "Stop"
                    connected = False
                if message !="":

                    # SEND
                    show_text(f"client send {toSend}")
                    client.send(str(toSend).encode())

                
        #time.sleep(5)
    print(f"LAST ORDER: {toSend}" )
    print("CLIENT CLOSED")
    client.close()
except KeyboardInterrupt:
    print("< KeyboardInterrupt error")
    client.close()
except:
    client.close()