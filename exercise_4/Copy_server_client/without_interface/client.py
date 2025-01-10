import curses
import datetime
import socket
import sys
import threading


def show_text(t):print(f"{datetime.datetime.now()} {t}")


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
                    print(message)
            except:
                show_text("an error occured!")
                cl.close()
                miau = False
                break
        
   


#   Envia missatje al servidor. Envia un string amb primer el nickname i després el texte del input.
def send_message(cl, nickname):
    global miau
    try:
        while miau:
                m = input("")
                if m != "disconnect":
                    message = '{}: {}'.format(nickname, m)
                    cl.send(message.encode('utf-8'))
                else:
        
                    cl.send(m.encode('utf-8'))
                    miau  = False
                    print("Closing")
                    break
    except:
        print("error")

def main():

    show_text("Starts:")
    nickname = input("Choose your name: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((sys.argv[1],int(sys.argv[2])))

    show_text(f"{nickname} {client.getsockname()[0]}:{client.getsockname()[1]}") 

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
        print("Error keyboard.")
    except:
        print("Closing connexion.")