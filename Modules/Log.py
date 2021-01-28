import json
import os
import time
import SimpleJSON

T = time.strftime(r"%Y-%m-%d %H:%M", time.localtime(time.time()))
logPath = "/home/pi/Desktop/Bot/Data/Log"

def nowLoginCount():
    Data = SimpleJSON.Read(Path="/home/pi/Desktop/Bot/Data/Init.json")
    return Data

def writeLog(content: str):
    initFile = "/home/pi/Desktop/Bot/Data/Init.json"
    if not (os.path.isfile(initFile) and os.path.exists(initFile)):
        obj={"loginCount": 0}
        SimpleJSON.BackupWrite(Path=initFile, Object=obj)
    else:
        with open(f"/home/pi/Desktop/Bot/Data/Log/{nowLoginCount()}.txt", "a") as LogFile:
            LogFile.write(f"{T}: {content}")
            LogFile.write("\n")
            return

def increaseLoginCount():
    InitPath = "/home/pi/Desktop/Bot/Data/Init.json"
    Data = SimpleJSON.Read(Path=InitPath)
    Data["loginCount"] += 1
    SimpleJSON.BackupWrite(Path=InitPath, Object=Data)

increaseLoginCount()