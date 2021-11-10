#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #                  
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#



import os

class InternalOperation():

    def dumpPID(filename = "./PID.txt"):
        PID = os.getpid()
        print(PID)
        with open(filename,"w") as file:
            file.write(str(PID))
            file.close()