import Main
from discord.ext import commands
import json
import os
import time
import FileSize
import discord

T = time.strftime(r"%Y-%m-%d %H:%M", time.localtime(time.time()))

def nowLoginCount():
    with open("/home/pi/Desktop/Bot/Data/Init.json", "r") as CountFile:
        Data = json.load(fp=CountFile)["loginCount"]
        return Data

def writeLog(content: str):
    initFile = "/home/pi/Desktop/Bot/Data/Init.json"
    if not (os.path.isfile(initFile) and os.path.exists(initFile)): # Init.json이 있는지 확인
        with open("/home/pi/Desktop/Bot/Data/Init.json", "w") as ConfigFile:
            json.dump(fp=ConfigFile, obj={"loginCount": 0}, indent=4)
    else:
        with open(f"/home/pi/Desktop/Bot/Data/Log/{nowLoginCount()}.txt", "a") as LogFile:
            LogFile.write(f"{T}: {content}")
            LogFile.write("\n")
            return

def loginCount_up():
    with open(f"/home/pi/Desktop/Bot/Data/Init.json", "w+") as InitFile:
        loginCount = json.load(fp=InitFile)["loginCount"]
        jsonData = {"loginCount": loginCount + 1}
        json.dump(fp=InitFile, obj=jsonData, indent=4)
        return

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group(name = "log")
    @commands.check(Main.isOwner)
    async def log(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send("수행할 작업을 입력해주세요.")

    @log.command(name = "view")
    async def Log_read(self, ctx: commands.Context, logver: int=nowLoginCount()):
        if os.path.getsize(f"/home/pi/Desktop/Bot/Data/Log/{logver}.txt") > (8 * FileSize.Size.MegaByte):
            return await ctx.send("파일 용량이 너무 큽니다.")
        else:
            await ctx.send(file = discord.File(f"/home/pi/Desktop/Bot/Data/Log/{logver}.txt"))

    @log.command(name = "write")
    async def log_write(self, ctx: commands.Context, *, content: str):
        try:
            writeLog(f"{content}")
            return await ctx.send("성공했습니다.")
        except Exception as E:
            return await ctx.send(f"E: {E}")

def setup(client):
    client.add_cog(Log(client))