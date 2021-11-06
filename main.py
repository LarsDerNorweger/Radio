import asyncio


from etc.helper import asyncsleep
from etc.LCDSpaceArranger import *
from etc.LCDDisplayManager import DisplayManager

dispMan = DisplayManager()

async def setup():
    
    await dispMan.addContentToDisplay("Hallo",2)
    await dispMan.addContentToDisplay("GUten Tag äh ist das zu lang?",1)

    print("ready")

async def loop():
    await dispMan.UpdateDisplay()
    
if __name__ == "__main__":
    asyncio.run(setup())
    while (True):
        asyncio.run(loop())
    
    


    