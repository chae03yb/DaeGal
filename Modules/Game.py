# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import random
import pickle

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="+돈", aliases=["+$", "돈받기"])
    @commands.cooldown(rate=1, per=3600000, type=commands.BucketType.user)
    async def getMoney(self, ctx):
        Money = random.randint(10000, 100000)
        Path = "/home/pi/Desktop/Bot/Data/Economy"
        try:
            with open(f"{Path}/{ctx.author.id}.bin", "+wb") as Data:
                if pickle.load(Data) is None:
                    pickle.dump(Money, Data)
                else:
                    GetMoney = pickle.load(Data) + Money
                    pickle.dump(GetMoney)
                await ctx.send(f"`{Money}`원을 받았습니다.")
        except EOFError:
            pass
        except Exception as E:
            await ctx.send(E)
            
    @commands.command(name="?$")
    async def wallet(self, ctx):
        with open(f"/home/pi/Desktop/Bot/Data/Economy/{ctx.author.id}.bin", "rb") as Data:
            try:
                await ctx.send(pickle.load(Data))
            except EOFError:
                pass

def setup(client):
    client.add_cog(Game(client))
    