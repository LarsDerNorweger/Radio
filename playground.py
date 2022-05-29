#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

from Internal.InternalOperation import InternalOperation
import logging


def mainplayground():
    InternalOperation.configLogging("./Radio.log")
    InternalOperation.dumpPID()
    InternalOperation.shortenLog(5, "Radio.log")
    pass


if __name__ == "__main__":
    mainplayground()
