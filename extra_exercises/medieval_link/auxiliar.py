import urllib.request
from BasicInfo import BasicInfoObject


building = "castell"

url_domn = 'https://www.catalunyamedieval.es/edificacions-de-caracter-militar/castells/'
url_start = 'https://www.catalunyamedieval.es/'
#   <a href="https://www.catalunyamedieval.es/castell-de-ponts-noguera/">469. Castell de Ponts / Noguera</a>
start = f'<li class="{building}"><a href="https://www.catalunyamedieval.es'
final = '</a></li>'

#   Secure html exists, !! NO-USE
def secure_url(url):
    response = ''
    try:
        response = urllib.request.urlopen(url)
      
    except urllib.error.HTTPError as e:
        return response.reason
    
    return response.code

#   Obtain the html
def get_data(url):
    data = urllib.request.urlopen(url)
    try:
        charset = data.headers.get_content_charset()
        html = data.read().decode(charset)
    except TypeError:
        data = urllib.request.urlopen(url)
        html = data.read().decode()
    return html

#   Get info of the html
def get_info(html, start, final):

    initial_position = html.find(start)
    final_position = html.find(final,initial_position)
    html_data = (html[initial_position:final_position])

    return html_data[len(start)+1:]

def clean(string):
    auxString = ""

    for c in range(len(string)):
      
        if string[c].isalpha():
            auxString += string[c]
        else:
          
            if c > 0 and string[c-1].isalpha():
                auxString += string[c]
            # Verificar si el siguiente carácter está dentro de los límites y es una letra
            if c + 1 < len(string) and string[c+1].isalpha():
                auxString += string[c]
            if string[c] == "–":
                auxString += string[c]

    return auxString

def get_all_info(html, start, final,sturl):
    bInfo = []
    while True:
        #   buscar posició iniciañ
        initial_position = html.find(start)
        if initial_position == -1:  # sino troba més surt del bucle
            break

        # buscar la posició final
        final_position = html.find(final, initial_position)
        if final_position == -1:  #sino troba el limitador sortir
            break

        # extraure la data
        html_data = html[initial_position + len(start):final_position]
        split_data = html_data.split("/")
        if len(split_data) == 4:
            url = sturl + split_data[1]
            bInfo.append(BasicInfoObject(url,clean(split_data[2]),clean(split_data[3])))
         

        
        html = html[final_position + len(final):]

    return bInfo

#   MAIN
if __name__ == '__main__':
    try:
        html = get_data(url_domn)
    #    take info of htmldata
    #string =  get_info(html, start, final)  
        bInfo = get_all_info(html,start,final,url_start)

        with open("castell.txt","w") as f:   
            for c in bInfo:
                f.write((f"{c.getUrl()}${c.getName()}${c.getCity()}\n"))
            
        print("--finish--")
    except Exception as e:
        print(f"Ha ocurrigut un problema en el programa. Error: {e}")

    
    
