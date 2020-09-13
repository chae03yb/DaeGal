#!/usr/bin/python3

# 디스코드
import discord
from discord.ext import commands

# 파이썬
import os
import asyncio
import json
import pickle

client = commands.Bot(command_prefix = "?")

Modules = [
    "Manage",
    "ManageServer",
    "Bot",
#    "Others",
    "Game",
    "User",
#    "Help",
#    "MusicTest",
]

# from Modules import *

client.remove_command("help")

client.remove_cog("help")

def isOwner(ctx):
    return ctx.author.id in [434549321216688128, 724436679556988990, 373473326179549205, 480977114980417538]
    #잠ㅅ갊#3497, 잠갈 부계#7379, 8956 마이크#4156, 8956Sharp8956#8956

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"os: {os.name}")
    print("--------------------------------------------------\n")
    # i = 0

    # Presence = [
    #     discord.Game(f"ping: {int(client.latency * 1000)}"),
    #     discord.Game("도움말: ?help"),
    # ]

    # while not client.is_closed():
        # delayTime = 3
        # await asyncio.sleep(delayTime)
        # await client.change_presence(activity = Presence[i], status = discord.Status.online)
        # i += 1
        # if i > len(Presence):
        #     i = 0

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send("권한이 부족합니다.")
    elif isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f"`{int(error.retry_after / 60000)}`분 후에 다시 사용해주세요.")
    elif isinstance(error, discord.NotFound):
        await ctx.send("봇의 역할이 대상의 역할보다 아래에 있습니다.")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("인수가 필요합니다.")
    else:
        print(f"E: {error}")

@client.event
async def on_member_join(member: discord.Member):
    try:
        with open(f"/home/pi/Desktop/Bot/Data/GuildData/WelcomeMessage/{member.guild.id}.txt", "r") as File:
            await member.send(File.read())
    except FileNotFoundError:
        pass

    try:
        with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{member.guild.id}.p", "rb") as File:
            await member.add_roles(pickle.load(File, encoding="utf-8"))
    except FileNotFoundError:
        pass

class Main(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="load", aliases=["+ext"], hidden=True)
    @commands.check(isOwner)
    async def loadEx(self, ctx, ext=None):
        if ext is None:
            await ctx.send("로드할 모듈 이름을 입력해야 합니다.")
        else:
            try:
                client.load_extension(ext)
                await ctx.send(f"{ext}를 로드했습니다.")
                print(f"loaded Module: {ext}")
            except Exception as E:
                await ctx.send(f"E: {E}")

    @commands.command(name="unload", aliases=["-ext", "uload"], hidden=True)
    @commands.check(isOwner)
    async def unloadEx(self, ctx, ext=None):
        try:
            client.unload_extension(ext)
            await ctx.send(f"{ext}를 언로드했습니다.")
            print(f"unloaded Module: {ext}")
        except Exception as E:
            await ctx.send(f"E: {E}")
    
    @commands.command(name="reload", hidden=True)
    @commands.check(isOwner)
    async def reload(self, ctx):
        try:
            for ext in Modules:
                client.reload_extension(ext)
                print(f"Reloaded extensions: {ext}")
            await ctx.send("모두 리로드했습니다.")
        except Exception as E:
            await ctx.send(E)
        
if __name__ == "__main__":
    client.add_cog(Main(client))
    for cog in Modules:
        client.load_extension(cog)
        print(f"Loaded Module: {cog}")
    with open("/home/pi/Desktop/Bot/Token/Token", "r") as Token:
        client.run(Token.read())
