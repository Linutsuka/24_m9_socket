import datetime
import urllib.request
import urllib.error

def show_text(t): print(f"{datetime.datetime.now()}   {t}")


slices_data = [['href="mailto:','">'],['<font face="Arial"><b>CALL US TOLL FREE','!!!</b>'],['<font face="Arial, Helvetica, sans-serif" size="2" color="#363D54">\n<br>',
                    '<br>(855)457-4469 (Toll Free Number)</font>']]

    
def scrapper(data,start,final):
    start_position = data.find(start)
    final_position = data.find(final,start_position)
    if final_position == -1 or start_position ==- 1:
        return "no trobat"
    else: return data[start_position+len(start):final_position]

def get_data():
    url = 'http://www.deeprock.com/'
    try:
        data = urllib.request.urlopen(url)
        charset = data.headers.get_content_charset("utf-8")
        html = data.read().decode(charset)
        return html
    except TypeError:
        data = urllib.request.urlopen(url)
        charset = data.headers.get_content_charset()
        html = data.read().decode(charset)
        return html

def info_html(data):
    html = "<div>"
    html += "<h1>Info</h1>"
    for n in range(len(data)):
        html += "<a>"+data[n]+"</a>"
    html += "</div>"
    return html
def write_page(data):
    try:
        with open('index.html','w') as f:
            f.write(str(data))
        f.close()
        return 0
    except Exception as e:
        print(e)
        return 1

try:
    print("Scrapper 'deeprock.com' page! Information to scrapp:")
    print(f"Number, mail, city")
    data = get_data()
    info = []
    #print(data)
    for a in range(len(slices_data)):
            info.append(scrapper(data,slices_data[a][0], slices_data[a][1]))
            print(info)
    info = (info_html(info))
    print(write_page(info))
except Exception as e:
    show_text(f"Error occurs. {e}")