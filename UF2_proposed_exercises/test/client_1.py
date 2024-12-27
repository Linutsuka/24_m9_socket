import socket
import threading


ip = "127.0.0.1"
port = 65530

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip,port))
print("connected")


message = "UY EL JAUME EL JOHN SNOW AY DIOMIO QUE GUAPO y puteros"
client.send(message.encode("utf-8"))
#
message = client.recv(1024).decode()
print(message)
client.close()
