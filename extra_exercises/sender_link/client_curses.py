import curses
import datetime
from time import sleep
import socket
from sys import argv
import threading


window = curses.initscr()
curses.newwin(100,200,0,0)
curses.start_color()
curses.curs_set(0)


#   curses functions
def input_curses(t):
    window.addstr(t)
    special_chars = [
    '$', '&', '%', '+', ',', '/', ':', ';', '=', '?', '@', '#',
    '[', ']', '{', '}', '|', '\\', '^', '~', '`', '<', '>', '"', "'","."]

    nonstop = True
    text = ''
    while nonstop:
        letter = window.getch()
        if chr(letter).isalpha() or chr(letter).isnumeric() or chr(letter) == " ":
            text += chr(letter)
        elif chr(letter) in special_chars:
            text += chr(letter)
        if letter == 10:
            nonstop = False
    return text
def show_text(t):
    
    curses.init_pair(5,2,0)
    window.addstr(f"{datetime.datetime.now()}    {t}\n", curses.color_pair(5))
    window.refresh()
def print_c(t):

    window.addstr(f"{t}\n")
    window.refresh()
def close_curses():
    print_c("Press any key to log out.")
    window.getch()
    curses.napms(1000)
    curses.endwin()
    
#   handle client - server
def handle(conn, nickname):
 
    print_c(f"Hello,{nickname}! Remember send with http/s")
    sleep(1)
    clientConnected = True
    while clientConnected:
        try:
                
                url = input_curses(">")
                if url == '': url = "Sended nothing"
                conn.send(url.encode("utf-8"))
                
                msg = conn.recv(1024).decode()
                if msg:
                    print_c(f"{msg}")
                else:
                    print_c(f"Goodbye {nickname}!")
                    clientConnected = False
                    conn.close()
                    close_curses()
                #window.refresh()

        except Exception as e:
            print_c("closing connection")
            conn.close()
            close_curses()

#   principal connection
def connection():
    try:
        ip = argv[1]
        port = int(argv[2])

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip,port))

        nickname = input_curses("your nickname>")
        
        show_text(f"client connected at {client.getsockname()}\n")

        client.recv(1024)
        client.send(nickname.encode("utf-8"))

        th = threading.Thread(target= handle, args=((client,nickname)))
        th.start()
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