# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import random
import sqlite3
import json
import asyncio
import time

class Others(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "vote", aliases = ["투표"])
    @commands.guild_only()
    async def makeVote(self, ctx: commands.Context, itemAmount: int, endDate: str, *, description = None):
        itemList = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        waitTime = 5.0

        async def sleepAndDelete(self, ctx, limit: int):
            await asyncio.sleep(waitTime)
            await ctx.channel.purge(limit = limit)

        if itemAmount > len(itemList):
            await ctx.channel.send(f"투표 항목은 최대 {len(itemList)}개입니다.\n\n{int(waitTime)}초 후 이 메시지와 사용된 명령은 삭제됩니다.")
            await sleepAndDelete(self = self, ctx = ctx, limit = 2)
            return
        elif itemAmount < 2:
            await ctx.channel.send(f"투표 항목은 최소 2개 이상이어야 합니다.\n\n{int(waitTime)}초 후 이 메시지와 사용된 명령은 삭제됩니다.")
            await sleepAndDelete(self = self, ctx = ctx, limit = 2)
            return
        if description is None:
            await ctx.channel.send(f"내용을 적어주세요\n\n{int(waitTime)}초 후 이 메시지와 사용된 명령은 삭제됩니다.")
            await sleepAndDelete(self = self, ctx = ctx, limit = 2) 
            return
        else:
            await ctx.channel.purge(limit=1)
            Embed = discord.Embed(
                color=0x000000,
                title="투표",
                description=f"작성자: {ctx.message.author}"
            )
            Embed.add_field(name=f"투표 항목: {itemAmount}", value=description, inline=False)
            msg = await ctx.channel.send(embed=Embed)

            for i in range(0, itemAmount):
                await msg.add_reaction(itemList[i])
            """
            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji)
            
            now = time.localtime()
            
            for now == 
            """
            # ✅를 반응으로 달 시 투표 종료 기능
        
def setup(client):
    client.add_cog(Others(client))
