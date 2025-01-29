import datetime
import socket
import urllib.error
import urllib.request
import threading

#   function help
def show_text(t): print(f"{datetime.datetime.now()}   {t}")
def client_close_connection(t,conn):
    print(f"{t} Closing connection with client. {conn.getsockname()}")
    conn.close()
    return False

#   handle server - client
#   server tractament when users in
def handle(conn,nickname):
    clientConnected = True
    while clientConnected:
        try:
            #   if client dont send message in x time close the server-thread-client connection
            conn.settimeout(60)
            url  = conn.recv(1024).decode()
            if url != 'close' :
                msg = urllib.request.urlopen(url)
                conn.send(str(msg.code).encode("utf-8"))
            else:
                show_text(f"{nickname} closed connection")
                clientConnected = False
                conn.close()
        #   Managment errors
        except urllib.error.HTTPError as e:
            senderror = f"HTTPError {e.code}"
            conn.send(senderror.encode("utf-8"))
           
        except urllib.error.URLError as e:
            senderror = f"URLError {e.reason}"
            conn.send(senderror.encode("utf-8"))
            
        except ValueError as e:
            atribute = str(e)
            conn.send(atribute.encode("utf-8"))
        #   never used
        except BrokenPipeError as e:
            print("Error with the pipe")
        except socket.timeout:
            clientConnected = client_close_connection(f"Client passed time. ", conn)
        #   Other errors with link
        except Exception as e:
            clientConnected = client_close_connection(f"Except error. {e}", conn)
            
#   connection server
def connection():

    try:
        ip = "localhost"
        port = 0

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip,port))
        server.listen()

        show_text(f"server connnected at {server.getsockname()}")


        sConnected = True
        while sConnected:

            conn, addr = server.accept()

            conn.send("NICK".encode("utf-8"))
            nickname = conn.recv(1024).decode()

            show_text(f"{addr} with name {nickname} connected")

            th = threading.Thread(target=handle, args=(conn,nickname))
            th.start()
    except BrokenPipeError:
        print("Broken connection")
        
    except Exception as e: 
        print(e)
    finally:
        return server
    
if __name__ ==  "__main__":
    try:
        server = connection()
    except KeyboardInterrupt:
        print("Server interrupted")
    except BrokenPipeError:
        print("Broken connection")
    finally:
        print("Server closed")

