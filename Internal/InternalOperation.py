#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#


import os


class InternalOperation():
    @staticmethod
    def dumpPID(self, filename: str = "./PID.txt"):
        PID = os.getpid()
        print(PID)
        with open(filename, "w") as fs:
            fs.write(str(PID))
            fs.close()

    @staticmethod
    def shortenLog(lenght: int, filepath: str):
        with open(filepath, "r+")as fs:
            file = fs.readlines()
            l = len(file)
            if l >= lenght:
                fs.seek(0)
                fs.writelines(file[l-lenght:l])
                fs.truncate()

        pass
