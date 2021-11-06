#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

import json
#import RPi.GPIO as GPIO

class ButtonDriver:
    def __init__(self):
        with open("LCDSettings.json","r")as readfile:
            self.Settings = json.load(readfile)
            readfile.close()