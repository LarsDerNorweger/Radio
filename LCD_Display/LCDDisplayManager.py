#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

import json
from os import SEEK_CUR
from time import time
import RPi.GPIO as GPIO
from LCD_Display.LCDSpaceArranger import SpaceArranger
from LCD_Display.LCDDisplayDriver import DisplayDriver

class DisplayManager:
    def __init__(self):
        with open("../LCDSettings.json","r")as readfile:
            self.Settings = json.load(readfile)
            readfile.close()
        
        self.spaceArranger = SpaceArranger()
        self.Displaydriver = DisplayDriver()

        self.lastUpdateTime = 0
        self.lineContent = []
        self.shownContent = []
        self.Updated = []
        self.Shedule = {}

        for i in range(0, self.Settings["LCD_LINES"]):
            self.lineContent.append('')
            self.shownContent.append('')
            self.Updated.append(True)
    
    async def toggleDisplay(self):
        self.Displaydriver.ToggleDisplay()

    async def addShedule(self,textfunktion,lineNumber, refreshtime):
        self.Shedule.update({lineNumber:[textfunktion,refreshtime,0]})

    async def LookForShedule(self):
        if len(self.Shedule.keys()) != 0:
            for line in self.Shedule.keys():
                cache = self.Shedule[line]
                if float(time())-cache[2] >= cache[1]:
                    await self.addContentToDisplay(await cache[0](),line)
                    self.Shedule[line][2] = float(time())

    async def addContentToDisplay(self,text,lineNumber):
        if lineNumber > self.Settings["LCD_LINES"] or lineNumber == None:
            raise Exception("No defiend Displayline")

        if text != self.lineContent[lineNumber-1]:
            self.lineContent[lineNumber-1] = str(text)
            text = await self.spaceArranger.formattingText(text)
            self.shownContent[lineNumber-1]=str(text)
            self.Updated[lineNumber-1]=True

    async def UpdateDisplay(self):
        await self.LookForShedule()

        if int(time())-self.lastUpdateTime >= self.Settings["LCD_UPDATE_INTERVALL"]:
            for i in range(0,len(self.lineContent)):
                if self.shownContent[i] != self.lineContent[i] or self.Updated[i]:

                    self.Updated[i] = False

                    self.shownContent[i]= await self.shifting(self.shownContent[i])
                    await self.Displaydriver.writeOnDisplay(self.shownContent[i],i)
                    
            self.lastUpdateTime = int(time())
        
    async def shifting(self,text):
        if len(text)>self.Settings["LCD_WIDTH"]:
            text = text[len(text)-1] + text[0:len(text)-1]
        return text


    