import asyncio
import os

import RPi.GPIO as GPIO
import time
import RadioFunktions
from LCD_Display.LCDSpaceArranger import *
from LCD_Display.LCDDisplayManager import DisplayManager
from IOButton.EventManager import Button
from Internal.InternalOperation import InternalOperation


dispMan = DisplayManager()
Buttons = Button()

rf = RadioFunktions.Radiofunctions()

prevTime = 0


async def setup():

    InternalOperation.dumpPID()
    InternalOperation.shortenLog(50, "./Restart.log")

    await Buttons.addEvent(19, Power)
    await Buttons.addEvent(13, VolumePlus)
    await Buttons.addEvent(6, VolumeMinus)
    await Buttons.addEvent(9, ChangePlayList)
    await Buttons.addEvent(26, ChangeSource)
    await Buttons.addEvent(5, PrevTitle)
    await Buttons.addEvent(11, NextTitle)

    # noch nicht Implementiert

    await dispMan.addContentWithShedule(Refresh, 1, 1)
    print("Startup succesfull")


async def loop():
    await Buttons.LookForEvent()
    await dispMan.UpdateDisplay()


# Radio Functions

async def Refresh():
    return rf.getCurrentTitle()


async def Power():
    rf.ChangePowerState()
    await dispMan.toggleDisplay()
    await dispMan.addContentToDisplay(" ", 1)
    print("Power Triggerd")


async def VolumePlus():
    await dispMan.addContentToDisplay(rf.Volume("+5"), 2)


async def VolumeMinus():
    await dispMan.addContentToDisplay(rf.Volume("-5"), 2)


async def ChangePlayList():
    await dispMan.addContentToDisplay(rf.ChangePlaylist(), 2)


async def ChangeSource():
    await dispMan.addContentToDisplay(rf.Changesource(), 2)


async def NextTitle():
    rf.changeTitle("up")


async def PrevTitle():
    rf.changeTitle("down")


if __name__ == "__main__":
    asyncio.run(setup())
    while (True):
        asyncio.run(loop())
        time.sleep(0.1)
