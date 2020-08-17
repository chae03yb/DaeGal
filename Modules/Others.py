# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import random
import asyncio

class Others(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = "random")
    async def RandomGenerator(self, ctx, Min: int, Max : int):
        # r"""최솟값부터 최댓값 사이의 난수를 생성합니다."""
        RandomResult = int(random.randrange(Min, Max))
        await ctx.send(f"{ctx.author}: `{RandomResult}` 입니다.")
    
    @commands.command(name = "getascii")
    async def GetASCII(self, ctx, arg = None):
        if arg == "-h":
            await ctx.send("`?getascii <문자>`")
        else:
            await ctx.send(ord(arg))
    
    @commands.command(name = "getchar")
    async def GetCharacter(self, ctx, arg = None):
        if type(arg) is str:
            if arg == "-h":
                await ctx.send("`?getchar <int>`")
        else:
            await ctx.send(chr(ASCII))

def setup(client):
    client.add_cog(Others(client))