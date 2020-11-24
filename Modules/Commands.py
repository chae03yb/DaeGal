import discord
from discord.ext import commands
from discord.utils import get

import asyncio

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def write(self, ctx, msg):
        await ctx.send(str(msg))
    
    async def wait(self, ctx, time: float or int):
        await asyncio.sleep(time)

def setup(client):
    client.add_cog(Commands(client))