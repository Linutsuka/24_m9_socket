import datetime
import time
from SellerManagment import Product
import socket
import threading

#   VARIABLES
ip = "localhost" 
port = 0

#
def show_text(t):
    print(f"{datetime.datetime.now()} {t}")

def brodcast_send(conn,clients,message):
    for c in clients:
        if c != conn:
            c.send(message.encode("utf-8"))

def brodcast_recv(conn,clients):
    for c in clients:
        if c != conn:
            message = c.recv(1024).decode()
            return message



def product_sell(productes,data,addr):
    productes.append(Product(data[1],data[2],'Purchase',str(addr)))
    print(f"Productes en venta {len(productes)} per el venedor {addr}")


#   Connexió del client independentment si es seller o buyer
def handle_client(conn,addr,clients,productes):
    show_text(f"NEW CONNECTION ADDRES :{addr}")

    connected = True
    #   El missatge inicial es la informació del connectat, si es buyer o seller i  la informació del producte
    #   INFORMACIÓ A POSAR del VENEDOR: SELLER,name,price,status,None
    allData = conn.recv(1024).decode()
    data = allData.split(',')
    client = data[0].lower()   
    
    show_text(f"NEW {client} ENTRY :{addr} ")
    #   Clients connectats
    clients.append(conn) 
    if client == "seller":
        product_sell(productes,data,addr)

    sendedProduct = False
    #   Mentre estigui connectat
    while connected:

        if len(clients) == 2 and client == "buyer" and sendedProduct == False:
         #   S'envia primerament l'informació del producte i continuar
            productSend = str("Product"+","+productes[0].getName()+","+productes[0].getPrice())
            show_text(f"send to buyer product:  {productSend}")
            conn.send(productSend.encode("utf-8"))
            sendedProduct = True

        if client == 'seller':
          
            status = "Keep"
            if len(clients) == 2:
                print("somos dos")
                while status != "Stop" or status != "Want":
                    print("he entrado 1 vez")
                    #   Rep la resposta del client
                    message = brodcast_recv(conn,clients) # la eleccion del pipe
                    status = message
                    conn.send(message.encode("utf-8"))
                    print(f"SELLER RECIBE {message} SE ENVIA AL SERVIDOR-SELLER")
                    time.sleep(3)
                    respuesta = conn.recv(1024).decode()
                    print(f"RESPUESTA DEL SERVIDOR SELLER{respuesta}")
                   
                if status == "Stop" or status == "Want":
                    message = brodcast_recv(conn,clients) # la eleccion del pipe
                    print("seller left the conversation")
                    if conn in clients:
                        clients.remove(conn)
                    conn.close()
                    print("Close seller")

        if client == "buyer":
            #   Mentre no hi hagi productes
            while len(productes) == 0:
                msg = "Wait,SERVER: Waiting to new product . . ."
                conn.send(msg.encode("utf-8"))
                time.sleep(5)
            #   Primero envia continua al buyer-server, el buyer hara un random y envia su primera respuesta que la recibe el seller
            conn.send(str("Keep").encode("utf-8"))
            # coge la respuesta del seller
            message = brodcast_recv(conn,clients)

            array_aux = message.split(",")
            print(f"BUYER RECIBE DE SELLER {array_aux[0]}")      #keep      
            #   CUANDO HAY DOS CLIENTES

            status = array_aux[0]
            #   Mentre el producte estigui per comprar i es vulgui comprar
            while status !=  'Stop' or status != "Sale":
                #   Envia lo recibido al cliente
                conn.send(str(status).encode())
                #   El seller i el client s'han de posar d'acord, si no fan en x s'acaba la negociacio
                #   Rep el missatge donat per el SELLER ( si continua o no )
                response = conn.recv(1024).decode()
                print(f"RESPUES DEL BUYER SERVER{response}")
                
                #   Envia la resposta
            if status == "Stop" or "Sale":
                print("connexion off buyer")
                conn.close()



def main():

    #   Encendre el servidor
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen()
    show_text("SERVER CONNECTED")
    show_text(f"listens for connections on {s.getsockname()}")
    #   Clients
    clients = []
    #   Productes
    productes = []

    connected = True

    while connected:
        try:
            #   Aceptar la connexió del client
            conn,addr = s.accept()
            #   Threading
            th = threading.Thread(target=handle_client, args=(conn,addr,clients,productes))
            th.setDaemon(True)
            th.start()
            show_text(f"connections ready :{threading.active_count() - 1 }")
        except KeyboardInterrupt:
            show_text("Shutting the server")
            connected = False


if __name__ == "__main__":
    main()
