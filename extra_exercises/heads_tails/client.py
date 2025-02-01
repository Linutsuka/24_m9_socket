import datetime
import socket
from random import randrange
import threading
import time

def show_text(t): print(f"{datetime.datetime.now()}  ({t})")
def random(number):
    return randrange(0,number)
def option(n):

    if n == 0: return "TAILS"
    elif n == 1: return "HEADS"
    else: return "HEADS"

if __name__ == "__main__":
    #   connect server
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("192.168.1.38",63541))
    nickname = input("choose your nickname: >")
    client.send(nickname.encode())
    show_text(f"connected to server, client info {client.getpeername()}")
    #
    clientConnected = True
    while clientConnected:
        try:
            time.sleep(2)
            coin = option(random(3))
            #
            client.send(coin.encode())
            msg = client.recv(1024).decode()
            
            if msg == "HEADS":
                print(msg)
    
            elif not msg or msg == "TAILS":
                client.close()
                clientConnected = False
                print(msg)
                print("You lost the game!")
        except Exception as e:
            print(f"Main: {e}")




