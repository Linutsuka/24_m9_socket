import datetime
import socket
import sys
def show_test(t):
    print(f"{datetime.datetime.now()} {t}")

def main():
    #   Agafa els valors ip i port on es vol connectar
    ip,port = sys.argv[1], int(sys.argv[2])
    client_name = sys.argv[3]
    show_test(f"{client_name} starts")
    #   Es fa la connexió, ipv4  i tcp
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #   Es connecta
    client.connect((ip,port))
    #   Mostra dades
    show_test(f"{client_name} {client.getsockname()[0]}:{client.getsockname()[1]}")
    show_test(f"{client_name} connected to server at {ip} : {port}")
    print("RULES: HEAD AND TAILS\n\tSend random message to participate.\tIf you get 'HEAD' you can keep playing.\n\tElse you lost the game.\n\tThe winner is who get more heads cconsecutively.\n\tGood luck!\n\n\tIf you want disconnect the server write 'DISCONNECT'.")
    connected = True
    #   Mentre estigui connectat 
    while connected:
        msg = input('> ')
       
        if msg == "DISCONNECT":
            client.send(msg.encode("utf-8").upper())
            connected = False
        else:
            #   Si el missatge es random, i no es DISCONNECT, canvia el nom per el del usuari. Envia el nom del usuari al servidor.
            msg = client_name
            client.send(msg.encode("utf-8").upper())
            msg = client.recv(1024).decode("UTF-8")
            
            show_test(f"SERVER:{msg}")
            if msg[0:4] ==  "HEAD":

                show_test("CONNECTED: You keep playing!")
            if msg[0:5] == 'TAILS':
                show_test("DISCONNECT: You lost the game.")
                connected = False
           
                
if __name__ == '__main__':
    main()

