

class BasicInfoObject():
    def __init__(self,url,name,city):
        self.url = url
        self.name = name
        self.city = city

    def getUrl(self):
        return self.url
    def getName(self):
        return self.name
    def getCity(self):
        return self.city
    #
    def setUrl(self,c):
        self.url = c
    def setName(self,c):
        self.name = c
    def setCity(self,c):
        self.city = c

        
class EspecificInfo():
    def __init__(self,url,epoca,local):
        self.url = url
        self.epoca = epoca
        self.local = local

    def getUrl(self):
        return self.url
    def getEpoca(self):
        return self.epoca
    def getLocal(self):
        return self.local
    #
    def setUrl(self,c):
        self.url = c
    def setEpoca(self,c):
        self.epoca = c
    def setLocal(self,c):
        self.local = c