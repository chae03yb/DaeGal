import discord
from discord.ext import commands
from discord.utils import get

import os
import asyncio
import json

import Commands

class CustomCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "customcmd") # aliases = ["cmd"])
    async def CustomCommand(self, ctx: commands.Context, *, then: str):
        pass

def setup(client):
    client.add_cog(CustomCommand(client))