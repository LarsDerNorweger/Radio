import asyncio
import logging

import RPi.GPIO as GPIO
import time
import RadioFunktions
from LCD_Display.LCDSpaceArranger import *
from LCD_Display.LCDDisplayManager import DisplayManager
from IOButton.EventManager import Button
from Internal.InternalOperation import InternalOperation


prevTime = 0
dispMan: DisplayManager
rf: RadioFunktions.Radiofunctions
Buttons: Button


async def setup():
    InternalOperation.configLogging("./Radio.log")
    try:
        InternalOperation.dumpPID()
        InternalOperation.shortenLog(200, "./Restart.log")
        dispMan = DisplayManager()
        Buttons = Button()
        rf = RadioFunktions.Radiofunctions()
    except Exception as e:
        logging.error("Setup failed", exc_info=True)

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
    try:
        await Buttons.LookForEvent()
        await dispMan.UpdateDisplay()
    except Exception as e:
        logging.error("occured in mainLoop", exc_info=True)


# Radio Functions

async def Refresh():
    return rf.getCurrentTitle()


async def Power():
    rf.ChangePowerState()
    await dispMan.toggleDisplay()
    await dispMan.addContentToDisplay(" ", 1)
    logging.debug("Toggle Radio State")


async def VolumePlus():
    await dispMan.addContentToDisplay(rf.Volume("+5"), 2)
    logging.info("add volume")


async def VolumeMinus():
    await dispMan.addContentToDisplay(rf.Volume("-5"), 2)
    logging.info("reduce Volume")


async def ChangePlayList():
    nPl = rf.ChangePlaylist()
    await dispMan.addContentToDisplay(nPl, 2)
    logging.debug(f"Change Playlist to {nPl}")


async def ChangeSource():
    src = rf.Changesource()
    await dispMan.addContentToDisplay(src, 2)
    logging.debug(f"Change Playlist to {src}")


async def NextTitle():
    rf.changeTitle("up")


async def PrevTitle():
    rf.changeTitle("down")


if __name__ == "__main__":
    asyncio.run(setup())
    while (True):
        asyncio.run(loop())
        time.sleep(0.1)
