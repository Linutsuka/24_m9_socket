import socket
from sys import argv
import threading
from random import randrange

def receive_message(conn,nickname):
    clientConnected = True
    begin = False
    dice = ''
    try:
        while clientConnected:
            m = conn.recv(1024).decode("utf-8")
            print(f" server sended {m}")
            # if reciv nothing from server, server closed interrupted
            if not m:
                print("server disconnected")
                break
            # else
            if m == "NICK":
                conn.send(nickname.encode("utf-8"))
            if m == 'ready':
                print("get ready!")
                begin = True
            if dice == m:
                print("You lose the game!")
                begin = False
                conn.close()
                clientConnected = False
                break
            if m == "WIN":
                print("you win the game!")
                clientConnected = False
                conn.close()
                break
            elif begin == True:
                sm = input(">")
                dice = str(randrange(0,6))
                print(f" number sended!: {dice}")
                conn.send(dice.encode("utf-8"))
           
                            
              

    except Exception as e:
        print("Server close!")
        print(e)

def connexion():
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((argv[1],int(argv[2])))

    nickname = input("Write your name: >")

    print(f"client connected at {client.getsockname()}")
    print(f"Rules:  - When the game starts write whatever, it will be your dice.\nWhen the four player send it the gamemaster will send his dice.\nIf are the same you will be killed.\nWin player will be the last death.")

    r = threading.Thread(target=receive_message,args=(client,nickname))
    r.start()



if __name__ == "__main__":
    connexion()