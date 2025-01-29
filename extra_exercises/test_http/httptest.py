import http.server
import socketserver

try:
   
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    print("connected")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
except KeyboardInterrupt:
    print("keyboard interrupted server")