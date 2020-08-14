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
    async def RandomGenerator(self, ctx, Min : int, Max : int):
        r"""최솟값부터 최댓값 사이의 난수를 생성합니다."""
        RandomResult = int(random.randrange(Min, Max))
        await ctx.send(f"{ctx.author}: `{RandomResult}` 입니다.")
    
    @commands.command(name = "invite")
    async def Invite(self, ctx):
        Embed = discord.Embed(title="초대 링크", url=\
            "https://discord.com/api/oauth2/authorize?client_id=736998050383396996&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D736998050383396996%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D736998&scope=bot")
        await ctx.send(embed=Embed)
    
    @commands.command(name = "getascii")
    async def GetASCII(self, ctx, character):
        await ctx.send(ord(character))
    
    @commands.command(name = "getchar")
    async def GetCharacter(self, ctx, ASCII : int):
        await ctx.send(chr(ASCII))

def setup(client):
    client.add_cog(Others(client))