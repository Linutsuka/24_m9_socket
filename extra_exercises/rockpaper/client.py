import socket
import threading

def compare_play(msgsend, msgrec):

    if msgsend == msgrec:
        return 0 
    #   rock vs papel
    elif msgsend == "paper" and msgrec == "rock":
        return -1
    # paper vs tisors
    elif msgsend == "paper" and msgrec == "tisors":
        return -1
    # tisors vs rock
    elif msgsend == "tisors" and msgrec == "rock":
        return -1
    else:
        return 0
    
if __name__ == "__main__":
    life_points = 3
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       
        client.connect(('192.168.1.38', 65431))
        print(f"Client {client.getsockname()}-----[RULES]-----\nTisors WIN Paper\nPaper WIN Rock\nRock WIN Tisors\n------------------------------")
    
        nickname = input("Choose your nickname: >")
        #   send nickname to server
        client.send(nickname.encode("utf-8"))

        # recibe start
        msg = client.recv(1024).decode() 
        #print(msg)
        # envia ok
        client.send("ok".encode("utf-8"))

        print("--Now playing send [paper,rock,tisors]--")
        #   recibe start, lo recibe otra vez porque la funcion que envia start lo envia dos veces ( por la cantidad de jugadores en el tablero en este caso 2)
        print(client.recv(1024).decode("utf-8"))

        clientPlaying = True
        while clientPlaying:

            jugadas = ["paper","rock","tisors"]
            msg = input(">")
            #
            if msg in jugadas:
                client.send(msg.encode("utf-8"))
            msgreciv = client.recv(1024).decode("utf-8")
            #
            print(f"other : {msgreciv}")
            life_points += compare_play(msg,msgreciv)
            print(f"My life points : {life_points}")
            if life_points == 0:
                print("You have 0 points you lose the game.")
                client.send("disconnect".encode("utf-8"))
                client.close()
                break
            if msgreciv not in jugadas:
                client.close()
                clientPlaying = False
        print("---Game Closed---")
            #
    except InterruptedError:
        print("interrupted")
    except KeyboardInterrupt:
        print("keyboard interrupted")
    except Exception as e:
        print(f"::{e}")