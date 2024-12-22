import socket
import threading
ip = 'localhost'
port = 65530





def brodcast_send(conn,clients,message):
    for c in clients:
        if c != conn:
            c.send(message)

def brodcast_recv(conn,clients):
    for c in clients:
        if c != conn:
            message = c.recv(1024).decode()
            return message


def handle(conn,addr,clients):
    connected = True
    clients.append(conn)
    try:
        while connected:
            if len(clients) == 2:
                message = conn.recv(1024).decode()
                print(f"message recibido {message}")
                brodcast_send(conn,clients,message.encode("utf-8"))
                print(f"message send to address{conn}")
                connected = False


    except:
        print("error")
        


try:
    clients = []
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen()
    print(f"SERVER RUN ADDRESS{s.getsockname()}")
    connected = True

    while connected:
        conn,addr = s.accept()
        print(f"ADDRESS CONNECTED to SERVER{addr}")
       
        th = threading.Thread(target=handle, args=((conn,addr,clients)))
        th.start()

except KeyboardInterrupt:
    print("error")
    s.close()
