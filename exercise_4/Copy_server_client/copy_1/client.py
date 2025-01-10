import curses
import datetime
import socket
import sys
import threading


#   Open curses window
w = curses.initscr()
curses.curs_set(0)
curses.start_color()
color = 7

#   HELP FUNCTIONS
def show_text(t):print(f"{datetime.datetime.now()} {t}")

#   CURSES FUNCTION
def printc(t):
    curses.init_pair(1,curses.COLOR_GREEN,0) 
    w.addstr(str(t+"\n"), curses.color_pair(1)) 
    w.refresh()
   

def show_ctext(t):
    w.addstr(f"{datetime.datetime.now()} {t}\n") 
    w.refresh()
#   Let user write and send the result, close with KEY_ENTER pulse. Return string.
def input_write(t):
    w.addstr(t)
    nonstop = True
    text = ''
    while nonstop:
        letter = w.getch()
        if chr(letter).isalpha() or chr(letter).isnumeric() or chr(letter) == " ":
            text += chr(letter)
        if letter == 10:
            nonstop = False

    w.addstr(text+"\n")
    return text

#   Inform user what colors can choose to start talk. If any color of the list are selected choose again. Return number
def input_color():
    #   colors on: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan y 7:white.
    text = "0.Black, 1.Red, 2.Green, 3.Yellow, 4.Blue, 5.Magenta, 6.Cyan, 7.White"
    w.addstr(f"Choose [the number of the color] what reprents better to you:\n\t {text}")
    colors_number = {"0","1","2","3","4","5","6","7"}
    non_color_choose = True
    while non_color_choose:
        color_choosed = input_write("").strip()
        
        if color_choosed in colors_number:
            curses.init_pair(1,3,0) 
            w.addstr(f"Color choosed! Number: {color_choosed}", curses.color_pair(1))
            w.refresh()
            non_color_choose = False
        else:
            w.addstr(f"The number {color_choosed} isn't any color. Choose: {text}")
            w.refresh()
    return int(color_choosed)
#   Qué es miau? connected pero connected falla así que miau.

global miau
miau = True

# Rep missatje del sevidor. Si el missatje es NICK envia nickname. Si es qualsevol cosa, printeja el missatje.
def receive_message(cl, nickname):

    global miau
    while miau:
            try:
                
                message = cl.recv(1024).decode('utf-8')
                if message == 'NICK':
                    cl.send(nickname.encode('utf-8'))
                else:
                    printc(message)
            except:
                show_ctext("an error occured!")
                cl.close()
                miau = False
                break
        
   


#   Envia missatje al servidor. Envia un string amb primer el nickname i després el texte del input.
def send_message(cl, nickname):
    global miau
    try:
        while miau:
                m = input_write("")
                if m != "disconnect":
                    message = '{}: {}'.format(nickname, m)
                    cl.send(message.encode('utf-8'))
                else:
                    
                    cl.send(m.encode('utf-8'))
                    miau  = False
                    printc("Closing")
                    break
    except:
        printc("error")

def main():

    printc("Press the enter button to accept or send messages.\nTo disconnect from the server, type disconnect.")
    
    printc("Starts:\n")
  
    nickname = input_write("Choose your name: ")
    w.refresh()
    #color = input_color()
    #nickname += "$"+str(color)
    

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((sys.argv[1],int(sys.argv[2])))

    show_ctext(f"{nickname} {client.getsockname()[0]}:{client.getsockname()[1]}") 

    #   Fils.
    receive = threading.Thread(target=receive_message, args=(client, nickname)) #   Llegir missatjes.
    receive.start()

    write = threading.Thread(target=send_message, args=(client, nickname))  #   Envia missatjes.
    write.start()

    return client


if __name__ == "__main__":
    try:
        main()


    except KeyboardInterrupt:
        printc("Error keyboard.")
        curses.endwin()
    except Exception as e:
        printc(f"Closing connexion. {e}")