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
    async def CustomCommand(self, ctx: commands.Context, *then):
        cmds = str(then)
        cmd = cmds.split(";")
        while True:
            Num = 0
            Command = str(cmd[Num].split("|"))
            Value = Command[1]
            try:
                setattr(Commands, Command[Num], Value)
            except IndexError:
                break
            except Exception as E:
                await ctx.send(E)
            else:
                Num += 1
        """반복문으로 Command[Num]을 차례대로 exec을 통해 실행."""
        """대괄호로 인수를 받고 Command.replace()"""

def setup(client):
    client.add_cog(CustomCommand(client))