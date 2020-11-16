# 디스코드
import discord
from discord.ext import commands
from discord import utils

# 파이썬
import os
import asyncio
import json

Path = "/home/pi/Desktop/Bot/Data/Guild"

class GuildUser(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name="kick", aliases=["킥", "추방"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, target: discord.Member=None):
        def check(message):
            return message.content == "Y" and message.channel == ctx.channel
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            await ctx.send("정말로 서버에서 추방하시겠습니까?\n\n\"Y\"로 수락")
            try:
                await self.client.wait_for("message", check=check, timeout=15.0)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                await target.kick(reason=f"Kicked by {ctx.author.name}")
                await ctx.send("완료.")
    
    @commands.command(name="ban", aliases=["밴", "차단"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, target: discord.Member=None):
        def check(reaction, user):
            return reaction, user == ctx.message.author and str(reaction.emoji)
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            Embed = discord.Embed(
                title=f"{target.display_name} 추방",
                description=f"정말로 {target.display_name}을(를) 추방하시겠습니까?",
                color=0xFF0000
            )
            try:
                send = await ctx.send(embed=Embed)
                await self.client.wait_for("message", check=check, timeout=15.0)
                await send.add_reaction("✔")
                await send.add_reaction("❌")
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                if check == "✔":
                    await target.ban(reason=f"Banned by {ctx.author.name}")
                    await ctx.send("완료.")
                else:
                    await ctx.send("취소되었습니다.")

    @commands.command(name="punish", aliases=["징벌"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def punish(self, ctx: commands.Context, target: discord.Member=None, Time: int=0):
        if target is None:
            await ctx.send("대상이 필요합니다.")
            return
        if Time == 0:
            await ctx.send("징벌 시간이 필요합니다.")
            return
        if "PunishRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Role"):
            await ctx.send("징벌자 역할을 설정해야 합니다.")
            return
        if "DefaultRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Role"):
            await ctx.send("기본 역할을 설정해야 합니다.")
            return
        else:
            with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r") as File:
                await target.add_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r") as File:
                await target.remove_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            await ctx.send("대상을 징벌했습니다.")

            await asyncio.sleep(Time * (60 * 60))

            with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r") as File:
                await target.remove_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r") as File:
                await target.add_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            await ctx.send(f"{target.mention} 징벌이 끝났습니다.")
            
    @commands.command(name="+role", aliases=["addRole", "addrole", "+역할"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addRole(self, ctx: commands.Context, target: discord.Member=None, role: discord.Role=None):
        await target.add_roles(role)
        await ctx.send(f"{target.name}에게 \"{role.name}\" 역할을 추가했습니다.")
    
    @commands.command(name="-role", aliases=["rmRole", "rmrole", "-역할"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removeRole(self, ctx: commands.Context, target: discord.Member=None, role: discord.Role=None):
        await target.remove_roles(role)
        await ctx.send(f"{target.name}에게 \"{role.name}\" 역할을 제거했습니다")
    
    @commands.command(name="warning", aliases=["경고"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def warning(self, ctx, target: discord.Member=None, amount: int=None):
        if target is None:
            await ctx.send("대상을 입력해주세요.")
        elif amount is None:
            amount = 1
        elif type(amount) != int:
            await ctx.send("부여할 경고의 개수를 정수로 입력해주세요.")
        elif target.bot:
            await ctx.send("봇에게는 경고를 부여할 수 없습니다.")
        try:
            with open(F"/home/pi/Desktop/Bot/Data/Guild/{ctx.guild.id}/Warnings.json", "r", encoding = "utf-8") as File:
                Data = json.load(File)
                try:
                    targetWarningCount = Data["warnings"][target.id]
                    with open(F"/home/pi/Desktop/Bot/Data/Guild/{ctx.guild.id}/GuildConfig.json", "r", encoding = "utf-8") as File2:
                        try:
                            Data2 = json.load(File2)
                            if targetWarningCount >= Data2["WarningLimit"]:
                                targetWarningCount -= Data2["WarningLimit"]
                                punishTime = Data2["DefaultPunishTime"]
                                await GuildUser.punish(self = self, ctx = ctx, target = target, Time = punishTime)
                        except Exception as E:
                            await ctx.send(f"E: {E}")
                except KeyError:
                    Data = json.load(File)
                    loadData = {target.id: amount}
                    temp = Data["warnings"]
                    temp.append(loadData)
                    with open(F"/home/pi/Desktop/Bot/Data/Guild/{ctx.guild.id}/Warnings.json", "w", encoding = "utf-8") as File:
                        pass
                        json.dump(obj = loadData, fp = File, indent = 4)
        except FileNotFoundError:
            with open(F"/home/pi/Desktop/Bot/Data/Guild/{ctx.guild.id}/Warnings.json", "x", encoding = "utf-8") as File:
                try:
                    loadData = {"warnings": {target.id: amount}}
                    json.dump(obj = Data, fp = File, indent = 4)
                except Exception as E:
                    await ctx.send(F"E: {E}")
                else:
                    await ctx.send(f"{target.id}에게 경고를 줬습니다.")

def setup(client):
    client.add_cog(GuildUser(client))
