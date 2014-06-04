__author__ = 'Vyrtan'

class context():

   global name
   name = str

   global address
   address = str

   def setname(self, n):
        name = n

   def setaddress(self, a):
        address = a

   def getname(self):
        return name

   def getaddress(self):
        return address