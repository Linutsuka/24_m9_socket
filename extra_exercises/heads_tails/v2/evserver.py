import socket
from time import sleep
import threading

def close_connection(conn):
   if conn in client:
       index = client.index(conn)
       client.remove(conn)
       nickname = nicknames[index]
       nicknames.remove(nickname)
       print(f"removed user: {nickname}")
       
def handle(conn):
    clientCOnnected = True
    while clientCOnnected:
        try:
            msg = conn.recv(1024).decode()
            event.wait()
            if msg:
                if msg == "HEADS":
                    if len(client) > 1: msg = "200"
                    else: msg = "Winner"
                    conn.send(msg.encode())
                else:
                    #conn.send("400".encode())
                    clientCOnnected = close_connection(conn)
        except:
            print(f"Handle: {e}")
            clientCOnnected = close_connection(conn)

if __name__ == "__main__":
    try:
        users = 3
        # server connection
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("localhost",65431))
        server.listen(3)
        print(f"Server listenning at {server.getsockname()}")
        # info saved
        client = []
        nicknames = []
        #
        event = threading.Event()
        #  
        for _ in range(users):
            conn, addr = server.accept()

            client.append(conn)
            nickname = conn.recv(1024).decode()
            nicknames.append(nickname)
            print(f"user: {nickname.title()} connected conn: {conn.getpeername()}")

            th = threading.Thread(target=handle, args=(conn,))
            th.start()
       
        while len(client) > 1:
            print("---------")
            event.clear()
            sleep(2)
            event.set()


        print("Game Closed")
        server.close()
    except Exception as e:
        print(f"Main: {e}")