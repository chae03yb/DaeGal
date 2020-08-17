#!/usr/bin/python3

# 디스코드
import discord
from discord.ext import commands

# 파이썬
import os
import asyncio

from Bot import Bot
from Game import Game
from Manage import Manage
from Others import Others
from User import User

client = commands.Bot(command_prefix = "?")

Modules = [
    "Manage",
    "Bot",
    # "Others",
    # "Game",
    "User"
]

client.remove_cog("help")

def isOwner(ctx):
    return ctx.author.id in [434549321216688128, 724436679556988990, 373473326179549205, 480977114980417538]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"os: {os.name}")
    print("--------------------------------------------------\n")
    while not client.is_closed():
        delayTime = 300

        await asyncio.sleep(delayTime)
        await client.change_presence(activity = discord.Game(f"ping: {int(client.latency * 1000)}"), status = discord.Status.online)
        
        await asyncio.sleep(delayTime)
        await client.change_presence(activity = discord.Game(f"도움말: ?도움말"), status = discord.Status.online)

        await asyncio.sleep(delayTime)
        await client.change_presence(activity = discord.Game("테스트", activity = discord.Status.online))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("권한이 부족합니다.")
    if isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f"`{int(error.retry_after / 60000)}`분 후에 다시 사용해주세요.")
    if isinstance(error, discord.NotFound):
        await ctx.send("봇의 역할이 대상의 역할보다 아래에 있습니다.")
    else:
        print(f"E: {error}")

class Main(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name = "load", aliases = ["+ext"], hidden = True)
    @commands.check(isOwner)
    async def loadEx(self, ctx, arg = None):
        if arg is None:
            await ctx.send("로드할 모듈 이름을 입력해야 합니다.")
        else:
            try:
                client.load_extension(arg)
                await ctx.send(f"{arg}를 로드했습니다.")
                print(f"loaded Module: {arg}")
            except Exception as E:
                await ctx.send(f"E: {E}")

    @commands.command(name = "unload", aliases = ["-ext", "uload"], hidden = True)
    @commands.check(isOwner)
    async def unloadEx(self, ctx, arg = None):
        @property
        def Help(self):
            "`?unload <모듈>`"
            return self._Help

        try:
            client.unload_extension(arg)
            await ctx.send(f"{arg}를 언로드했습니다.")
            print(f"unloaded Module: {arg}")
        except Exception as E:
            await ctx.send(f"E: {E}")
    
    @commands.command(name = "reload", hidden = True)
    @commands.is_owner()
    async def reload(self, ctx):
        try:
            for cog in Modules:
                client.reload_extension(cog)
                print(f"Reloaded extensions: {cog}")
            await ctx.send("모두 리로드했습니다.")
        except Exception as E:
            await ctx.send(E)

    @commands.command(name = "도움말")
    async def HelpCommand(self, ctx: commands.Context, command=None):
        await ctx.send(f"{command}")
        
if __name__ == "__main__":
    client.add_cog(Main(client))
    for cog in Modules:
        client.load_extension(cog)
        print(f"Loaded Module: {cog}")
    with open("../Token/Token", "r") as Token:
        client.run(Token.read())