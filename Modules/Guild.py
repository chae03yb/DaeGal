import os
import sys

from discord.embeds import Embed

import discord
from discord.ext import commands
from discord import utils
import json
import os.path
import asyncio
import time
import Main
import SimpleJSON

Path = "/DaeGal/Data/Guild/"

class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot == False:
            try:
                with open(f"{Path}/{member.guild.id}/GuildConfig.json", "r") as File:
                    await member.add_roles(utils.get(member.guild.roles, id=json.load(File, encoding="utf-8")["Role"]["MemberRole"]), atomic=True)
            except (FileNotFoundError, KeyError):
                pass
        if member.bot == True:
            try:
                with open(f"{Path}/{member.guild.id}/GuildConfig.json", "r") as File:
                    await member.add_roles(utils.get(member.guild.roles, id=json.load(File, encoding="utf-8")["Role"]["BotRole"]), atomic=True)
            except (FileNotFoundError, KeyError):
                pass

        try:
            Embed = None
            with open(f"{Path}/{member.guild.id}/Welcome/Message", "r") as File:
                Embed = discord.Embed(
                    color=0x000000,
                    title="환영합니다",
                    description=File.read()
                )
            try:
                with open(f"{Path}/{member.guild.id}/GuildConfig.json", "r") as File:
                    await member.guild.get_channel(json.load(fp=File)["Channel"]["WelcomeChannel"]).send(embed=Embed)
            except Exception:
                return
        except FileNotFoundError:
            return

    @commands.Cog.listener(name="on_guild_join")
    async def onGuildJoin(self, guild: discord.Guild):
        os.mkdir(f"{Path}/{guild.id}")
        os.mkdir(f"{Path}/{guild.id}/Members")
        os.mkdir(f"{Path}/{guild.id}/Memo")
        os.mkdir(f"{Path}/{guild.id}/Welcome")

    @commands.command(name="setPunishRole", aliases=["정지_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setPunishRole(self, ctx: commands.Context, role: discord.Role):
        os.makedirs(f"{Path}/{ctx.guild.id}/Role", exist_ok=True)
        with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "w") as File:
            Data = { "Role": {"PunishRole": role.id }}
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setMemberRole", aliases=["멤버_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setDefaultRole(self, ctx: commands.Context, role: discord.Role):
        os.makedirs(f"{Path}/{ctx.guild.id}/Role", exist_ok=True)
        with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "w") as File:
            Data = { "Role": {"MemberRole": role.id }}
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setBotRole", aliases=["봇_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setBotRole(self, ctx: commands.Context, role: discord.Role):
        os.makedirs(f"{Path}/{ctx.guild.id}", exist_ok=True)
        with open(f"{Path}/{ctx.guild.id}/Role/BotRole.json", "w") as File:
            Data = { "Role": {"BotRole": role.id }}
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setWelcomeChannel")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setWelcomeChannel(self, ctx: commands.Context, channel:discord.TextChannel=None):
        if channel is None:
            return await ctx.send("채널 언급/채널 이름이 필요합니다.")
        try:
            os.makedirs(f"{Path}/{ctx.guild.id}", exist_ok=True)
        except Exception as E:
            await ctx.send(E)
        finally:
            try:
                with open(f"{Path}/{ctx.guild.id}/Config.json") as File:
                    Data = { "Channel": { "WelcomeChannel": channel.id }}
                    json.dump(obj=Data, fp=File, indent=4)
                    await ctx.send("채널 설정 완료")
            except Exception as E:
                await ctx.send(E)
    
    # @commands.command(name="setNoticeChannel", aliases=["공지채널_설정"])
    async def setNoticeChannel(self, ctx:commands.Context, channel:discord.TextChannel=None):
        if channel is None:
            Embed = discord.Embed(
                title="오류",
                description="채널이 필요합니다",
                color=0xFF0000
            )
            return await ctx.send(embed=Embed)

        try:
            with open(f"/DaeGal/Data/Bot/NoticeChannel.json", "r") as rFile:
                Data = json.load(fp=rFile)
                with open(f"/DaeGal/Data/Bot/NoticeChannel.json", "w") as wFile:
                    Data.update({f"{ctx.guild.id}": channel.id})
                    json.dump(fp=wFile, obj=Data, indent=4)
                    Embed = discord.Embed(
                        title="성공",
                        description="공지 채널 설정에 성공했습니다",
                        color=0x00FF00
                    )
                    await ctx.send(embed=Embed)
                    
        except Exception as E:
            Embed = discord.Embed(
                title="실패",
                description=f"공지 채널 설정에 실패했습니다\n```사유: {E}```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)

    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clear(self, ctx: commands.Context, reach: int, *, keyword=None):
        try:
            if reach <= 0:
                return await ctx.send("범위는 0보다 큰 정수로 입력해주세요.")
            elif keyword is None:
                await ctx.channel.purge(limit=reach + 1)
            else:
                def check(ctx: commands.Context):
                    if keyword == None:
                        return True
                    else:
                        return ctx.content in str(keyword)
                await ctx.channel.purge(limit=reach + 1, check=check)
        except Exception as E:
            errEmbed = discord.Embed(
                title="오류",
                description=f"{E}",
                color=0xFF0000
            )
            await ctx.send(embed=errEmbed)
    
    @commands.command(name="출석", aliases = ["ㅊㅊ"])
    @commands.guild_only()
    async def attendance(self, ctx: commands.Context, *, comment=None):
        DataPath = f"/DaeGal/Data/Guild/{ctx.guild.id}/Members"
        AttFile = f"{DataPath}/attendanceList.json"
        AttendanceData = {}

        try:
            AttendanceData = SimpleJSON.Read(AttFile)
        except FileNotFoundError:
            SimpleJSON.Write(Path=AttFile, Object={})

        os.makedirs(DataPath, exist_ok=True)
        if comment is not None:
            comment = f"\n\n> {comment}"
        if comment is None:
            comment = ""

        if f"{ctx.author.id}" not in AttendanceData.keys():
            AttendanceData.update({
                f"{ctx.author.id}": {
                    "count": 1,
                    "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime())
                }
            })
            SimpleJSON.Write(Path=AttFile, Object=AttendanceData)
            Embed = discord.Embed(
               title="✅",
               description=f"현재 {ctx.author}님의 출석 횟수는 1회 입니다 {comment}",
               color=0x00FF00
            )
            await ctx.send(embed=Embed)
        else:
            if AttendanceData[f"{ctx.author.id}"]["lastAttendance"] == time.strftime(r"%Y-%m-%d", time.localtime()):
                Embed = discord.Embed(
                    title="이미 출석했습니다",
                    description="하루에 한 번만 출석할 수 있습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
            else:
                AttendanceData[f"{ctx.author.id}"]["count"] += 1
                AttendanceData[f"{ctx.author.id}"]["lastAttendance"] = time.strftime(r"%Y-%m-%d", time.localtime())
                SimpleJSON.Write(Path=AttFile, Object=AttendanceData)
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {AttendanceData[f'{ctx.author.id}']['count']}회 입니다 {comment}",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(Guild(client))
