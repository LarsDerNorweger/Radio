#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#

from Internal.InternalOperation import InternalOperation


def mainplayground():
    InternalOperation.shortenLog(5, "./test.py")
    InternalOperation.shortenLog(5, "./test.py")
    pass


if __name__ == "__main__":
    mainplayground()
