import socket
import threading
import datetime
import time
from SellerManagment import Product 

ip = "localhost"
port = 0

#   SERVER CONNECTION
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
server.listen()
connected = True

clients = []
product = []

#   FUNCTION HELP
def show_text(t):print(f"{datetime.datetime.now()} {t}")

def brodcast_send(conn,clients,message):
    for c in clients:
        if c != conn:
            c.send(message.encode("utf-8"))
            show_text(f"send {c.getpeername()} message {message}")

def brodcast_recv(conn,clients):
    for c in clients:
        if c != conn:
            message = c.recv(1024).decode()
            show_text(f"recive {c.getpeername()} message {message}")
            return message
        
def sellProduct(product,data,addr):
    newProduct = Product(data[1],data[2],'Purchase',addr) 
    product.append(newProduct)
#   ALERT
show_text(f"server open at address {server.getsockname()}")

#   SERVER MANAGMENT  

def handle(conn,addr,clients,product):

    connected = True

    allData = conn.recv(1024).decode()
    data = allData.split(",")
    
    nameClient = data[0].lower()    #   seller, buller
    clients.append(conn)


    show_text(f"NEW custumer entry, category: {nameClient}")

    if nameClient == "seller":
        #   Posar el item
        sellProduct(product,data,addr)
        flag = True
        while connected:
            if len(clients) == 2:
                if flag and nameClient == "seller":
                    product_send = "Product,"+product[0].getName()+","+product[0].getPrice()
                    brodcast_send(conn,clients,product_send)    #   Enviar al buyer informació producte
                    flag = False
                    conn.send(brodcast_recv(conn,clients).encode("utf-8"))  # Enviar seller resposta buyer primera buyer: Start Conversation
                    #   COMENÇA LA NEGOCIACIO
                  
    elif nameClient == "buyer":
        while connected:
            if len(clients) == 2:
                conn.send(brodcast_recv(conn,clients).encode("utf-8")) #    seller: accept
                    #   COMENÇA LA NEGOCIACIO
                n = True
                while n:
                    try:
                        message = conn.recv(1024).decode()  
                        brodcast_send(conn,clients,message)
                        conn.send(brodcast_recv(conn,clients).encode("utf-8"))
                        time.sleep(5)
                    except:

                        print("Server close")
                        server.close()
                        connected = False
                        clients.clear()
                        n = False
       
        
while connected:

    try:
        conn,addr = server.accept()

        th = threading.Thread(target=handle, args=((conn,addr,clients,product)))
        th.start()
        show_text(f"NEW connection addrs :{addr}")
        show_text(f"connections ready :{threading.active_count() - 1 }")
    except KeyboardInterrupt:
        print("< KeyboardInterrupt, Server close")
        server.close()
    except:
        connected = False
        server.close()


