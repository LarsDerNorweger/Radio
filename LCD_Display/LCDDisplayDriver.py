#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

import json
import RPi.GPIO as GPIO
import time

class DisplayDriver:
    def __init__(self):
        with open("../LCDSettings.json","r")as readfile:
            self.Settings = json.load(readfile)
            readfile.close()
        
        self.DisplayState = self.gen_States()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Settings["LCD_BACKLIGHT"],GPIO.OUT)

        GPIO.setwarnings(False)
        GPIO.setup(self.Settings["LCD_E"], GPIO.OUT)
        GPIO.setup(self.Settings["LCD_RS"], GPIO.OUT)
        GPIO.setup(self.Settings["LCD_DATA4"], GPIO.OUT)
        GPIO.setup(self.Settings["LCD_DATA5"], GPIO.OUT)
        GPIO.setup(self.Settings["LCD_DATA6"], GPIO.OUT)
        GPIO.setup(self.Settings["LCD_DATA7"], GPIO.OUT)
        self.lcd_send_byte(0x33, GPIO.LOW)
        self.lcd_send_byte(0x32, GPIO.LOW)
        self.lcd_send_byte(0x28, GPIO.LOW)
        self.lcd_send_byte(0x0C, GPIO.LOW)  
        self.lcd_send_byte(0x06, GPIO.LOW)
        self.lcd_send_byte(0x01, GPIO.LOW) 
        
    def lcd_send_byte(self,bits, mode):

        def resetPins():
            GPIO.output(self.Settings["LCD_DATA4"], GPIO.LOW)
            GPIO.output(self.Settings["LCD_DATA5"], GPIO.LOW)
            GPIO.output(self.Settings["LCD_DATA6"], GPIO.LOW)
            GPIO.output(self.Settings["LCD_DATA7"], GPIO.LOW)
    
        def sendEndBytes():
            time.sleep(self.Settings["E_DELAY"])
            GPIO.output(self.Settings["LCD_E"], GPIO.HIGH)  
            time.sleep(self.Settings["E_PULSE"])
            GPIO.output(self.Settings["LCD_E"], GPIO.LOW)  
            time.sleep(self.Settings["E_DELAY"])      

        GPIO.output(self.Settings["LCD_RS"], mode)

        resetPins()

        if bits & 0x10 == 0x10:
        	GPIO.output(self.Settings["LCD_DATA4"], GPIO.HIGH)
        if bits & 0x20 == 0x20: 
    	    GPIO.output(self.Settings["LCD_DATA5"], GPIO.HIGH)
        if bits & 0x40 == 0x40:
            GPIO.output(self.Settings["LCD_DATA6"], GPIO.HIGH)
        if bits & 0x80 == 0x80:
            GPIO.output(self.Settings["LCD_DATA7"], GPIO.HIGH)

        sendEndBytes()
        resetPins()

        if bits&0x01==0x01:
            GPIO.output(self.Settings["LCD_DATA4"], GPIO.HIGH)
        if bits&0x02==0x02:
            GPIO.output(self.Settings["LCD_DATA5"], GPIO.HIGH)
        if bits&0x04==0x04:
            GPIO.output(self.Settings["LCD_DATA6"], GPIO.HIGH)
        if bits&0x08==0x08:
            GPIO.output(self.Settings["LCD_DATA7"], GPIO.HIGH)

        sendEndBytes()
    

    def lcd_message(self,message):
        message = message.ljust(self.Settings["LCD_WIDTH"]," ")  
        for i in range(self.Settings["LCD_WIDTH"]):
            self.lcd_send_byte(ord(message[i]),GPIO.HIGH)
	
    async def writeOnDisplay(self,text,line):
        if line == 0:
            self.lcd_send_byte(self.Settings["LCD_LINE_1"], GPIO.LOW)
        elif line == 1:
            self.lcd_send_byte(self.Settings["LCD_LINE_2"], GPIO.LOW)

        else:
            self.lcd_send_byte(self.Settings["LCD_LINE_1"], GPIO.LOW)
            self.lcd_message("ERROR")
            raise Exception("Line out of Range",line)
	
        self.lcd_message(text)

    def ToggleDisplay(self):
        GPIO.output(self.Settings["LCD_BACKLIGHT"] ,self.DisplayState.__next__()) 

    def gen_States(self):
        while True:
            yield GPIO.HIGH
            yield GPIO.LOW
