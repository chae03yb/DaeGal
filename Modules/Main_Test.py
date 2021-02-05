#!/usr/bin/python3

import discord
from discord.ext import commands
import Log

client = commands.Bot(
    command_prefix="?",
    intents=discord.Intents.all()
)

Modules = [
    "Bot",
#    "Commands",
#    "CustomCommands",
    "Docs",
    "ErrorHandler",
    "Game",
    "Guild",
    "GuildUser",
#    "Log",
#    "MailService",
#    "MusicTest",
    "Others",
    "User",
]

adminID = (
    434549321216688128, # 샤프#8720
    480977114980417538, # 잠ㅅ갊#3497
)

DataPath = "/home/pi/Desktop/Bot/Data"

def isOwner(ctx: commands.Context):
    return ctx.author.id in adminID

class Main(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.Modules = Modules

    @commands.Cog.listener()
    async def on_ready(self):
        Log.increaseLoginCount()
        Log.Write("Login", f"Logged in as {self.client.user}")
#        print(f"{CC.BG_RGB(0, 200, 0)} Logged in as {self.client.user} {CC.EFCT.CLEAR}")

    @commands.command(name="load", hidden=True)
    @commands.check(isOwner)
    async def loadEx(self, ctx: commands.Context, ext=None):
        if ext is None:
            await ctx.send("로드할 모듈 이름을 입력해야 합니다.")
        else:
            try:
                client.load_extension(ext)
                Modules.append(ext)
                Modules.sort()
                await ctx.send(f"{ext}를 로드했습니다.")
                Log.Write("Success", f"Loaded Module: {ext}")
            except Exception as E:
                await ctx.send(f"E: {E}")

    @commands.command(name="unload", hidden=True)
    @commands.check(isOwner)
    async def unloadEx(self, ctx: commands.Context, ext=None):
        try:
            client.unload_extension(ext)
            Modules.remove(ext)
            Modules.sort()
            await ctx.send(f"{ext}를 언로드했습니다.")
            Log.Write("Success", f"Unloaded Module: {ext}")
        except Exception as E:
            await ctx.send(f"E: {E}")
    
    @commands.command(name="reload", hidden=True)
    @commands.check(isOwner)
    async def reload(self, ctx: commands.Context):
        try:
            for ext in Modules:
                client.reload_extension(ext)
                Log.Write("Success", f"Reloaded Module: {ext}")
            await ctx.send("모두 리로드했습니다.")
        except Exception as E:
            await ctx.send(E)

    @commands.command(name="currentMainVer")
    @commands.check(isOwner)
    async def currentMainVer(self, ctx: commands.Context):
        await ctx.send("VER: TEST")

if __name__ == "__main__":
    try:
        client.remove_command("help")
        client.remove_cog("help")
        client.add_cog(Main(client))
        for Module in Modules:
            client.load_extension(Module)
            Log.Write("Success", f"Loaded Module: {Module}")
        print("--------------------------------------------------")
        with open("/home/pi/Desktop/Bot/Token/Token", "r") as Token:
            client.run(Token.read())
    except KeyboardInterrupt:
        Log.Write("Shutdown", "Terminated by KeyboardInterrupt")
    except Exception as E:
        Log.Write("Error", f"Error: {E}")
