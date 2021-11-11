#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#


import time, json
import RPi.GPIO as GPIO


class Button(object):
    def __init__(self):

        with open("../ButtonSettings.json","r")as readfile:
            self.Settings = json.load(readfile)
            readfile.close()

        self.EventLibrary={ }
        self.LastActivatedTime = { } 

    async def addEvent(self,port,function = None):
        if function == None:
            raise Exception("Incomplete Parameterliste")

        GPIO.setup(port, GPIO.IN)

        self.EventLibrary.update({port:function})

        akttime = float(time.time())
        self.LastActivatedTime.update({port:akttime})


    async def handleEvent(self, Port):
        print("Handle Event",Port)
        if float(time.time()) - self.LastActivatedTime[Port] >= self.Settings["UnbounceTime"]:
            await self.EventLibrary[Port]()       
            self.LastActivatedTime[Port] = float(time.time())

    async def LookForEvent(self):
        for port in self.EventLibrary.keys():
            if GPIO.input(port):
                await self.handleEvent(port)
