#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

import json
import os
import subprocess
import RPi.GPIO as GPIO


class NativeRadioMethods():
    def gen_Changer(self):
        while True:
            yield "Radio"
            yield "Intern"

    def gen_Playlist(self, Playlist) -> str:
        while True:
            for item in Playlist:
                yield item


class NativeMPCMethods():

    def __init__(self):
        self.getCommand = {
            "Radio":
            {
                "start": "mpc play",
                "stop": "mpc stop"
            },
            "Intern": {
                "start": "mpc play",
                "stop": "mpc pause"
            }
        }
        self.Playstate = self.gen_Playstate()

    def gen_Playstate(self):
        while True:
            yield "start"
            yield "stop"

    def clearPlayList(self, Source):
        self.ToggleMusik(Source)
        os.system("mpc clear")
        return None

    def ToggleMusik(self, Source):
        command = self.getCommand[Source][self.Playstate.__next__()]
        os.system(command)
        print(command)


class Radiofunctions(NativeMPCMethods, NativeRadioMethods):
    def __init__(self):
        GPIO.setup(20, GPIO.OUT)
        self.Powerstate = False
        self.npm = NativeMPCMethods()
        with open("../RadioSettings.json", "r")as readfile:
            self.Settings = json.load(readfile)
            readfile.close()

        self.getSource = self.gen_Changer()
        self.Source = self.getSource.__next__()
        self.Playlist = self.gen_Playlist(self.Settings[self.Source].keys())

    def ChangePlaylist(self) -> str:
        self.npm.clearPlayList(self.Source)
        Playlist = self.Playlist.__next__()
        command = "mpc load " + self.Settings[self.Source][Playlist]
        print(command)
        os.system(command)
        self.npm.ToggleMusik(self.Source)
        return Playlist

    def Volume(self, ratio):
        command = "mpc volume " + str(ratio)
        print(command)
        os.system(command)
        return f"Volume  {ratio}"

    def Changesource(self):
        self.Source = self.getSource.__next__()
        self.Playlist = self.gen_Playlist(self.Settings[self.Source].keys())
        return self.Source

# noch nicht an Event gebunden

    def changeTitle(self, direction) -> str:
        if self.Source == "Intern":
            if direction == "up":
                os.system("mpc next")
                return "Next Title"
            if direction == "down":
                os.system("mpc prev")
                return "Previous Title"

    def getCurrentTitle(self):
        befehl = "mpc current"
        process = subprocess.Popen(befehl, shell=True, stdout=subprocess.PIPE)
        text = str(process.stdout.read())
        text = text[2:len(text)-3]
        print(text)
        return text

    def ChangePowerState(self):
        self.Powerstate = not(self.Powerstate)
        self.npm.ToggleMusik(self.Source)
        if self.Powerstate:
            GPIO.output(20, GPIO.HIGH)
            return
        GPIO.output(20, GPIO.LOW)
