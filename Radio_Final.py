import time
import RPi.GPIO as GPIO
from threading import Thread
from time import sleep
import subprocess
from os import system

Audio = 20
Backlight = 21

LOW = GPIO.LOW
HIGH = GPIO.HIGH

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Buttonlist = [26,19,13,6,5,0,11,9]
for i in range(0,len(Buttonlist)):
    GPIO.setup(Buttonlist[i],GPIO.IN)

print("run")

GPIO.setup(Audio,GPIO.OUT)
GPIO.setup(Backlight,GPIO.OUT)

# Zuordnung der GPIO Pins (ggf. anpassen)
LCD_RS = 4
LCD_E  = 17
LCD_DATA4 = 18
LCD_DATA5 = 23
LCD_DATA6 = 22
LCD_DATA7 = 24

LCD_WIDTH = 16 		# Zeichen je Zeile
LCD_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
LCD_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005

class display:
	def __init__(self):
		self.line1 = ""
		self.line2 = ""
		self.x1 = []

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(LCD_E, GPIO.OUT)
		GPIO.setup(LCD_RS, GPIO.OUT)
		GPIO.setup(LCD_DATA4, GPIO.OUT)
		GPIO.setup(LCD_DATA5, GPIO.OUT)
		GPIO.setup(LCD_DATA6, GPIO.OUT)
		GPIO.setup(LCD_DATA7, GPIO.OUT)
		self.lcd_send_byte(0x33, GPIO.LOW)
		self.lcd_send_byte(0x32, GPIO.LOW)
		self.lcd_send_byte(0x28, GPIO.LOW)
		self.lcd_send_byte(0x0C, GPIO.LOW)  
		self.lcd_send_byte(0x06, GPIO.LOW)
		self.lcd_send_byte(0x01, GPIO.LOW) 

	def lcd_send_byte(self,bits, mode):
		GPIO.output(LCD_RS, mode)
		GPIO.output(LCD_DATA4, GPIO.LOW)
		GPIO.output(LCD_DATA5, GPIO.LOW)
		GPIO.output(LCD_DATA6, GPIO.LOW)
		GPIO.output(LCD_DATA7, GPIO.LOW)
		if bits & 0x10 == 0x10:
			GPIO.output(LCD_DATA4, GPIO.HIGH)
		if bits & 0x20 == 0x20:
			GPIO.output(LCD_DATA5, GPIO.HIGH)
		if bits & 0x40 == 0x40:
			GPIO.output(LCD_DATA6, GPIO.HIGH)
		if bits & 0x80 == 0x80:
			GPIO.output(LCD_DATA7, GPIO.HIGH)
		time.sleep(E_DELAY)
		GPIO.output(LCD_E, GPIO.HIGH)  
		time.sleep(E_PULSE)
		GPIO.output(LCD_E, GPIO.LOW)  
		time.sleep(E_DELAY)
		GPIO.output(LCD_DATA4, GPIO.LOW)
		GPIO.output(LCD_DATA5, GPIO.LOW)
		GPIO.output(LCD_DATA6, GPIO.LOW)
		GPIO.output(LCD_DATA7, GPIO.LOW)
		if bits&0x01==0x01:
			GPIO.output(LCD_DATA4, GPIO.HIGH)
		if bits&0x02==0x02:
			GPIO.output(LCD_DATA5, GPIO.HIGH)
		if bits&0x04==0x04:
			GPIO.output(LCD_DATA6, GPIO.HIGH)
		if bits&0x08==0x08:
			GPIO.output(LCD_DATA7, GPIO.HIGH)
		time.sleep(E_DELAY)
		GPIO.output(LCD_E, GPIO.HIGH)  
		time.sleep(E_PULSE)
		GPIO.output(LCD_E, GPIO.LOW)  
		time.sleep(E_DELAY)  

	def lcd_message(self,message):
		message = message.ljust(LCD_WIDTH," ")  
		for i in range(LCD_WIDTH):
			self.lcd_send_byte(ord(message[i]),LCD_CHR)
	
	def printTextToDisplay(self,line,text):
		if line == 1:
			self.lcd_send_byte(LCD_LINE_1, LCD_CMD)
		elif line == 2:
			self.lcd_send_byte(LCD_LINE_2, LCD_CMD)
		else:
			print("Diese Zeile ist nicht vergeben")
			self.lcd_send_byte(LCD_LINE_1, LCD_CMD)
			self.lcd_message("ERROR")

		self.lcd_message(text)

class prepareWriteToDisplay():
	def __init__(self,zeichen):
		self.zeichenlaenge = zeichen
		self.line1 = ""
		self.line2 = ""
		self.x1 = ["","",0,0]
		self.x2 = [" "," ",0,0]
		pass

	def filling(self,line):
		# auffüllen der Zeichen für sauberen Lauf
		if len(line) > self.zeichenlaenge:
			for i in range(0,self.zeichenlaenge):
				line = " " + line
		return line

	def replaceANSI(self,line):
		for i in range(0,len(line)):
			if line[i] == "ä":
				print("found")
				line[i] = "a"
		return line
		pass

	def preparing(self):
		sleep = 0.5
		self.x1[0] = self.filling(self.line1)
		self.x1[1] = self.filling(self.line2)

		#ausführung bei veränderung
		if self.x1[0] != self.x2[0] or self.x1[1] != self.x2[1]:
			for i in range(0,2):
				if len(self.x1[i]) > self.zeichenlaenge:
					d.printTextToDisplay(i+1,self.x1[i])
					self.x1[i+2] +=1
					pass
				else:
					d.printTextToDisplay(i+1,self.x1[i])
					pass

		else:
			#verschiebung der Darstellung um eine Stelle
			for i in range(0,2):
				if len(self.x1[i]) > self.zeichenlaenge:
					t = self.x1[i]
					d.printTextToDisplay(i+1,t[self.x1[i+2]:len(t)])
					self.x1[i+2] += 1
					if self.x1[i+2] > len(t):
						self.x1[i+2] = 0
						sleep = 2.5
				else:
					pass
			pass
		self.x2 = self.x1.copy()
		return sleep

