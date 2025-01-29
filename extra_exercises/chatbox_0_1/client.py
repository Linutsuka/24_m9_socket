import datetime
import socket
import threading

def show_text (t): print(f"{datetime.datetime.now()}    {t}")

def close_connection(co):
    co.close()
    print("Closing thread")
    return False

def reciv_messages(co,nickname):
    orders = ["disconnect","exit","sala-config","users"]
    clientConnected = True
    while clientConnected:
        try:
            msg = co.recv(1024).decode()
            if msg:
                if msg == "NICK":
                    co.send(nickname.encode("utf-8"))
                else:
                    if msg not in orders:
                        print(msg)
            if not msg:
               clientConnected = close_connection(co)
        except:
            clientConnected = close_connection(co)
def send_messages(co,nickname):
    clientConnected = True
    orders = ["disconnect","exit","sala-config","users"]
    while clientConnected:
        try:
            msg = input(">")
            if msg:
                if msg not in orders:
                    msg ="{} : {}".format(nickname,msg)
                    co.send(msg.encode("utf-8"))
                
                else:
                    co.send(msg.encode("utf-8"))
                    if msg == "disconnect":
                        print("disconnecting user config")
                        clientConnected = close_connection(co)
        except:
            clientConnected = close_connection(co)
if __name__ == "__main__":
    try:
        #info server
        ip = '192.168.3.179'
        port = 65432
        #
        nickname = input("Write your name: >")
        #
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip,port))
        show_text(f"connected at {ip} : {port} server")
        #
        thReciv = threading.Thread(target=reciv_messages, args=(client,nickname))
        thReciv.start()
        thSend = threading.Thread(target=send_messages, args=(client,nickname))
        thSend.start()
        
    
        
    except KeyboardInterrupt:
        print("closed by interrupted keyboard")
    except Exception as e:
        print(e)