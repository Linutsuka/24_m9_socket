import datetime as dati
import socket
from random import randrange
from time import sleep
import threading

def show_text(t):print(f"{dati.datetime.now()}   {t}")


def send_all(cl,m):
    for c in cl:
        c.send(m.encode("utf-8"))
#   send to all user unless the connexion
def brodcast(cn, cl, m):
    for c in cl:
        if c != cn:
            c.send(f"{m}".encode("utf-8"))

def random():
    return str(randrange(0, 6))

#   close all the connexions
def all_close(cl):
    with list_lock:
        for c in cl:
            c.close()
        cl.clear()
#   close connexion:
def close_connexion(conn,cl,nickname,number_players):
    print(f"Client closed")
    if conn in cl:
            index = cl.index(conn)
            print(f"Removing client at index: {index}")
            cl.remove(conn)
            nickname.pop(index)
            number_players = number_players -1
    return number_players

#   protect variable from others threads
list_lock = threading.Lock()


#   thread handle server
def handle(conn, cl, nickname):
    global number_players
    number_players = 3
    clientConnected = True
    begin = False
    global nm_s
    nm_s = 0

    while clientConnected:
        if len(cl) == number_players and begin == False:
            print("sended ready to players!")
            if conn in cl:
                conn.send("ready".encode("utf-8"))
                begin = True
            else:
                clientConnected = False
        try:
            while begin:
           
                m = conn.recv(1024).decode("utf-8")

                if not m:  # Si el mensaje está vacío
                    with list_lock:
                        number_players = close_connexion(conn,cl,nickname,number_players)
                        clientConnected = False
                        print(",".join(nickname))
                        conn.close()
                    


                if m:
                    print(f">server recv {m}")
                    #   sumar el valor de las respuestas de los usuarios
                    with list_lock:
                        if m:
                            nm_s += 1
                    s = random()
                    #   si solo queda un usuario en la lista
                    if len(cl) == 1:  # only 1 client
                        with list_lock:
                            if conn in cl:
                                conn.send("WIN".encode("utf-8"))
                                index = cl.index(conn)
                                print(f"user with nickname: {nickname[index]}")
                                print("win")
                                all_close(cl)
                                begin = False
                                clientConnected = False

                    #   si el numero de clientes es el mismo que respuestas y es el mismo que players
                    print(f"{len(cl)}  {nm_s}  {number_players}")
                    if len(cl) > 1 and nm_s == number_players:
                        send_all(cl,s)
                        print(f"server sent: {s}")
                        nm_s = 0

            #   close connection user managment
        except Exception as e:
                print(f"Error with a client: {e}")
                with list_lock:  # protect the list
                   number_players = close_connexion(conn,cl,nickname,number_players)
                conn.close()  # close actual conn
                clientConnected = False 
    print("--connexion closed!")
#   connexion
def connexion():
    client = []
    nickname = []
    ip = "localhost"
    port = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(3)
    show_text(f"server [open] ready to listen connections at {server.getsockname()} needs 3 people to start")
    server_open = True

    while server_open:
        conn, addr = server.accept()  # Aceptar la conexión
        # Enviar solicitud de nickname
        conn.send("NICK".encode("utf-8"))
        nick = conn.recv(1024).decode()

        show_text(f"nick received {nick}     addr: {addr}")

        with list_lock:  # Proteger acceso a las listas
            nickname.append(nick)
            client.append(conn)
        # Crear un hilo para manejar al cliente
        th = threading.Thread(target=handle, args=(conn, client, nickname))
        th.start()

if __name__ == "__main__":
    try:
        connexion()
    except Exception as e:
        print(f"server close e: {e}")
