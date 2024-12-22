import datetime as dati
import time
import threading as th
import  urllib.request

#   urllib. per obrir enllaços web i agafar data
#   http.server crea un servidor web

#   what to do?  get temperature, humidity, wind speed, sunrise time and sunset time, display information, update every minute

#   https://www.eltiempo.es/san-feliu-de-guixols.html   << windspeed,temperature
#   https://www.sunrise-and-sunset.com/es/sun/espana/sant-feliu-de-guixols  <<sunrise, sunset
#   https://www.tutiempo.net/sant-feliu-de-guixols.html << humity

#   Get  data of the url
def get_data(url):
    data = urllib.request.urlopen(url)
    try:
        charset = data.headers.get_content_charset()    # Obtain url-charset of the content, to secure decode
        html = data.read().decode(charset)
    except TypeError:   #   If occurs any problem obtaining the charset decode without secure mode
        data = urllib.request.urlopen(url)
        html = data.read().decode() 
    #print(f"{th.current_thread().name} ... url open>> {url}")
    return html
#   Take the numbers of a string
def get_numbers(data):
    numbers = ''
    for item in data:
        if item.isnumeric():
            numbers += item
    return numbers
#   Take the information of the html passed, to the start point to final point
def get_info(html,start, final):
    
    initial_position = html.find(start)
    final_position = html.find(final,initial_position)

    html_data = (html[initial_position:final_position])

    return get_numbers(html_data)

#   Concat ':' to string
def set_timer(number):
    return number[0:2] + ":" + number[2:4]

name = ["Sant Feliu de Guixols","Begur","Pals","Palamos","Calonge"]
categories = ['Temperature','WindSpeed','Humidity','Sunrise','Sunset']
slices = [['currentTemperature',"ºC',"],["windSpeed':",'km/h'],['<th>Amanecer de hoy</th>','</td>'],['<th>Atardecer de hoy</th>','</td'],['Humedad relativa:</td>','%</td>']]
#   First array: Temperature, windspeed
#   Second array: Humidity
#   Three array: Sunrise, sunset
url = [
                ['https://www.eltiempo.es/san-feliu-de-guixols.html','https://www.eltiempo.es/begur.html','https://www.eltiempo.es/pals.html','https://www.eltiempo.es/palamos.html','https://www.eltiempo.es/calonge.html'],
                ['https://www.tutiempo.net/sant-feliu-de-guixols.html','https://www.tutiempo.net/begur.html','https://www.tutiempo.net/pals.html','https://www.tutiempo.net/palamos.html','https://www.tutiempo.net/calonge.html'],
                ['https://www.sunrise-and-sunset.com/es/sun/espana/sant-feliu-de-guixols','https://www.sunrise-and-sunset.com/es/sun/espana/begur','https://www.sunrise-and-sunset.com/es/sun/espana/pals','https://www.sunrise-and-sunset.com/es/sun/espana/palamos','https://www.sunrise-and-sunset.com/es/sun/espana/calonge'],
                
                    ]

#   
def update_array(name,url,slices):
    array_info = []
    for a in range(len(name)):
        #print(name[a])
        array_info.append([])
        #Temperature and windpseed
        for b in range(len(url)):
        #print(f"\t{url[b][a]}")
            if b == 0:

                html = get_data(url[b][a])
                #Temperature and Windspeed
                temperature = get_info(html,slices[0][0],slices[0][1])
                windspeed = get_info(html,slices[1][0],slices[1][1])
                #print(f"\t Temperature: {temperature}\n\t WindSpeed: {windspeed}")
                #   Put info into array
                array_info[a].append(temperature)
                array_info[a].append(windspeed)

            if b == 2:
            
                html = get_data(url[b][a])
                sunrise = get_info(html,slices[2][0],slices[2][1])
                sunset = get_info(html,slices[3][0],slices[3][1])
                #print(f"\t Sunrise: {set_timer(sunrise)}\n\t Sunset: {set_timer(sunset)}")
                #   Put info into array
                array_info[a].append(set_timer(sunrise))
                array_info[a].append(set_timer(sunset))

            if b == 1:
                
                html = get_data(url[b][a])
                humidity = get_info(html,slices[4][0],slices[4][1])
                #print(f"\t Humidity: {humidity}")
                #   Put info into array
                array_info[a].append(humidity)
    return array_info
