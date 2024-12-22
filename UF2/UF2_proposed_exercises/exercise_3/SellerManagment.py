
class Product:
    def __init__(self,name,price,status,seller):
        self.name = name
        self.price = price
        self.status = status
        self.buyer = 'None'
        self.seller = ''
    #   GETTERS
    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def getStatus(self):
        return self.status
    def getBuyer(self):
        return self.buyer
    def getSeller(self):
        return self.seller
    #   SETTERS
    def setPrice(self,newPrice):
        self.price = newPrice
    def setStatus(self,newStatus):
        self.status = newStatus
    def setBuyer(self,newBuyer):
        self.buyer = newBuyer
        
   