class musik():
    def __init__(self):
        self.senderliste = ["284280-0_mp3_low","HITRTL","HITRTL-80GER","HITRTL-OLDIES","HITRTL-XMAS",0]
        self.musikliste = ["80-ger","ErzWeihnachten","Weihnachten", "Hintergrund",0]
        self.run = bool(False)
        self.Status = "Radio"
        pass

    def playNextEntry(self):
        print("weiter")
        print(self.Status)
        if self.Status == "Radio":
            listen = self.senderliste
        else:
            listen = self.musikliste

        i = listen.pop()
        self.clearPlayList()
        i += 1
        if i >= len(listen):
            i = 0
        befehl = "mpc load "+ listen[i]
        system(befehl)
          
        listen.append(i)
        pass

    def einlesen(self):
        print("einlesen")
        print(self.Status)
        if self.Status == "Radio":
            listen = self.senderliste
        else:
            listen = self.musikliste

        i = listen.pop()
        self.clearPlayList()
        befehl = "mpc load "+ listen[i]
        system(befehl)  
        listen.append(i)
        pass
    
    def toggleMusic(self):
        if self.Status == "Radio":
            if self.run == True:
                system("mpc stop")
                print("mpc stop")
                self.run = False
            elif self.run == False:
                system("mpc play")
                print("mpc play")
                self.run = True
        else:
            system("mpc toggle")
            print("mpc toggle")


    def clearPlayList(self):
        system("mpc clear")
        self.toggleMusic()
        self.run = False
        pass

    def findCurrentPlayedTitle(self):
        befehl = "mpc current"
        process = subprocess.Popen(befehl,shell = True,stdout=subprocess.PIPE)
        text = str(process.stdout.read())
        text = text[2:len(text)-3]
        return text
    pass

class Button():
    def __init__(self):
        print("Button")
        self.t1_stop = True
        Thread(target= self.Diplay_Status).start()
        self.musik = musik()
        self.value = [0,0,0,0,0,0,0,0]
        Thread(target=lambda: self.check()).start()
        Thread(target = lambda: self.auswerten()).start()
        pass

    def auswerten(self):
        
        status = False
        print("auswerten")
        while True:
            if self.value[1] == 1:
                print("go")
                status = self.Power(status)
                sleep(0.5)
            #wechsel Radio / Server
            elif self.value[0] == 1:
                if self.musik.Status == "Radio":
                    self.musik.Status = "Server"
                else:
                    self.musik.Status = "Radio"
                self.musik.einlesen()
                self.musik.toggleMusic()
                sleep(0.5)
            #Ander Liste Sender auswählen
            elif self.value[7] == 1:
                self.musik.playNextEntry()
                self.musik.toggleMusic()
            
            # nächster Titel

            elif self.value[6] == 1:
                if self.musik.Status == "Radio":
                    pass
                else:
                    system("mpc next")
                sleep (0.5)

            elif self.value[4] == 1:
                if self.musik.Status == "Radio":
                    pass
                else:
                    system("mpc prev")
                sleep (0.5)

            #Volume change

            elif self.value[2] == 1:
                system("mpc volume +5")
                prepredText.line2 = "volume +5"
                sleep (0.5)

            elif self.value[3] == 1:
                system("mpc volume -5")
                prepredText.line2 = "volume -5"
                sleep (0.5)
                

    def check(self):
        while True:
            for i in range(0,len(Buttonlist)):
                self.value[i] = GPIO.input(Buttonlist[i])
    
    def Power(self,status):
        
        if status:
            print("stop")
            GPIO.output(Backlight,LOW)
            GPIO.output(Audio,LOW)
            self.musik.toggleMusic()
            self.t1_stop = True

            
            pass
        else:
            print("start")
            GPIO.output(Backlight,HIGH)
            GPIO.output(Audio,HIGH)
            self.musik.toggleMusic()
            self.t1_stop = False
        return not(status)

    def Diplay_Status(self):
        
        global d
        d = display()
        global prepredText
        prepredText = prepareWriteToDisplay(16)
        m_time = [0,0]
        m_time_for_updatecycle = 0.5
        while True:
            if self.t1_stop:
                sleep(1)
                pass
            else:
                if m_time[0] <= time.time() - m_time_for_updatecycle:
                    m_time_for_updatecycle = prepredText.preparing()
                    prepredText.line2 = ""	
                    m_time[0] = time.time()
                if m_time[1] <= time.time() - 5:
                    prepredText.line1 = self.musik.findCurrentPlayedTitle()
                    m_time[1] = time.time()
            
                        
            
print("Button")
Button()
        

