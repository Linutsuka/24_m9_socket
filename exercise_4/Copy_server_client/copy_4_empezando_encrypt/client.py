import AES
import curses
import datetime
import socket
import sys
import traceback
import threading


#   Open curses window
w = curses.initscr()
curses.curs_set(0)
curses.start_color()
color = 7

#   HELP FUNCTIONS
def show_text(t):print(f"{datetime.datetime.now()} {t}")

#   CURSES FUNCTION
def printc(t,color):
    curses.init_pair(1,int(color),0) 
    w.addstr(str(t+"\n"), curses.color_pair(1)) 
    w.refresh()
def printc_t(t,color,n):
    curses.init_pair(n,int(color),0) 
    w.addstr(str(t+"\n"), curses.color_pair(n)) 
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
            curses.init_pair(2,int(color_choosed),0) 
            w.addstr(f"Color choosed! Number: {color_choosed}\n", curses.color_pair(2))
            w.refresh()
            non_color_choose = False
        else:
            w.addstr(f"The number {color_choosed} isn't any color. Choose: {text}")
            w.refresh()
    return int(color_choosed)
#   Qué es miau? connected pero connected falla así que miau.

global miau
miau = True

global key_aes 
key_aes = None 

def sende(m):
    m = AES.encrypt_message(key_aes,m)
    return m
def recive(m):
    m = AES.decrypt_message(key_aes,m)
    return m
# Rep missatje del sevidor. Si el missatje es NICK envia nickname. Si es qualsevol cosa, printeja el missatje.
def receive_message(cl, nickname):

    global miau
    global key_aes
    color_value = 2
    users_value = []
    key_aes = ''
    while miau:
            try:

                message = cl.recv(1024)

                if key_aes == '':
        
                    #   reciv the key encrypted with rsa
                    from do_rsa import RSA_

                    rsa = RSA_("d",".",message)
                        #   decrypt the key
                    rsa.decrypt_txt()
                    key_aes = rsa.get_ciphertext()
                    printc(str(key_aes),1)
                    printc("Recived without fails the secret key!",1)
                    #message = AES.encrypt_message(key_aes,"ACCEPT")
                    #printc(str(sende()),1)
                    message = sende("accept")
                    cl.send(message)  # Envías un mensaje indicando que aceptaste

                else:
                    message = message.decode("utf-8")
                    
                    if message == 'NICK':
                        #nickname = sende(nickname)
                        cl.send(nickname.encode('utf-8'))
                    
                    
                    if message.find("$") != -1 and message.find(":") != -1:
                        printc(message,1)
                        name_color_message = message.split("$") #   nom$color:message  >> nom  color$message
                        color_message = name_color_message[1].split(":") 
                        user_config = str(name_color_message[0]+color_message[0])
                        if user_config not in users_value:
                            users_value.append(user_config)
                        #   nom, message, color              
                        printc_t(name_color_message[0]+" : "+color_message[1], str(color_message[0]),len(user_config)+3)
                
                    else:
                        printc(message,color_value)
            except Exception as e:
                show_ctext("an error occured!")
                show_ctext(f"{e}")
               
                cl.close()
                miau = False
                
                break
        
   


#   Envia missatje al servidor. Envia un string amb primer el nickname i després el texte del input.
def send_message(cl, nickname):
    global miau
    global key_aes
    try:
        while miau:
                m = input_write("")
                if m != "disconnect":
                    message = '{}: {}'.format(nickname, m)
                    cl.send(message.encode('utf-8'))
                else:

                    cl.send(m.encode('utf-8'))
                    miau  = False
                    printc("Closing",2)
                   
                    break
    except:
        printc("error",2)

def main():

    printc("Press the enter button to accept or send messages.\nTo disconnect from the server, type disconnect.",4)
    
    printc("Starts:\n",4)
  
    nickname = input_write("Choose your name: ")
    w.refresh()

    color = input_color()
    nickname += "$"+str(color)
    

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
        printc("Error keyboard.",2)
        curses.endwin()
    except Exception as e:
        printc(f"Closing connexion. {e}",2)