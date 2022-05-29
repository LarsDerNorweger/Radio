#-------------------------------------------------------------------------------------------------#
#      Written for a Raspberrypi 2021                                                             #
#                                                                                                 #
#      Autor(s): Colin Böttger                                                                    #
#                                                                                                 #
#      kontakt: boettger.colin@gmail.com                                                          #
#-------------------------------------------------------------------------------------------------#


import logging
import os


class InternalOperation():
    @staticmethod
    def dumpPID(filename: str = "./PID.txt"):
        PID = os.getpid()
        logging.debug(f"dump PID: {PID} in {filename}")
        with open(filename, "w") as fs:
            fs.write(str(PID))
            fs.close()

    @staticmethod
    def shortenLog(lenght: int, filepath: str):
        try:
            with open(filepath, "r+")as fs:
                file = fs.readlines()
                l = len(file)
                if l >= lenght:
                    fs.seek(0)
                    fs.writelines(file[l-lenght:l])
                    fs.truncate()
        except Exception as e:
            logging.error("LoggingFile can't be shorten", exc_info=True)

    @staticmethod
    def configLogging(filename: str):
        logging.basicConfig(
            filename=filename,
            level=logging.DEBUG,
            format='%(process)d-%(levelname)s-%(message)s'
        )
        pass
