#!/usr/bin/python3
#-*- coding: utf-8 -*-

import discord
from discord.ext import commands

import ConsoleColors as CC
import SimpleJSON
import json
import Logger

client = commands.Bot(
    command_prefix="?",
    intents=discord.Intents.all()
)

Modules = [
    "Bot",
    "Docs",
    "ErrorHandler",
    "Game",
    "Guild",
    "GuildUser",
    "Others",
    "User",
    "Get",
    "Set"
]

CONFIG = SimpleJSON.Read("./Data/Config.json")

# adminID = (
#     434549321216688128, # 샤프#8720
#     480977114980417538, # 잠ㅅ갊#3497 
# )

adminID = tuple(CONFIG["DevList"])

Path    = "/DaeGal/Data"
LogPath = f"{Path}/Log"

def isOwner(ctx: commands.Context) -> bool:
    return ctx.author.id in adminID

# def isDisabledCommand(ctx:commands.Context):
#     return ctx.command.name in SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")["DisabledCommand"]

class Main(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{CC.BG_RGB(0, 200, 0)} Logged in as {self.client.user} {CC.EFCT.CLEAR}")
        Logger.write("INFO", f"Bot is online", open("./Data/Log/log.log", "a"))
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

def setup(client):
    client.add_cog(Main(client))

if __name__ == "__main__":
    try:
        client.remove_command("help")
        client.remove_cog("help")

        client.add_cog(Main(client))

        for Module in Modules:
            client.load_extension(Module)
            print(f"Loaded Module: {Module}")
        print("--------------------------------------------------")
        with open("./Token/Token", "r") as Token:
            client.run(Token.read())
    except KeyboardInterrupt: Logger.write("INFO" , "Terminated", open("./Data/Log/log.log", "a"))
    except Exception as E:    Logger.write("ERROR",  E,           open("./Data/Log/log.log", "a"))
