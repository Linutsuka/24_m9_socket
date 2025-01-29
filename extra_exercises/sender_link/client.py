import curses
import datetime
import socket
from sys import argv
import threading

#   function help
def show_text(t): print(f"{datetime.datetime.now()}   {t}")
#   handle client - server
def handle(conn, nickname):
    print(f"Hello,{nickname}! Remember send with http/s\nIf you don't send message in 60 seconds server will close!")
    clientConnected = True
    while clientConnected:
        try:
                
                url = input(">")
                if url == '': url = "Sended nothing"
                conn.send(url.encode("utf-8"))
                
                msg = conn.recv(1024).decode()
                if msg:
                    print(msg)
                else:
                    print(f"Goodbye {nickname}!")
                    clientConnected = False
                    conn.close()
        except KeyboardInterrupt as e:
            print("Keyboard Interrupted")
            conn.close()
        except Exception as e:
            print("closing connection")
            conn.close()
          


#   principal connection
def connection():
    try:
        ip = argv[1]
        port = int(argv[2])

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip,port))

        nickname = input("Write your nickname: >")
        show_text(f"client connected at {client.getsockname()}")

        client.recv(1024)
        client.send(nickname.encode("utf-8"))

        th = threading.Thread(target= handle, args=((client,nickname)))
        th.start()
          # treu l error de thread except si es tenca malament no influeix al altres fils
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print({e})
        return client
    
    

if __name__ == "__main__":
    try:
        client = connection()
    except KeyboardInterrupt:
        print("Server interrupted")
    except Exception as e:
        print(f"{e}")