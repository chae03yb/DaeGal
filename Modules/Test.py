import discord
from discord.ext import commands
import DaeGal_Utils
import random
import asyncio

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="d")
    async def d(self, ctx: commands.Context):
        duration = random.randint(7, 15)
        msg = await ctx.send(f"주사위: {random.randint(1, 6)}")
        for d in range(duration):
            await asyncio.sleep(0.2)
            await msg.edit(content=f"{random.randint(1, 6)}")
        await msg.edit(content=f"결과: {random.randint(1, 6)}")

def setup(client):
    client.add_cog(Test(client))
