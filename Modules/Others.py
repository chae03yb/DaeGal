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

class Others(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command(name="메모", aliases=["memo"])
    async def memo(self, ctx: commands.Context, Title=None, *Memo):
        con = sqlite3.connect(f"/home/pi/Desktop/Bot/Data/Memo/{ctx.guild.id}")
        cur = con.cursor()
        if Title is None:
            await ctx.send("열람/업데이트할 메모의 제목을 같이 입력해주십시오")
        elif bool(Memo) is False:
            try:
                with con:
                    Embed = discord.Embed(
                        title=Title,
                        # description=,
                        color=0x000000
                    )
                    # Embed.set_footer(text=f"Created By: {}")
                    await ctx.send(embed=Embed)

        # elif bool(Memo) is True:
            # with 
    
    @commands.command(name="-메모", aliases=["-memo"])
    async def rmMemo(self, ctx: commands.Context, Title=None):
        
        await ctx.send("메모를 삭제했습니다.")
    
def setup(client):
    client.add_cog(Others(client))