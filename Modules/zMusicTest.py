# 디스코드
import discord
from discord.ext import commands
from discord.utils import get
import discord.voice_client

# 파이썬
import asyncio

# 음악
import youtube_dl

players = {}

class Music(commands.Cog):
    voice = None
    
    def __init__(self, client):
        self.client = client

    @commands.command(name=">", aliases=["play", "p"])
    @commands.guild_only()
    async def play(self, ctx, url):
        server = ctx.message.guild
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()


    # @commands.command(name="", aliases=["stop", "s"])
    # @commands.guild_only()

    # @commands.command(name="||", aliases=["pause"])

    # @commands.command(name=">>", aliases=["skip"])
    # @commands.guild_only()

    # @commands.command(name="[]", aliases=["queue", "list"])
    # @commands.guild_only()

    @commands.command(name="join", aliases=[])
    @commands.guild_only()
    async def join(self, ctx: commands.Context):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f"{channel} 에 참가했습니다.")

    # @commands.command(name="loop", aliases=[])
    # @commands.guild_only()

    @commands.command(name="leave", aliases=[])
    @commands.guild_only()
    async def leave(self, ctx: commands.Context):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send("채널에서 나왔습니다.")

        else:
            pass
            # await ctx.send("채널에 참가하지 않았습니다.")

def setup(client):
    client.add_cog(Music(client))