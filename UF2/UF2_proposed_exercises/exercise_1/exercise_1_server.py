import http.server
import socketserver

ip = '192.168.3.179'
#    Server information
adresses = (ip,65532)
handler = http.server.SimpleHTTPRequestHandler
httpp = socketserver.TCPServer(adresses,handler)

#   Open server
try:
    #   Catch default .html >> index.html
    print("server running!")
    httpp.serve_forever()
    
except KeyboardInterrupt:
    httpp.server_close()
    print("server closed")
