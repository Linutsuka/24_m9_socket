import threading as th
import urllib.request
class HttpRequestThread(th.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
    def run(self):
        print(f"{self.name} checking {self.url} ... ")
        try:
            response = urllib.request.urlopen(self.url)
            print(f"{self.name} {response.code} ")
        except urllib.error.HTTPError as e:
            print(f"{self.name} {e.code} ")
        except urllib.error.URLError as e:
            print(f"{self.name} {e.reason} ")
urls = [
"https://google.es/ ",
"https://httpstat.us/200 ",
"https://httpstat.us/400 ",
"https://doesnotexistandwillneverexist.com "
]
threads = [HttpRequestThread(url) for url in urls]
[t.start() for t in threads]
[t.join() for t in threads]