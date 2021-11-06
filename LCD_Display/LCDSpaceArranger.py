#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

import json

class SpaceArranger:
    def __init__(self):
        with open("LCDSettings.json","r")as readfile:
            self.Settings = json.load(readfile)
            readfile.close()

    async def formattingText(self,text):

        line = await self.replaceANSIwithASCI(str(text))
        if len(line) > self.Settings["LCD_WIDTH"]:
            line = await self.fillingWithSpacers(line)

        return line
        
    async def fillingWithSpacers(self,replacedline):
        for i in range(0,self.Settings["LCD_WIDTH"]):
            replacedline = replacedline+" "
        return replacedline

    async def replaceANSIwithASCI(self,text):
        
        li = []
        for i in range(0,len(text)):
            if text[i] == "ä":
                li.append("ae")
                pass

            elif text[i] == "ö":
                li.append("oe")
                pass

            elif text[i] == "ü":
                li.append("ue")
                pass

            elif text[i] == "Ä":
                li.append("Ae")
                pass

            elif text[i] == "Ö":
                li.append("Oe")
                pass

            elif text[i] == "Ü":
                li.append("Ue")
                pass

            elif text[i] == "ß":
                li.append("sz")
                pass

            else:
                li.append(text[i])

        return ''.join(li)




        




   
        
    
    
    



