# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import random
import json
import asyncio
import sqlite3

import Main

class Others(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="메모", aliases=["memo"])
    @commands.check(Main.isOwner)
    async def memo(self, ctx: commands.Context, *Memo):
        con = sqlite3.connect(f"/home/pi/Desktop/Bot/Data/Memo/{ctx.guild.id}.sqlite3")
        cur = con.cursor()

        # -i --immutable: 생성 후 수정 불가
        # -o --owner-only: 메세지 생성한 사람만 수정 가능.
        # -io: 두 옵션
        
        if bool(Memo) is False: # 
            await ctx.send("열람/업데이트할 메모의 제목을 같이 입력해주십시오")

        else: #
            try:
                Memo[2]
            except IndexError:
                await ctx.send("view")
            else:
                if "-i" in Memo or "--immutable" in Memo:
                    await ctx.send("immutable option")
                elif "-o" in Memo or "--owner-only" in Memo:
                    await ctx.send("owner only option")
                elif "-io" in Memo:
                    await ctx.send("-i -o")
                else:
                    await ctx.send("else")
    """
    @commands.command(name="-메모", aliases=["-memo"])
    async def rmMemo(self, ctx: commands.Context, Title=None):
        await ctx.send("메모를 삭제했습니다.")
    """
def setup(client):
    client.add_cog(Others(client))