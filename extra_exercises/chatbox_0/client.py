import datetime
import socket
import sys
import threading

def show_text(t): print(f"{datetime.datetime.now()}   {t}")


#   common errors, send >> encode, recv >> decode
#                   client close if server also close, if not, recive messages will be alive because it doesnt close -> waits messages > and close
#                   try-except into bucles


def recive_message(conn,nickname):
    global clientConnected
    clientConnected = True
    #   while client connected
    while clientConnected:
        try:
            message = conn.recv(1024).decode()
            if  message == "NICK":
                conn.send(nickname.encode("utf-8"))
            else:
                if message:
                    print(message)
                else:
                    conn.close()
                    clientConnected = False
        except:
            show_text("Closing recive-message service.")
            conn.close()
            clientConnected =  False

            
def send_message(conn,nickname):
    global clientConnected
    clientConnected = True
    while clientConnected:
        try:
            message = input("")
            if message == "disconnect":
                conn.send(message.encode("utf-8"))
                clientConnected = False
                conn.close()
                show_text("Trying to close connection.")
            else:
                message = "{} : {}".format(nickname,message)
                conn.send(message.encode("utf-8"))
        except:
            conn.close()
            clientConnected = False
            show_text("Closing send-message service.")



def main():

    #   server info
    ip = sys.argv[1]
    port = int(sys.argv[2])
    #   info

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        
        client.connect((ip,port))

        show_text(f"Connected in server {ip} : {port}")
        print("If no message is sent within 60 seconds the client will be closed, when sending the next message if this time has elapsed the client will be notified of the closure.")
        nickname = input("Choose your name: >")

        recThread = threading.Thread(target=recive_message, args=(client,nickname))
        recThread.start()
        sendThread = threading.Thread(target=send_message, args=(client,nickname ))
        sendThread.start()


    except Exception as e:
        show_text(f"Error ocurred trying to connect. {e}")




if __name__ == "__main__":
    if len(sys.argv) >= 3:
        try:
            main()
        except Exception as e:
            show_text(f"Error ocurred. {e}")
    else:
        show_text(f"Arguments required: SERVER-IP, SERVER-PORT")