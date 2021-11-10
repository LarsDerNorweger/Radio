import os

class InternalOperation():

    def dumpPID(filename = "./PID.txt"):
        PID = os.getpid()
        print(PID)
        with open(filename,"w") as file:
            file.write(str(PID))
            file.close()