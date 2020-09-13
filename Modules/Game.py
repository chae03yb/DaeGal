# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import random
import json

class Game(commands.Cog, name="게임"):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = "random", aliases = ["랜덤"])
    async def RandomGenerator(self, ctx: commands.Context, Min: int=None, Max : int=None):
        if Min or Max is None:
            await ctx.send("난수를 생성할 범위의 정수 두개를 입력해야 합니다.")
        else:
            RandomResult = random.randint(Min, Max)
            await ctx.send(f"{ctx.author}: `{RandomResult}` 입니다.")

    @commands.command(name="dice", aliases=["주사위"])
    async def dice(self, ctx: commands.Context):
        await ctx.send(f"주사위: {random.randint(1, 6)}")

    # 카드게임
    # 턴제 전략 게임

def setup(client):
    client.add_cog(Game(client))
    