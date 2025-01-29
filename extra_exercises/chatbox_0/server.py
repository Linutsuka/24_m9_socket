import datetime
import socket
import threading

lock = threading.Lock()

def show_text(t): print(f"{datetime.datetime.now()}   {t}")

#   common errors: be sure to send >> encode and reciv >> decode
#                   port needs parse-int
#                   be sure to append all the information into arrays
#                   secure no send void messages to other users
#                   secure closing connection

#   important c send the messages, not conn, it only 4compare
def broadcast(co,clients,m):
    for c in clients:
        if c != co:
            c.send(m)
            show_text(f"send {c.getpeername()} message {m.decode()}")

def close_connection(conn,cl,nicknames):
    with lock:
        index = cl.index(conn)
        cl.remove(conn)
        nickname = nicknames[index]
        broadcast(conn,cl,f"{nickname} left the chat".encode("utf-8"))
        nicknames.remove(nickname)
        conn.close()
    return False

def handle(conn,cl,nicknames):
    clientConnected = True
    while clientConnected:
        try:
            conn.settimeout(60)
            message = conn.recv(1024).decode()
            if message and message != "disconnect" and not message:
                print(message)
                broadcast(conn,cl,message.encode("utf-8"))
            if message == "disconnect":
                show_text(f"User: {conn.getpeername()} closed connection.")
                clientConnected = close_connection(conn,cl,nicknames)
            if not message:
                print("No-message detected error")
                clientConnected = close_connection(conn,cl,nicknames)
        except TimeoutError:
            show_text(f"Time out closing connection. User: {conn.getpeername()} closed connection.")
            clientConnected = close_connection(conn,cl,nicknames)
        except Exception as e:
            show_text(f"Error ocurred tryng to talk-clients {e}")
            clientConnected = close_connection(conn,cl,nicknames)
            break
        

def main():
    

    #   server information and data
    ip = '192.168.3.179'
    port = 65531

    clients = []
    nicknames = []

    #   server connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen()
    show_text(f"Server listenning connections at {server.getsockname()}")

    connectedServer = True
    try:
        while connectedServer:
                conn,addr = server.accept()
                show_text(f"Client connected with connection {conn.getsockname()}")
                #   ask connection
                conn.send("NICK".encode("utf-8"))
                nickname = conn.recv(1024).decode()
                show_text(f"Recibed nickname: {nickname} from {conn.getsockname()}")

                clients.append(conn)
                nicknames.append(nickname)

                broadcast(conn,clients,f"{nickname} joined!".encode("utf-8"))
                th = threading.Thread(target=handle, args=(conn,clients,nicknames))
                th.start()
               
    except Exception as e:
        print(f"Error in connection {e}")
        



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("keyboard interrupted server")
    except  Exception as e:
        print(f"external error {e}")