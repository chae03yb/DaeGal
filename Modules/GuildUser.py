import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import json
import os

import Main
import ConsoleColors as CC

import SimpleJSON
import DaeGal_Utils

Path = "/DaeGal/Data/Guild"
ONE_HOUR = 60 * 60

class GuildUser(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name="kick", aliases=["추방"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, target: discord.Member=None):
        def check(reaction, user):
            return str(reaction.emoji) and user == ctx.author
        if target is None:
            return await ctx.send("대상을 지정해주세요.")
        if target == ctx.author or target.id == 736998050383396996:
            return await ctx.send("봇 또는 스스로를 대상으로 할 수 없습니다.")
        Embed = discord.Embed(
            title=f"{target.display_name} 추방",
            description=f"정말로 {target.display_name}을(를) 추방하시겠습니까?",
            color=0xFF0000
        )
        try:
            send = await ctx.send(embed=Embed)
            for emoji in ["✔", "❌"]:
                await send.add_reaction(emoji)
            reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=15.0)  
        except asyncio.TimeoutError:
            await ctx.send("취소되었습니다.")
        except discord.Forbidden:
            await ctx.send("권한이 부족합니다")
        else:
            if str(reaction.emoji) == "✔":
                await target.kick(reason=f"Kicked by {ctx.author.name}")
                await ctx.send("완료.")
            else:
                await ctx.send("취소되었습니다.")
    
    @commands.command(name="ban", aliases=["차단", "밴"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, target: discord.Member=None):
        def check(reaction, user):
            return str(reaction.emoji) and user == ctx.author
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        elif target == ctx.author or target.id == 736998050383396996:
            return await ctx.send("봇 또는 스스로를 대상으로 할 수 없습니다.")
        else:
            Embed = discord.Embed(
                title=f"{target.display_name} 차단",
                description=f"정말로 {target.display_name}을(를) 차단하시겠습니까?",
                color=0xFF0000
            )
            try:
                send = await ctx.send(embed=Embed)
                for emoji in ["✔", "❌"]:
                    await send.add_reaction(emoji)
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=15.0)  
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                if str(reaction.emoji) == "✔":
                    await target.ban(reason=f"Banned by {ctx.author.name}")
                    await ctx.send("완료.")
                else:
                    await ctx.send("취소되었습니다.")

    @commands.command(name="addRole", aliases=["+역할", "+role"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addRole(self, ctx: commands.Context, target: discord.Member, role: discord.Role=None):
        await target.add_roles(role) # discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
        await ctx.send(f"{target.name}에게 \"{role.name}\" 역할을 추가했습니다.")
    
    @commands.command(name="rmRole", aliases=["-역할", "removeRole", "-role"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removeRole(self, ctx: commands.Context, target: discord.Member, role: discord.Role=None):
        await target.remove_roles(role)
        await ctx.send(f"{target.name}의 \"{role.name}\" 역할을 제거했습니다")

    @commands.command(name="punish", aliases=["정지"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def punish(self, ctx: commands.Context, target: discord.Member=None, time: float=0):
        # return await ctx.send("현재 사용할 수 없습니다.")
        PunishRole  = None
        DefaultRole = None
        if target is None:
            await ctx.send("대상이 필요합니다.")
            return
        if time == 0:
            await ctx.send("정지 시간이 필요합니다.")
            return
        if "PunishRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Role"):
            await ctx.send("정지 역할을 설정해야 합니다.")
            return
        if "DefaultRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Role"):
            await ctx.send("기본 역할을 설정해야 합니다.")
            return
        elif "PunishConfig.json" is os.listdir(F"{Path}/{ctx.guild.id}/"):
            Config = json.load(fp=open(F"{Path}/{ctx.guild.id}/PunishConfig.json", "r"))
        if "DefaultRole.json" not in os.listdir(F"{Path}/{ctx.guild.id}/Role") and "PunishRole.json" not in os.listdir(F"{Path}/{ctx.guild.id}/Roles"):
            return await ctx.send("기본 역할과 정지 역할을 설정하지 않았습니다.")
        else:
            PunishRole  = json.load(fp=open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r"))["roleID"]
            DefaultRole = json.load(fp=open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r"))["roleID"]
            async def Start(ctx: commands.Context):
                await target.add_roles(discord.utils.get(ctx.guild.roles, id=PunishRole))
                await target.remove_roles(discord.utils.get(ctx.guild.roles, id=DefaultRole))
                await asyncio.sleep(time * ONE_HOUR)
                await ctx.send("대상을 정지했습니다.")
            await Start(ctx)
            await asyncio.sleep(time)
            await self.release(ctx=ctx, target=target, auto=True)

    @commands.command(name="release", aliases=["정지취소"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def release(self, ctx: commands.Context, target: discord.Member, auto:bool=False):
        with open(f"{Path}/{ctx.guild.id}/GuildConfig.json", "r") as punishRole:
            PunishRole  = json.load(fp=punishRole)["Role"]["PunishRole"]
        with open(f"{Path}/{ctx.guild.id}/GuildConfig.json", "r") as defaultRole:
            DefaultRole = json.load(fp=defaultRole)["Role"]["MemberRole"]
        await target.add_roles(discord.utils.get(ctx.guild.roles, id=DefaultRole))
        await target.remove_roles(discord.utils.get(ctx.guild.roles, id=PunishRole))
        if auto == True: await ctx.channel.send("정지가 끝났습니다.")
        elif auto == False: await ctx.channel.send("정지가 취소되었습니다.")

    @commands.command(name="warning")
    @commands.guild_only()
    async def warning(self, ctx: commands.Context, target: discord.Member=None, amount: int=1):
        if target is None:
            Embed = discord.Embed(
                title="오류",
                description="대상이 설정되지 않았습니다",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        else:
            wPath = f"{Path}/{ctx.guild.id}/Members/WarningList.json"
            Embed = None
            async def giveWarning():
                with open(wPath, 'r') as WarningListFile:
                    WarningList = json.load(fp=WarningListFile)

                    try:
                        WarningList[str(target.id)] += amount
                    except KeyError:
                        WarningList.update({f"{target.id}":amount})
                        SimpleJSON.Write(wPath, WarningList)

                    try:
                        Config = json.load(fp=open(f"{Path}/{ctx.guild.id}/PunishConfig.json", "r"))

                        WarningLimit      = Config["WarningLimit"]
                        DefaultPunishTime = Config["DefaultPunishTime"]

                        WarningList[str(target.id)] -= WarningLimit
                        if (WarningList[str(target.id)] >= WarningLimit) and Config["AutoPunish"]:
                            await self.punish(ctx=ctx, target=target, time=DefaultPunishTime)
                    except FileNotFoundError:
                        pass
                    except Exception as E:
                        Embed = discord.Embed(
                            title="오류",
                            description=f"```{E}```",
                            color=0xFF0000
                        )
                    else:
                        Embed = discord.Embed(
                            title="성공",
                            description=f"{target.name}에게 경고 {amount} 개를 주었습니다.",
                            color=0x00FF00
                        )
                    finally:
                        await ctx.send(embed=Embed)
            try:
                await giveWarning()
            except FileNotFoundError:
                SimpleJSON.Write(Path=wPath, Object={})
            finally:
                await giveWarning()
     
    @commands.command(name="warninglist")
    async def warninglist(self, ctx: commands.Context, target: discord.Member=None):
        try:
            if target is None:
                target = ctx.author
            with open(F"{Path}/{ctx.guild.id}/Members/WarningList.json", 'r', encoding="utf-8") as List:
                try:
                    jsonData = json.load(List)
                    userWarningCount = jsonData[str(target.id)]
                    Embed=discord.Embed(title="경고 목록", description=f"사용자: {target}", color=0xFF0000)
                    Embed.add_field(name="경고 횟수", value=userWarningCount)
                    await ctx.send(embed=Embed)
                except KeyError:
                    return await ctx.send("당신은 아직 경고를 받지 않았습니다.")
        except FileNotFoundError:
            return await ctx.send("이 서버에는 아직 경고를 받은 사람이 없습니다.")
    
def setup(client):
    client.add_cog(GuildUser(client))
