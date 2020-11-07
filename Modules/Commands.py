import discord
from discord.ext import commands
from discord.utils import get

import asyncio

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def msg(self, ctx, *, msg):
        await ctx.send(str(msg))
        return
    
    @commands.command()
    async def wait(self, ctx, time: float or int):
        await asyncio.sleep(time)
        return

def setup(client):
    client.add_cog(Commands(client))