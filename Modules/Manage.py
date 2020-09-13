# 디스코드
import discord
from discord.ext import commands
from discord import utils

# 파이썬
import os
import asyncio
import json
import pickle

class Manage(commands.Cog, name="유저 관리"):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name="kick", aliases=["킥"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, target: discord.Member=None):
        def check(message):
            return message.content == "Y" and message.channel == ctx.channel
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            await ctx.send("정말로 서버에서 추방하시겠습니까?")
            try:
                await self.client.wait_for("message", check=check, timeout=15.0)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                await target.kick(reason=f"Banned by {ctx.author.name}")
                await ctx.send("완료.")
                
    @commands.command(name="ban", aliases=["밴"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, target: discord.Member=None):
        def check(message):
            return message.content == "Y" and message.channel == ctx.channel
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            await ctx.send("정말로 서버에서 차단하시겠습니까?")
            try:
                await self.client.wait_for("message", check=check, timeout=15.0)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                await target.ban(reason=f"Banned by {ctx.author.name}")
                await ctx.send("완료.")

    @commands.command(name="punish", aliases=["징벌"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def punish(self, ctx: commands.Context, target: discord.Member=None, Time: int=0):
        if target is None:
            await ctx.send("대상이 필요합니다.")
        if Time == 0:
            await ctx.send("징벌 시간이 필요합니다.")
        if f"{ctx.guild.id}.p" not in os.listdir("/home/pi/Desktop/Bot/Data/Role/PunishRole/"):
            await ctx.send("징벌자 역할을 설정해야 합니다.")
        if f"{ctx.guild.id}.p" not in os.listdir("/home/pi/Desktop/Bot/Data/Role/DefaultRole/"):
            await ctx.send("기본 역할을 설정해야 합니다.")
        else:
            with open(f"/home/pi/Desktop/Bot/Data/Role/PunishRole/{ctx.guild.id}.p", "rb") as File:
                await target.add_roles(pickle.load(File, encoding="utf-8"))
            with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{ctx.guild.id}.p", "rb") as File:
                await target.remove_roles(pickle.load(File, encoding="utf-8"))
            await ctx.send("대상을 징벌했습니다.")

            await asyncio.sleep(Time * 60)

            with open(f"/home/pi/Desktop/Bot/Data/Role/PunishRole/{ctx.guild.id}.p", "rb") as File:
                await target.remove_roles(pickle.load(File, encoding="utf-8"))
            with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{ctx.guild.id}.p", "rb") as File:
                Data = json.load(File)
                await target.add_roles(pickle.load(File, encoding="utf-8"))
            await ctx.send(f"{target.mention} 징벌이 끝났습니다.")
            
    @commands.command(name="+role", aliases=["addRole", "addrole", "+역할"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addRole(self, ctx: commands.Context, target: discord.Member=None, role: discord.Role=None):
        await target.add_roles(role)
        await ctx.send(f"{target.name}에게 \"{role.name}\"역할을 추가했습니다.")
    
    @commands.command(name="-role", aliases=["rmRole", "rmrole", "-역할"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removeRole(self, ctx: commands.Context, target: discord.Member=None, role: discord.Role=None):
        await target.remove_roles(role)
        await ctx.send(f"{target.name}에게 \"{role.name}\"역할을 제거했습니다")
    
    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clear(self, ctx: commands.Context, amount: int):
        if amount <= 0:
            return await ctx.send("0보다 큰 정수를 입력해주세요.")
        else:
            await ctx.channel.purge(limit=amount + 1)
    
    @commands.command(name="warning", aliases=["경고"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def warning(self, ctx, target: discord.Member=None, amount: int=None):
        if target is None:
            await ctx.send("대상을 입력해주세요.")
        elif amount is None:
            amount = 1
        elif amount < 0 or type(amount) != int:
            await ctx.send("1 이상의 정수를 입력해주세요.")
        elif target.bot:
            await ctx.send("봇에게는 경고를 부여할 수 없습니다.")
        else:
            pass
            # try:
                # def punish(self, target):
                    # with open()
                # with open(f"/home/pi/Desktop/Bot/Data/Manage/WarningList/{target.id}", "+t") as File:
                    # if int(File.read().strip()) >= 3:
                        # pass
    

def setup(client):
    client.add_cog(Manage(client))
