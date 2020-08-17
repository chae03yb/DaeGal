# 디스코드
import discord
from discord.ext import commands
from discord import utils

# 파이썬
import os
import asyncio
import json

class Manage(commands.Cog, name = "유저 관리"):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name = "setPunishRole")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setPunishRole(self, ctx: commands.Context, role: discord.Role):
        with open(f"/home/pi/Desktop/Bot/Data/Role/PunishRole/{ctx.guild.id}.json", "w") as File:
            Data = { "PunishRole": role.id }
            json.dump(Data, fp = File, indent = 4)
            await ctx.send("설정 완료")
    
    @commands.command(name = "setDefaultRole")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setDefaultRole(self, ctx: commands.Context, role: discord.Role):
        with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{ctx.guild.id}.json", "w") as File:
            Data = { "DefaultRole": role.id }
            json.dump(Data, fp = File, indent = 4)
            await ctx.send("설정 완료.")
    
    @commands.command(name = "setBotRole")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setBotRole(self, ctx: commands.Context, role: discord.Role):
        with open(f"/home/pi/Desktop/Bot/Data/Role/BotRole/{ctx.guild.id}.json", "w") as File:
            Data = { "BotRole": role.id }
            json.dump(Data, fp = File, indent = 4)
            await ctx.send("설정 완료.")
    
    @commands.command(name = "kick")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, target: discord.Member = None):
        def check(message):
            return message.content == "Y" and message.channel == ctx.channel
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            await ctx.send("정말로 서버에서 추방하시겠습니까?")
            try:
                await self.client.wait_for("message", check = check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                await target.kick(reason = f"Banned by {ctx.author.name}")
                await ctx.send("완료.")
                
    @commands.command(name = "ban")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, target: discord.Member = None):
        def check(message):
            return message.content == "Y" and message.channel == ctx.channel
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            await ctx.send("정말로 서버에서 차단하시겠습니까?")
            try:
                await self.client.wait_for("message", check = check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                await target.ban(reason = f"Banned by {ctx.author.name}")
                await ctx.send("완료.")

    @commands.command(name = "punish")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def punish(self, ctx: commands.Context, target: discord.Member = None, Time: int = 0):
        if target is None:
            await ctx.send("대상이 필요합니다.")
        if Time == 0:
            await ctx.send("징벌 시간이 필요합니다.")
        if f"{ctx.guild.id}.json" not in os.listdir("/home/pi/Desktop/Bot/Data/Role/PunishRole/"):
            await ctx.send("징벌자 역할을 설정해야 합니다.")
        if f"{ctx.guild.id}.json" not in os.listdir("/home/pi/Desktop/Bot/Data/Role/DefaultRole/"):
            await ctx.send("기본 역할을 설정해야 합니다.")
        else:
            with open(f"/home/pi/Desktop/Bot/Data/Role/PunishRole/{ctx.guild.id}.json", "r") as File:
                Data = json.load(File)
                await target.add_roles(ctx.guild.get_role(Data["PunishRole"]))
            with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{ctx.guild.id}.json", "r") as File:
                Data = json.load(File)
                await target.remove_roles(ctx.guild.get_role(Data["DefaultRole"]))
            await ctx.send("대상을 징벌했습니다.")

            await asyncio.sleep(Time * 60)

            with open(f"/home/pi/Desktop/Bot/Data/Role/PunishRole/{ctx.guild.id}.json", "r") as File:
                Data = json.load(File)
                await target.remove_roles(ctx.guild.get_role(Data["PunishRole"]))
            with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{ctx.guild.id}.json", "r") as File:
                Data = json.load(File)
                await target.add_roles(ctx.guild.get_role(Data["DefaultRole"]))
            await ctx.send(f"{target.mention} 징벌이 끝났습니다.")
            
    @commands.command(name = "+role", aliases = ["addRole", "addrole"])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def addRole(self, ctx: commands.Context, target: discord.Member = None, role: discord.Role = None):
        await target.add_roles(role)
        await ctx.send(f"{target.name}에게 {role.name}역할을 추가했습니다.")
    
    @commands.command(name = "-role", aliases = ["rmRole", "rmrole"])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def removeRole(self, ctx: commands.Context, target: discord.Member = None, role: discord.Role = None):
        await target.remove_roles(role)
        await ctx.send(f"{target.name}에게 {role.name}역할을 제거했습니다")

def setup(client):
    client.add_cog(Manage(client))
