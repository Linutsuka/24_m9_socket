import datetime 
from random import randrange as rand
import sys
import socket


def show_text(t):
    print(f"{datetime.datetime.now()} {t}")

#   0 = CONTINUE
#   1 = STOP
#   2 = WANT
def number(max):
    return str(rand(0,max))

def election(number):

    if number == '0':
        return 'Continue'
    elif number == '1':
        return 'Stop'
    elif number == '2':
        return "Want"


def main():

    ip = str(sys.argv[1])
    port = int(sys.argv[2])
   
    #   Connection
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip,port))   # !Tuple
    show_text(f"CONNECTED to: {ip}   {port}")
    #   Notificar server

    #   Enviar al servidor el status 'buyer'
    client.send(str("buyer").encode("UTF-8"))
    #   Pujar
    connected = True
    while(connected):
        msg = ""
        sellerSend = client.recv(1024).decode().split(",")
        if sellerSend[0] == "Keep":
            msg = str(election(number(3)))
            client.send(msg.encode("utf-8"))
            print(f"--ELECTION BUYER-- {msg}")

        # BUCLES PRINCIPALES
        elif sellerSend[0] == "Wait":
            print(sellerSend[1])
        elif sellerSend[0]:
             print(sellerSend)

if __name__ == "__main__":
    main()