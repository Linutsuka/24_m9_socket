import datetime
import threading
import socket

#   FUNCION HELP
def show_text(t):print(f"{datetime.datetime.now()} {t}")

def broadcast(co,clients,m):
    for c in clients:
        if c != co:
            c.send(m)
            show_text(f"send {c.getpeername()} message {m.decode('utf-8')}")

#   FUNCTION THREAD
def handle(conn,clients):
    
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

    while connected:
        conn, addr = server.accept()

        # ASK NICK NAME
        conn.send("NICK".encode("utf-8"))
        nickname = conn.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(conn)

        show_text(f"New connexion ready, addr:' {addr}  '. Nickname: {nickname}")
        broadcast(conn,clients,f"{nickname} joined!".encode("utf-8"))
        conn.send("connected to server!".encode("utf-8"))

        th = threading.Thread(target=handle, args= ((conn,clients)))
        th.start()
        show_text(f"New connexion ready, addr:' {addr}  '.")
       


except KeyboardInterrupt:
    print("Keyboard Interrupt, server close.")
except Exception as e:
    print("Error server, server close.")
