import AES
import datetime
import time
import threading
import traceback
import socket
from sys import argv


#   FUNCION HELP
def show_text(t):print(f"{datetime.datetime.now()} {t}")

def broadcast(co,clients,m):
    for c in clients:
        if c != co:
            c.send(m)
            show_text(f"send {c.getpeername()} message {m.decode('utf-8')}")

#   FUNCTION THREAD
def handle(conn,clients,key):
    
    clientConnected = True
    while clientConnected:
        try:
            message = conn.recv(1024)
            broadcast(conn,clients,message)
            if message.decode() == "disconnect":
                index = clients.index(conn)
                clients.remove(conn)
                conn.close()
                nickname = nicknames[index]
                broadcast(conn, clients, f"{nickname} left".encode('utf-8'))
                nicknames.remove(nickname)
                # >> Poner configuracion cuando este
                clientConnected = False

        except:
            print("error with a client")
            # Si algo falla se quita la información de los clientes de la array de clientes y su información relacionada.
            index = clients.index(conn)
            clients.remove(conn)
            conn.close()
            nickname = nicknames[index]
            broadcast(conn, clients, f"{nickname} left".encode('utf-8'))
            nicknames.remove(nickname)
            # >> Poner configuracion cuando este
            clientConnected = False
            break
#   encrypt auxiliar
def encrypt_key(key):
    from do_rsa import RSA_
    path = "."
    rsa = RSA_("e",path,key) 
    rsa.encrypt_txt()   #
    return  rsa.get_ciphertext()

def sende(key,m):
    m = AES.encrypt_message(key,m)
    return m
def recive(key,m):
    m = AES.decrypt_message(key,m)
    return m

#   SERVER CONNECTION

try:

    nicknames = []
    clients = []
    config = []

    ip = "localhost"
    port = 0
    connected = True

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen()

    show_text(f"Server OPEN, listening connexions at {server.getsockname()}")
    #   test
    key = argv[1].encode()   #   key without encrypt
    key = AES.key_adjust(key)

    key_encrypted = encrypt_key(key) #   create key encrypted with rsa return rsa_key
   
    #

    while connected:
        conn, addr = server.accept()
        
        conn.send(key_encrypted)
        print(key_encrypted)
        message = conn.recv(1024)
        print(f"client status key :  {AES.decrypt_message(key,message)}")
        #message = conn.recv(1024).decode("utf-8")
        time.sleep(3)  
        #   ASK NICK NAME
        conn.send("NICK".encode("utf-8"))
        nickname_color = conn.recv(1024).decode()
        #  
        print(nickname_color+"<<")
        nickname = nickname_color.split("$")[0]
        color = nickname_color.split("$")[1]
        
        #   NICKNAME AND CONFIG
        nicknames.append(nickname)
        clients.append(conn)
       

        show_text(f"New connexion ready, addr:' {addr}  '. Nickname: {nickname} || Color: {color}")
        broadcast(conn,clients,f"{nickname} joined!".encode("utf-8"))
        conn.send("connected to server!".encode("utf-8"))

        th = threading.Thread(target=handle, args= ((conn,clients,key)))
        th.start()
       
       


except KeyboardInterrupt:
    print("Keyboard Interrupt, server close.")
except Exception as e:
    print(f"Error server, server close. {e}")
    traceback.print_exc()
