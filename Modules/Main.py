#!/usr/bin/python3
#-*- coding: utf-8 -*-

import discord
from discord.ext import commands
import Log

import ConsoleColors as CC
import json

client = commands.Bot(
    command_prefix="?",
    intents=discord.Intents.all()
)

Modules = [
    "Bot",
    # "Commands",
    # "CustomCommands",
    "Docs",
    "ErrorHandler",
    "Game",
    "Guild",
    "GuildUser",
    # "MailService",
    # "MusicTest",
    "Others",
    "User",
    # "slashTest"
]

adminID = (
    434549321216688128, # 샤프#8720
    480977114980417538, # 잠ㅅ갊#3497 
)

LogPath = "/home/pi/Desktop/Bot/Data/Log"
Path    = "/home/pi/Desktop/Bot/Data"

def isOwner(ctx):
    return ctx.author.id in adminID

class Main(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{CC.BG_RGB(0, 200, 0)} Logged in as {self.client.user} {CC.EFCT.CLEAR}")
        print("--------------------------------------------------")

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
                print(f"{CC.TEXT.BrightGreen} Loaded Module: {ext} {CC.EFCT.CLEAR}")
            except Exception as E:
                await ctx.send(f"E: {E}")

    @commands.command(name="unload", aliases=["-ext", "uload"], hidden=True)
    @commands.check(isOwner)
    async def unloadEx(self, ctx: commands.Context, ext=None):
        try:
            client.unload_extension(ext)
            Modules.remove(ext)
            await ctx.send(f"{ext}를 언로드했습니다.")
            print(f"{CC.TEXT.BrightRed} Unloaded Module: {ext} {CC.EFCT.CLEAR}")
        except Exception as E:
            await ctx.send(f"E: {E}")
    
    @commands.command(name="reload", hidden=True)
    @commands.check(isOwner)
    async def reload(self, ctx: commands.Context, category=None):
        if category is None:
            try:
                for ext in Modules:
                    client.reload_extension(ext)
                    print(f"{CC.TEXT.BrightGreen} Reloaded Module: {ext} {CC.EFCT.CLEAR}")
                print("--------------------------------------------------")
                Embed = discord.Embed(
                    title="성공",
                    description="모든 모듈을 리로드했습니다",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)
            except Exception as Error:
                Embed = discord.Embed(
                    title="실패",
                    description=f"```사유: {Error}```",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
        else:
            try:
                client.reload_extension(category)
                ext = category
                print(f"{CC.TEXT.BrightGreen} Reloaded Module: {ext} {CC.EFCT.CLEAR}")
                print("--------------------------------------------------")
                Embed = discord.Embed(
                    title="성공",
                    description=f"{ext} 모듈을 리로드했습니다",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)
            except Exception as Error:
                Embed = discord.Embed(
                    title="실패",
                    description=f"```사유: {Error}```",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)

    @commands.command(name="currentMainVer", aliases=["curMainVer"])
    @commands.check(isOwner)
    async def currentMainVer(self, ctx: commands.Context):
        await ctx.send("VER: STABLE")

    @commands.command(name="disableCategory", aliases=["카테고리_비활성화"])
    # @commands.has_permissions(administrator=True)
    async def disableCategory(self, ctx: commands.Context, *category):
        if category is None:
            Embed = discord.Embed(
                title="오류",
                description="비활성화할 카테고리가 필요합니다",
                color=0xFF0000
            )
            return await ctx.send(embed=Embed)

        with open(f"{Path}/Guild/{ctx.guild.id}/disabledCategory.json", "r") as File:
            # {
            #     "disabledCategory": [
            #         "cat1",
            #         "cat2"
            #     ]
            # }
            Config = json.load(fp=File)
            # await ctx.send("asdf")
            with open(f"{Path}/Guild/{ctx.guild.id}/disabledCategory.json", "w") as File:
                json.dump(Config.update({"disabledCategory": list(category)}))
                await ctx.send("완료")

if __name__ == "__main__":
    try:
        client.remove_command("help")
        client.remove_cog("help")
        client.add_cog(Main(client))

        for Module in Modules:
            client.load_extension(Module)
            print(f"Loaded Module: {Module}")
        print("--------------------------------------------------")
        with open("/DaeGal/Token/Token", "r") as Token:
            client.run(Token.read())
    except KeyboardInterrupt:
        pass
    # except Exception as E:
        # print(f"{CC.BG.RED} E: {E} {CC.EFCT.CLEAR}")
