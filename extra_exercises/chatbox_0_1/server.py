import datetime
import socket
import threading

def show_text (t): print(f"{datetime.datetime.now()}    {t}")



def brodcast(co,cl,msg,salas,selected):
    for c in cl:
        if c != co:
            if c in salas[selected]:
                c.send(msg)
                print(f"{co.getpeername()} send {msg.decode()}")
lock = threading.Lock()
def close_connection(conn,cl,nicknames,salas,selected):

    with lock:
        index = cl.index(conn)
        cl.remove(conn)
        nickname = nicknames[index]
        brodcast(conn,cl,f"{nickname} left the chat".encode("utf-8"),salas,selected)
        if conn in salas[selected]:
            salas[selected].remove(conn)
        nicknames.remove(nickname)
        conn.close()
    return False
#   select user sala to chat
def select_sala(conn,salas,cl,nicknames):
    noSelect = True
    sala = ''
    while noSelect:
        try:
            conn.send(f"Salas number: {len(salas)} Select number: [1 to {len(salas)}]  [0] Is lobby  [555] See users".encode("utf-8"))
            msg = str(conn.recv(1024).decode()).split(":")[1].replace(" ","")
            if not msg.isnumeric():
                msg = '0'
                print("nonumeric"+msg)
            if msg != '555':
                print("no 555"+msg)
                for n in range(len(salas)):
                    if int(msg) == int(n):
                        noSelect = False
                        sala = msg
                        break
                return int(sala)
            else:
                print("user entry")
                conn.send(f"Salas number: {len(salas)}: Select number to see: [1] to {len(salas)}] [0] is lobby".encode("utf-8"))
                msg = str(conn.recv(1024).decode()).split(":")[1].replace(" ","")
                if not msg.isnumeric():
                    conn.send("Only numeric numbers")
                else:
                    show_users_sala(conn,cl,salas,nicknames,msg)
                
        except: 
            print(msg)
            return 0
def exit_sala(conn,salas,selected,cl,nicknames):

    salas[selected].remove(conn)
    return select_sala(conn,salas,cl,nicknames)

#   show sala users 
def show_users_sala(conn,cl,salas,nicknames,selected):
    users = []
    try:
        for c in salas[selected]: 
            index = cl.index(c)
            users.append(nicknames[index])   
        conn.send("->".join(users).encode("utf-8"))
    except Exception as e:
        show_text(f"error sending sala users   : {e}")

#   get nickname client
def getNickName(conn,clients,nicknames):
    index = clients.index(conn)
    nickname = nicknames[index]
    return nickname

#   client handler
def handle(conn,clients,nicknames,salas):
    # salas first select
    sala_selected = select_sala(conn,salas,clients,nicknames)
    print(f"user: {conn.getpeername()} selected: {sala_selected}")
    salas[sala_selected].append(conn) if sala_selected != -1 else salas[0].append(conn)
    #   remove connection from the lobby if they choose other sala
    if sala_selected != 0:
        salas[0].remove(conn)
    #   anunce wich loby entry
    conn.send(f"Hey {getNickName(conn,clients,nicknames)}! Sala: {sala_selected}".encode("utf-8"))
    
    clientConnect = True
    while clientConnect:
        try:
            msg = conn.recv(1024)
            if msg.decode() == "sala-config":
                conn.send("[exit]-[users]".encode("utf-8"))
                msg = conn.recv(1024)
                if msg.decode() == "exit":
                    msg = f"{getNickName(conn,clients,nicknames)} left the sala!".encode("utf-8")
                  
                    brodcast(conn,clients,msg,salas,sala_selected)
                    sala_selected =  exit_sala(conn,salas,sala_selected,clients,nicknames)
                    salas[sala_selected].append(conn) if sala_selected != -1 else salas[0].append(conn)
                    
                elif msg.decode() == "users":
                     show_users_sala(conn,clients,salas,nicknames,sala_selected)
                else:
                    conn.send(f"Server: You don't choose any option given. Message sended: {msg.decode()}".encode("utf-8"))
            elif msg.decode() == "disconnect":
                clientConnect = close_connection(conn,clients,nicknames,salas,sala_selected)
            else:
                if msg:
                    brodcast(conn,clients,msg,salas,sala_selected)
        except KeyboardInterrupt:
            print("closed connection with keyboard interrupt")
            clientConnect = close_connection(conn,clients,nicknames,salas,sala_selected)
        except Exception as e:
            show_text(f"user error : {e}")
            clientConnect = close_connection(conn,clients,nicknames,salas,sala_selected)
            
def main():
    #info server
    ip = '192.168.3.179'
    port = 65432

    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen()
    show_text(f"Server open listening connections at {server.getsockname()}")
    
    serverConnected = True

    #info clients
    clients = []
    nicknames = []
    #   loby: 0
    salas = [[],[],[],[]]

    while serverConnected:
        try:
            conn, addr = server.accept()
         

            clients.append(conn)
            salas[0].append(conn)
            conn.send("NICK".encode("utf-8"))
            nickname = conn.recv(1024).decode()
            nicknames.append(nickname)
            show_text(f"user: {addr} , name: {nickname}")
            brodcast(conn,clients,f"{nickname} join the lobby!".encode("utf-8"),salas,0)
            th = threading.Thread(target=handle, args=(conn,clients,nicknames,salas))
            th.start()
        except Exception as e:
            print(f"Error connecting. {e}")




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        global server
        server.close()
        print("keyboard interrupted")
        
    except Exception as e:
        print({e})