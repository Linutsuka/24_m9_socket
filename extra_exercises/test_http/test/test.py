from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
from datetime import datetime as dati
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        forever = True
        while forever:
            self.send_header('Content-type', 'text/HTML; charset=utf-8')
            self.end_headers()

            self.wfile.write("<h1>Hey</h1>".encode())
            self.wfile.write(f"<h3>{dati.now()}</h3>".encode())
            sleep(1)


info = ('127.0.0.1',8000)
httpd = HTTPServer(info,HttpHandler)
try:
    httpd.serve_forever()
except:
    print("error")
