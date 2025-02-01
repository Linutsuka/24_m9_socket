import datetime
import socket
import threading

def show_text(t): print(f"{datetime.datetime.now()}  ({t})")

def close_connection(conn,client,nicknames):
    try:
        if conn in client:
            index = client.index(conn)
            client.remove(conn)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            print(f"user: {nickname} left the game connection: {conn.getpeername()}")
    except Exception as e:
        print(f"Close connection: {e}")
def getName(conn,client,nicknames):
    if conn in client:
        index = client.index(conn)
        return nicknames[index]

def handle(conn,client,nicknames):
    clientConnected = True
    while clientConnected:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                #print(msg)
                if msg == "TAILS":
                    conn.send("TAILS".encode())
                    clientConnected = close_connection(conn,client,nicknames)
                else:
                    conn.send("HEADS".encode())
                    print(f"user: {getName(conn,client,nicknames)} keep playing connection: {conn.getpeername()}")
            else:
                clientConnected = close_connection(conn,client,nicknames)

        except Exception as e:
            clientConnected = close_connection(conn,client,nicknames)
            print(f"Handle: {e}")

    
if __name__ == "__main__":
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("192.168.1.38",63541))
        server.listen()
        show_text("connected")
        # save
        client = []
        nicknames = []

        clientConnected = True
        while clientConnected:

            conn,addr = server.accept()
            #   server interaction
            conn.send("NICK".encode())
            nickname = conn.recv(1024).decode()

            #
            client.append(conn)
            nicknames.append(nickname.title())

            th = threading.Thread(target=handle, args=(conn,client,nicknames))
            th.start()
    except KeyboardInterrupt: print("Keyboard Interrupt")
    except Exception as e: print(f"Main: {e}")
