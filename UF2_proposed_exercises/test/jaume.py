import datetime as dati
import socket
import threading
import time
 
clients = []
 
def show_text(t):
    print(f"{dati.datetime.now()} {t}")
 
 
def handle_client(co, ad):
    client_name = co.recv(1024).decode("utf-8")
    show_text(f"A {client_name} enter to the server")
    connected = True
    clients.append(co)
    show_text(f"clients connected{len(clients)}")
    if len(clients) == 2:
        if client_name == "Buyer":
            while connected:
                time.sleep(3)
                print(client_name)
                #print(co.recv(1024).decode("utf-8"))
 
        if client_name == "Seller":
            while connected:
               time.sleep(3)
               print(client_name)
 
        else:
            print("Client name error")
            co.close()
 
def main():
    try:
        show_text("starts")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 65501))
        show_text(f"listens for connections on {server.getsockname()}")
        server.listen()
 
        while True:
            try:
                conn, addr = server.accept()
                th = threading.Thread(target=handle_client, args=(conn, addr))
                th.start()  
                show_text(f"active connections {threading.active_count() - 1}")
            except:
                show_text("\nshutting down the server")
                break
        server.close()
    except KeyboardInterrupt:
        server.close()
        print(f"\n{dati.datetime.now()} server interrupted!") # Control + C.
 
if __name__ == "__main__":
    main()