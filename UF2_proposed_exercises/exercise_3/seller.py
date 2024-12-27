import sys
import datetime
import time
from random import randrange as rand
from SellerManagment import Product
import socket


#   0 = CONTINUE
#   1 = STOP
#   2 = WANT
def number(max):
    return str(rand(0,max))

def election(number):

    if number == '0':
        return 'Keep'
    elif number == '1':
        return 'Stop'
    elif number == '2':
        return 'Sale'

def main(information,newIp,newPort):
    
    #   INFO CONNECTION
    ip = str(newIp)
    port = int(newPort)
    #   CONNECTION
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip,port))   # !Tuple
    #   PRODUCTE        name            price
    myProduct = Product(information[1],information[2],"Purchase",ip)
    #   ENVIAR INFORMACIO DEL PRODUCTE
    client.send(str("seller,"+information).encode("UTF-8"))
    #   Mentre estigui connectad




    connected = True
    while(connected):
        #   Agafa la resposta del comprador, Continue,Want,Stop
        buyerResponse = client.recv(1024).decode()
        response = buyerResponse.split(",")

        #Client vol continuar baixant la aposta
        if response[0] == "Continue":
            newPrice = "Keep,"+"10"
            client.send(str(newPrice).encode("UTF-8"))
            print(f"SELLER ENVIA: {str(newPrice)}")
            


        elif response[0] == "Want":
            client.send(str("Sale").encode("utf-8"))
            connected = False
        elif response[0] == "Stop":
            print("--CANCEL SALE-- Buyer don't wanna buy this product.")
            client.send(str("Stop").encode("UTF-8"))
            connected = False
      
    client.close()

if __name__ == "__main__":
    information = str(sys.argv[1])
    
    #   PRODUCT : SELLER,NAME,PRICE
    #   CONNECTION :  IP, PORT
    try:
        main(information,sys.argv[2],sys.argv[3])
    except KeyboardInterrupt:
        print("< KeyboardInterrupt: Closing connection.")
        
