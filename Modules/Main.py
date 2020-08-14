#!/usr/bin/python3

# 디스코드
import discord
from discord.ext import commands

# 파이썬
import os

client = commands.Bot(command_prefix = "?")

Modules = [
    # "Main",
    "Manage",
    "Bot",
    "Others",
    "Game",
    "User"
]

client.remove_cog("help")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"os: {os.name}")
    print("--------------------------------------------------\n")
    game = discord.Game("개발")
    await client.change_presence(activity = game, status = discord.Status.online)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        pass
    if isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f"`{int(error.retry_after / 60000)}`분 후에 다시 사용해주세요.")
    else:
        print(f"E: {error}")

class Main(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "load", aliases = ["+ext"], hidden = True)
    @commands.is_owner()
    async def loadEx(self, ctx, Ext):
        try:
            client.load_extension(Ext)
            await ctx.send(f"{Ext}를 로드했습니다.")
            print(f"loaded Module: {Ext}")
        except Exception as E:
            await ctx.send(f"E: {E}")

    @commands.command(name = "unload", aliases = ["-ext", "uload"], hidden = True)
    @commands.is_owner()
    async def unloadEx(self, ctx, Ext):
        try:
            client.unload_extension(Ext)
            await ctx.send(f"{Ext}를 언로드했습니다.")
            print(f"unloaded Module: {Ext}")
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

    @commands.command(name = "Help")
    async def Help(self, ctx, com=None):
        Embed = discord.Embed(title="help", description="도움말")
        for x in Modules:
            ModuleData = self.client.get_cog(x)
            commandList = ModuleData.get_commands()
            Embed.add_field(name=x, value=" ".join([c.name for c in commandList]))
        await ctx.send(embed=Embed)
    
if __name__ == "__main__":
    client.add_cog(Main(client))
    for cog in Modules:
        client.load_extension(cog)
        print(f"Loaded Module: {cog}")
    with open("../Token/Token", "r") as Token:
        client.run(Token.read())