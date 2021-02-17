import os
import time
import SimpleJSON

T = time.strftime(r"%Y-%m-%d %H:%M", time.localtime(time.time())) + " GMT"
LogPath = "/DaeGal/Data/Log"

def LoginCount():
    Data = SimpleJSON.Read(Path="/DaeGal/Data/Config.json")
    return Data["loginCount"]

def Write(Type: str, content: str):
    initFile = "/DaeGal/Data/Config.json"
    if not (os.path.isfile(initFile) and os.path.exists(initFile)):
        obj={"loginCount": 0}
        SimpleJSON.BackupWrite(Path=initFile, Object=obj)
    else:
        with open(f"{LogPath}/{LoginCount()}.txt", "a") as LogFile:
            LogFile.write(f"[ {T} ] [ {Type} ] {content}")
            LogFile.write("\n")

def increaseLoginCount():
    InitPath = "/DaeGal/Data/Config.json"
    Data = SimpleJSON.Read(Path=InitPath)
    Data["loginCount"] += 1
    SimpleJSON.BackupWrite(Path=InitPath, Object=Data)
