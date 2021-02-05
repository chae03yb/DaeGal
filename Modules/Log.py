import os
import time
import SimpleJSON

T = time.strftime(r"%Y-%m-%d %H:%M", time.localtime(time.time())) + " GMT"
logPath = "/home/pi/Desktop/Bot/Data/Log"

def LoginCount():
    Data = SimpleJSON.Read(Path="/home/pi/Desktop/Bot/Data/Config.json")
    return Data["loginCount"]

def Write(Type: str, content: str):
    initFile = "/home/pi/Desktop/Bot/Data/Config.json"
    if not (os.path.isfile(initFile) and os.path.exists(initFile)):
        obj={"loginCount": 0}
        SimpleJSON.BackupWrite(Path=initFile, Object=obj)
    else:
        with open(f"/home/pi/Desktop/Bot/Data/Log/{LoginCount()}.txt", "a") as LogFile:
            LogFile.write(f"[ {T} ] [ {Type} ] {content}")
            LogFile.write("\n")

def increaseLoginCount():
    InitPath = "/home/pi/Desktop/Bot/Data/Config.json"
    Data = SimpleJSON.Read(Path=InitPath)
    Data["loginCount"] += 1
    SimpleJSON.BackupWrite(Path=InitPath, Object=Data)
