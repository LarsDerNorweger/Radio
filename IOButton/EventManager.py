#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

import json
import threading
from time import sleep
import ButtonDriver




class Button:
    def __init__(self):
        self.EventLibrary={ }

        return None
    
    def mainloop(self):
        threading.Thread(target=lambda: self.eventLoop()).start()

    def addEvent(self,port,function = None):
        if function == None:
            raise Exception("Incomplete Parameterliste")

        self.EventLibrary.update({port:function})
        print(self.EventLibrary)

        return None

    def handleEvent(self, Port):
        print("Handle Event",Port)
        print(self.EventLibrary[Port])
        exec(self.EventLibrary[Port])
        

    def eventLoop(self):
        while(True):
             
            sleep(3)

def test():
    print("test succesfull")



b = Button()
b.addEvent(2,test)
b.handleEvent(2)
