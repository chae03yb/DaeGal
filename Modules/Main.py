#!/usr/bin/python3

# 디스코드
import discord
from discord.ext import commands
from discord import utils

# 파이썬
import os
import asyncio
import json
import pickle
import random

import ConsoleColors as CC

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
    "MailService",
    "MusicTest",
    "Others",
    "User",
]

adminID = (
    434549321216688128, # 샤프#8720
    480977114980417538, # 잠ㅅ갊#3497 
    373473326179549205, # 샤프 마이크#4156
)

def isOwner(ctx):
    return ctx.author.id in adminID

class Main(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.DataPath = "/home/pi/Desktop/Bot/Data"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{CC.BG_RGB(0, 200, 0)} Logged in as {self.client.user} {CC.EFCT.CLEAR}")
        print(f"os: {os.name}")
        print("--------------------------------------------------\n")

    @commands.command(name="load", aliases=["+ext"], hidden=True)
    @commands.check(isOwner)
    async def loadEx(self, ctx: commands.Context, ext=None):
        if ext is None:
            await ctx.send("로드할 모듈 이름을 입력해야 합니다.")
        else:
            try:
                client.load_extension(ext)
                Modules.append(ext)
                await ctx.send(f"{ext}를 로드했습니다.")
                print(f"{CC.TXT.BR_GREEN} Loaded Module: {ext} {CC.EFCT.CLEAR}")
            except Exception as E:
                await ctx.send(f"E: {E}")

    @commands.command(name="unload", aliases=["-ext", "uload"], hidden=True)
    @commands.check(isOwner)
    async def unloadEx(self, ctx: commands.Context, ext=None):
        try:
            client.unload_extension(ext)
            await ctx.send(f"{ext}를 언로드했습니다.")
            print(f"{CC.TXT.BR_RED} Unloaded Module: {ext} {CC.EFCT.CLEAR}")
        except Exception as E:
            await ctx.send(f"E: {E}")
    
    @commands.command(name="reload", hidden=True)
    @commands.check(isOwner)
    async def reload(self, ctx: commands.Context):
        try:
            for ext in Modules:
                client.reload_extension(ext)
                print(f"{CC.TXT.BR_GREEN} Reloaded Module: {ext} {CC.EFCT.CLEAR}")
            print("--------------------------------------------------")
            await ctx.send("모두 리로드했습니다.")
        except Exception as E:
            await ctx.send(E)

if __name__ == "__main__":
    try:
        client.remove_command("help")
        client.remove_cog("help")
        client.add_cog(Main(client))
        for Module in Modules:
            client.load_extension(Module)
            print(f"{CC.TXT.BR_GREEN} Loaded Module: {Module} {CC.EFCT.CLEAR}")
        print("--------------------------------------------------")
        with open("/home/pi/Desktop/Bot/Token/Token", "r") as Token:
            client.run(Token.read())
    except KeyboardInterrupt:
        pass
    # except Exception as E:
        # print(f"{CC.BG.RED} E: {E} {CC.EFCT.CLEAR}")
