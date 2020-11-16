# 디스코드
import discord
from discord.ext import commands
from discord.utils import get
import discord.voice_client

# 파이썬
import asyncio

# 음악
import youtube_dl

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command(name=">", aliases=["play", "p"])
    # @commands.guild_only()

    # @commands.command(name="", aliases=["stop", "s"])
    # @commands.guild_only()

    # @commands.command(name="||", aliases=["pause"])

    # @commands.command(name=">>", aliases=["skip"])
    # @commands.guild_only()

    # @commands.command(name="[]", aliases=["queue", "list"])
    # @commands.guild_only()

    # @commands.command(name="join", aliases=[])
    # @commands.guild_only()

    # @commands.command(name="loop", aliases=[])
    # @commands.guild_only()

    # @commands.command(name="leave", aliases=[])
    # @commands.guild_only()

def setup(client):
    client.add_cog(Music(client))