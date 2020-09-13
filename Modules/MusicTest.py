import discord
from discord.ext import commands
from discord.utils import get
import asyncio

class Music(commands.Cog, name = "음악"):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "play", alises = ["p"])
    @commands.guild_only()

def setup(client):
    client.add_cog(Bot(client))