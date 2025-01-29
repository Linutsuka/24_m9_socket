import urllib.request
from BasicInfo import EspecificInfo
from multiprocessing import Pool




url = 'https://www.catalunyamedieval.es/can-clara-sant-pere-pescador-alt-emporda/'
url = 'https://www.catalunyamedieval.es/castell-dels-montcada-vic-osona/'



# get data of html
def get_data(url):
    data = urllib.request.urlopen(url)
    try:
        charset = data.headers.get_content_charset()
        html = data.read().decode(charset)
    except:
        data = urllib.request.urlopen(url)
        html = data.read().decode()
        return html
    return html
#   get information of html
def get_info(html,start,final):
    start_pos = html.find(start)
    final_pos = html.find(final, start_pos)

    html = html[start_pos:final_pos]
    html = html[(len(start)):]
    return html

#   get epoca 
def get_info_epoca(html,start,final):
    info = get_info(html,start,final)
    if info[:8] == "Medieval":
        return "Medieval"
    elif info[:5] == "Segle":
        blank = 0
        word = ''
        for c in range(len(info[0:15])):
            if blank < 2:
                if info[c] == ' ':
                    blank += 1
                if info[c].isalpha():
                    word += info[c]
        return word

    else:
        return "NotFound"
    
    

def get_data_info(url):

    indexes = [['Època</strong>: ','</p>'],
           ['rel="noopener noreferrer">N','</a>']]
    url_index = len("https://www.catalunyamedieval.es/")

    html = get_data(url)
   
    epoca = get_info_epoca(html,indexes[0][0],indexes[0][1])
    local = get_info(html,indexes[1][0],indexes[1][1])
    


    return local


# Main
if __name__ == '__main__':
    lines = []
    with open('castell.txt', 'r') as f:
        for line in f:
            newLine = line.split("$")
            lines.append(newLine[0])  # Limpia cada línea y agrégala a la lista
    f.close()
    
    print("start")
    # Usar Pool para procesar las líneas
    with Pool() as pool:
        results = pool.map(get_data_info, lines)  # Mapea cada línea a la función

    # Imprimir los resultados
    for r in results:
        if r == "":
            print("NotFound")
        else:
            print(f"{r}")
    print("finish")
        