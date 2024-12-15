import urllib.request

#   Obre el url
url = 'https://www.eltiempo.es/palamos.html'
data = urllib.request.urlopen(url)
#   Obtenir code html de la web
charset = data.headers.get_content_charset()
html = data.read().decode(charset)
#   Mostrar una part del html, escrapejar
initial_position = html.find('dataLayer = [{')
final_position = html.find(';',initial_position)
print(html[initial_position:final_position])