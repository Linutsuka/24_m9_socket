import urllib.request
from sys import argv
#
from http.server import HTTPServer, BaseHTTPRequestHandler


def get_data(url):
    try:
        data = urllib.request.urlopen(url)
        charset = data.headers.get_content_charset()
        html = data.read().decode(charset)
        return html
    except:
        data = urllib.request.url(open)
        html = data.read().decode()
        return html

def get_info(html,start,final):

    start_position = html.find(start)
    final_position = html.find(final,start_position)
    return html[len(start)+start_position:final_position]

def slice_show(html,slices):
    pieces = ''
    finalwords = ["C","km/h'"]
    for a in range(len(slices)):
        pieces += f"{get_numbers(get_info(html,slices[a][0],slices[a][1]))} {finalwords[a]}\n"
    return pieces
def write_index(html):
    with open("index.html","w") as f:
        f.write(html)
def get_numbers(word):
    number = ''
    for item in word:
        if item.isnumeric(): number += item
    return number

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"{info}".encode("utf-8"))


if __name__ == "__main__":

   
    slices = [["'currentTemperature':",","],
              ["'windSpeed':",","]]
    name_city = ["palamos","begur"]
    city = ["https://www.eltiempo.es/palamos.html","https://www.eltiempo.es/begur.html"]
    try:
        info = "<div>"
        n = 0
        for a in range(len(city)):
            html_info = get_data(city[a])
            info += f"<h1 style=color:salmon >{name_city[a]}</h1>"
            info += f"<a>{slice_show(html_info,slices)}</a>"
        info += f"</div>"
        # no haria falta perque ja esta en el handler
        # handler agafa var globals
        write_index(info)
        
        print("Server open at localhost:8000")
        httpd = HTTPServer(("localhost",8000),Handler)
        httpd.serve_forever()
    
    except KeyboardInterrupt: pass
    except Exception as e:
        print(e)