#   Creating html data format
def info_to_html(name,categories,info):
    
    html = "<div>"

    for a in range(len(name)):
        html += "   <h1 style="'color:blue'">"+name[a]+"</h1>"
        #print(name[a])
        for b in range(len(info)):    
            html += "   <a><b>"+categories[b]+":</b>"+info[a][b]+"<a><br>"  
            #print(f"\t{info[a][b]}")
    html += "<a>                "+str(dati.datetime.now())+"</a></br>"
    html += "</div>"
    return html

#   Write html index.html 
def write_html(html):

    with open("index.html","w") as f:
        f.write(html)


#   --- TEST THREADS ---

#   
def update_array_thread(name,data,slices):
    array_info = []
    for a in range(len(name)):
        #print(name[a])
        array_info.append([])
        #Temperature and windpseed
        for b in range(len(data)):
        #print(f"\t{url[b][a]}")
            if b == 0:

                html = data[b][a]
                #Temperature and Windspeed
                temperature = get_info(html,slices[0][0],slices[0][1])
                windspeed = get_info(html,slices[1][0],slices[1][1])
                #print(f"\t Temperature: {temperature}\n\t WindSpeed: {windspeed}")
                #   Put info into array
                array_info[a].append(temperature)
                array_info[a].append(windspeed)
            if b == 1:
                
                html = data[b][a]
                humidity = get_info(html,slices[4][0],slices[4][1])
                #print(f"\t Humidity: {humidity}")
                #   Put info into array
                array_info[a].append(humidity)
            
            if b == 2:
            
                html = data[b][a]
                sunrise = get_info(html,slices[2][0],slices[2][1])
                sunset = get_info(html,slices[3][0],slices[3][1])
                #print(f"\t Sunrise: {set_timer(sunrise)}\n\t Sunset: {set_timer(sunset)}")
                #   Put info into array
                array_info[a].append(set_timer(sunrise))
                array_info[a].append(set_timer(sunset))
    return array_info


#   Append list with data  
def get_data_rewrite(info_test,url,b,a):
    info_test[b][a] = get_data(url) #   Put the html info into list 
   
#   URL OPEN and read, URL information into arrays
def thread_url(name,url,slices):
    info_test= [['_'] * len(name) for _ in range(len(url))]
   
    for a in range(len(name)):
        for b in range(len(url)):
            t = th.Thread(target=get_data_rewrite, args=(info_test,url[b][a],b,a))
            t.start()
        
    return info_test

#   Amb la funció thread_url carrega els urls i posa la data dintre de una array.
#   Després posa aquesta informació en un string, i la pasa a la funció update_array_thread, aquesta funció fa els slices corresponents i ho posa en una llista.
#   return: list
def get_data_url(name,url,slices):
    print(f"start url--{dati.datetime.now()}")
    html = thread_url(name,url,slices)
    print(f"final url--{dati.datetime.now()}")
    time.sleep(5)   #   Wait 5 seconds to secure data
    
    array = update_array_thread(name,html,slices)
    return array


#   Main program
try:
  
    while KeyboardInterrupt:
        print("tracking...")
        #print(f"start ... {dati.datetime.now()}")
        info = get_data_url(name,url,slices)
        html = info_to_html(name,categories,info)
        write_html(html)
        #print(f"finish ... {dati.datetime.now()}")
        time.sleep(55)
        print(f"last update:  {dati.datetime.now()}")
       
except KeyboardInterrupt:
    print("script stopped")
except:
    print(f"Ocurrs error")