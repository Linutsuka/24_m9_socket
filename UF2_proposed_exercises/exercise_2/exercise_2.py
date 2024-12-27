import datetime
import socket
import threading
from random import randrange as rand

#   VARIABLES
ip = '192.168.3.179'  # Sempre en string  
port = 65530    #  Sempre en int


#
def show_test(t):
    print(f"{datetime.datetime.now()} {t}")

#   Crea random 0,1, si es 0 pots seguir jugant, si es 1 perds no pots seguir jugant
def response_coin():
    coin = rand(0,2)
    return coin

#   Maneja el client, agafa la connexio i la adreça
def handle_client(co,ad,lastWinner):
    show_test(f" new connection on {ad}")
    connected = True
    myCoins = 1
    while connected:
        msg = co.recv(1024).decode("utf-8")
        if msg == "DISCONNECT":
            show_test(f"disconnect {ad}")
            connected = False
        else:
            name = msg
    
            msg = response_coin()
            
            if msg == 0:    #   CORRECT COIN
                show_test(f"send to {ad}  HEAD")
                myCoins += 1
                # SI TINC MÉS COINS QUE EL ÚLTIM GUANYADOR EM CORONO COM GUANYADOR
                if myCoins >= lastWinner[1]:
                    lastWinner[0] = ad
                    lastWinner[1] = lastWinner[1]+1
                    lastWinner[2] = name
                sendwinner = (f" LASTWINNER{lastWinner[0]} with name: {lastWinner[2]} COINS: {lastWinner[1]}")
                co.send(("HEAD"+sendwinner).encode("UTF-8"))
            else:   #   FAILED COIN
                sendwinner = (f" LASTWINNER{lastWinner[0]} with name: {lastWinner[2]} COINS: {lastWinner[1]}")
                co.send(("TAILS"+sendwinner).encode("UTF-8"))
                #   DEIXA DE JUGAR
                show_test(f"send to {ad} TAILS")
                show_test(f"DISCONNECT  {ad}")
                connected = False
        
                print(f"LAST WINNER:{lastWinner}")
    co.close() 


def main():
    show_test("start")
    #                 CONSTANT:   IPV4        TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,port))   #   Connexió
    show_test(f"listen for connections {s.getsockname()}")
    s.listen() #   Listen a lot of connections
    lastWinner = ['',1,'']
    #   ---
    connected = True
    while connected:
        try:
            conn,addr = s.accept()
            #   lastClient who has thrown face
            
            th = threading.Thread(target=handle_client, args=(conn,addr,lastWinner))
            th.start()
            show_test(f" active connextions {threading.active_count() - 1}")
        except KeyboardInterrupt:
            show_test("\nshutting down the server")
            connected = False
           


if __name__ == "__main__":
    print(f"{datetime.datetime.now().strftime('%H:%M:%S.f')} waiting ...")
    main()
