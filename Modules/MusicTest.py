import discord
from discord import utils
from discord.ext import commands

import asyncio
import youtube_dl
import queue

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="Mconnect", aliases=["Mjoin"])
    async def connect(self, ctx:commands.Context):
        if ctx.author.voice is None:
            return await ctx.send("음성 채널에 들어가야 합니다")
        await ctx.author.voice.channel.connect(timeout=60.0, reconnect=False)

    @commands.command(name="Mdisconnect", aliases=["Mleave", "Mquit"])
    async def disconnect(self, ctx:commands.Context):
        if ctx.author.voice is None:
            return await ctx.send("음성 채널에 있지 않습니다.")
        elif ctx.author not in ctx.guild.me.voice.channel.members:
            return await ctx.send("같은 음성 채널에 있지 않습니다.")
        else:
            try:
                await ctx.voice_client.disconnect()
            except asyncio.TimeoutError:
                await ctx.send("E: TimeoutError")
    
    @commands.command(name="Mplay")
    async def play(self, ctx: commands.Context, *url):
        if bool(url) == False:
            return await ctx.send("플레이리스트, 혹은 URL이 필요합니다.")
        else:
            MusicList = list(url)

            
    
    @commands.command(name="MdownloadMusic", aliases=["MgetMusic"])
    async def downloadMusic(self, ctx: commands.Context, url=None, musicName=None, composer=None, saveName=None):
        if url is None:
            return await ctx.send("URL이 필요합니다.")
        if musicName is None:
            return await ctx.send("이름이 필요합니다.")
        if composer is None:
            return await ctx.send("작곡가가 필요합니다.")
        if saveName is None:
            return await ctx.send("저장할 이름이 필요합니다.")
        else:
            opts = {
                "format": "bestaudio/best",
                "outtmpl": "/home/pi/Desktop/Bot/Data/MusicCache",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
            try:
                with youtube_dl.YoutubeDL(opts) as ydl:
                    ydl.download(url)
            except Exception as E:
                await ctx.send(f"E: {E}")
                
def setup(client):
    client.add_cog(Music(client))