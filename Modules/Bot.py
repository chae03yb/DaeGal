# 디스코드
import discord
from discord.ext import commands

class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = "ping")
    async def ping(self, ctx):
        await ctx.send(f"pong! `{int(self.client.latency * 1000)}ms`")

    @commands.command(name = "logout", hidden = True)
    @commands.is_owner()
    async def Logout(self, ctx):
        try:
            await ctx.send("종료중...")
            await self.client.logout()
            print(f"Terminated by {ctx.author.name}")
            os._exit(0)
        except Exception as E:
            await ctx.send(f"E: {E}")

def setup(client):
    client.add_cog(Bot(client))