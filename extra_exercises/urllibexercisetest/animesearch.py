import urllib.request
import urllib.error


url = "https://anilist.co/anime/175422/Baban-Baban-Ban-Vampire"
def get_data(url):
   
    try:
        data = urllib.request.urlopen(url)
        charset = data.headers.get_content_charset()
        html = data.read().decode(charset)
        return html
    except urllib.error.HTTPError as e:
        return f"{e.code} {e.reason}"
    except:
        html = data.read().decode()
        return html

def get_info(html,start,final):
    start_position = html.find(start)
    final_position = html.find(final,start_position)
    return html[len(start)+start_position:final_position]

html = get_data(url)
print(get_info(html,'<p data-v-5776f768="" class="description">',"<br>"))
