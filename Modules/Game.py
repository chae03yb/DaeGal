# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import random
import json
import asyncio

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="random", aliases=["랜덤"])
    async def RandomNumberGenerator(self, ctx: commands.Context, Min=None, Max=None):
        if Min == None:
            await ctx.send("시작 값을 입력해주세요.")
        elif Max == None:
            await ctx.send("끝 값을 입력해주세요.")
        elif Min > Max:
            await ctx.send("시작 값은 끝 값보다 클 수 없습니다.")
        else:
            try:
                RandomResult = random.randint(int(Min), int(Max))
                await ctx.send(f"{ctx.author}: `{RandomResult}` 입니다.")
            except ValueError:
                await ctx.send("시작 값/끝 값을 정수로 입력해주세요.")

    @commands.command(name="dice", aliases=["주사위"])
    async def dice(self, ctx: commands.Context):
        await ctx.send(f"주사위: {random.randint(1, 6)}")
    
    @commands.command(name="choice", aliases=["선택"])
    async def choice(self, ctx: commands.Context, *contents):
        if bool(contents) is False:
            await ctx.send("선택할 항목들을 1개 이상 넣어주세요.")
        else:
            await ctx.send(f"{ctx.author.mention}, {random.choice(contents)}이 좋겠군요.")
    
    @commands.command(name="조커뽑기")
    async def Joker(self, ctx: commands.Context):
        pass
            
    # 카드게임
    # 턴제 전략 게임
    # 도박
    # 주식

def setup(client):
    client.add_cog(Game(client))
    