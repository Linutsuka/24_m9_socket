import socket
import threading
from random import randrange
from time import sleep
def random(number):
    return randrange(0,number)
def option(n):

    if n == 0: return "TAILS"
    elif n == 1: return "HEADS"
    else: return "HEADS"

def close_connection(c,msg):
    c.close()
    print(msg)
    return False
if __name__ == "__main__":
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(("localhost",65431))
        #
        client.send(input("choose your name: ").encode())
        sleep(2)

        serverConnection = True
        while serverConnection:
            try:
                coin = option(random(4))
                client.send(coin.encode())
                print(f"send: {coin}")
                msg = client.recv(1024).decode()
                if msg:
                    if msg == "200":    print("Keep playing!")
                    else:   serverConnection = close_connection(client,msg)
                else:   serverConnection = close_connection(client,"You lose the game!")
                    

            except Exception as e: 
                print(f"Client: {e}") 
                serverConnection = False
    except Exception as e:
        print("Main: {e}")