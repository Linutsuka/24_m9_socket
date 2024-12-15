import http.server
import socketserver


#    Server information
adresses = ('192.168.1.38',65532)
handler = http.server.SimpleHTTPRequestHandler
httpp = socketserver.TCPServer(adresses,handler)

#   Open server
try:
    #   Catch default .html >> index.html
    print("server running!")
    httpp.serve_forever()
    
except KeyboardInterrupt:
    print("Interrupted")
    httpp.server_close()
    print("server closed")
