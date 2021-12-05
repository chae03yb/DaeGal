import discord
from discord.ext import commands

import SimpleJSON
import os

class Utils:
    def __init__(self, Path:str=None):
        self.Path = Path

    def hasUserConfigFile(ctx: commands.Context):
        return os.path.exists(f"{Path}/User/{ctx.author.id}.json")
            