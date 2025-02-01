import socket
import threading

def broadcast(conn, client,msg):
    for c in client:
        if c != conn:
            c.send(msg)
            print(f"{conn.getpeername()} sended {msg.decode()}")
def allplaying(client):
    for c in client:
        c.send("start!!".encode("utf-8"))
       

def close_connection(conn,client,nicknames):
    index = client.index(conn)
    client.remove(conn)
    nickname = nicknames[index]
    nicknames.remove(nickname)
    broadcast(conn,client,f"{nickname} left the chat\nYou win the game.".encode("utf-8"))
    return False

def handle(conn,client,nicknames):
    clientConnected = True
    startSended = True
    while clientConnected:
        # si hay dos usuarios en marcha
        if len(client) == 2 and startSended:
            # send all players start
            # el mensaje start se enviara 2 veces porque hay dos clientes, sino cambiar a broadcast
            allplaying(client)
            startSended = False
            #client sended ok
            msg = conn.recv(1024)
            print(f"ready client {conn.getpeername()} sended {msg.decode()}")
           
        if startSended == False:
            try:
                
                msg = conn.recv(1024).decode("utf-8")
                if msg:
                    if msg != "disconnect":
                        broadcast(conn,client,msg.encode("utf-8"))
                    else: clientConnected = close_connection(conn,client,nicknames)
            except Exception as e:
                print(f"{e}")
                clientConnected = close_connection(conn,client,nicknames)            

if __name__ == "__main__":
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("192.168.1.38",65431))
        server.listen(2)
        print(f"server connect at {server.getsockname()}")
        print("Paper,rock and tisors game server, if server shutdown clients will closed automatically.")
        client = []
        nicknames = []
        serverConnected = True
        while serverConnected:
            conn, addr = server.accept()
           
            #   send and recive information user
            #conn.send("NICK".encode("utf-8"))
            nickname = conn.recv(1024).decode()
            client.append(conn)
            nicknames.append(nickname)
            # info notify
            print(f"user: {nickname} with {addr} connected")
           
            #   thread
            th = threading.Thread(target=handle, args=(conn, client, nicknames), daemon=True)
            th.start()

    except KeyboardInterrupt:
        print("Keyboard Interrupted: Server will close and clients.")
        serverConnected = False
        server.close()
    except Exception as e: print(e)
        