import os
import sys

from discord.embeds import Embed

import discord
from discord.ext import commands
from discord import utils
import json
import os.path
import asyncio
import SimpleJSON
import time
import datetime
import DaeGal_Utils

import Main

Path = "/home/pi/Desktop/Bot/Data/Guild/"

class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if member.bot == False:
                with open(f"{Path}/{member.guild.id}/Role/DefaultRole.json", "r") as File:
                    await member.add_roles(utils.get(member.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            if member.bot == True:
                with open(f"{Path}/{member.guild.id}/Role/BotRole.json", "r") as File:
                    await member.add_roles(utils.get(member.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
        except FileNotFoundError:
            pass
        try:
            Embed = None
            with open(f"{Path}/{member.guild.id}/Welcome/Message", "r") as File:
                Embed = discord.Embed(
                    color=0x000000,
                    title="환영합니다",
                    description=File.read()
                )
            with open(f"{Path}/{member.guild.id}/Welcome/Channel.json", "r") as File:
                await member.guild.get_channel(json.load(fp=File)["ChannelID"]).send(embed=Embed)
        except FileNotFoundError:
            pass
        
    # @commands.Cog.listener()
    async def on_message(self, ctx):
        return 
        if (ctx.author.bot) or (not ctx.channel.id == 663785408802586645): return 
        if (ctx.content.startswith("섹") or ctx.content.startswith("섻")) and \
           (ctx.content.endswith("스")):
            await PunishMain.warning(ctx=ctx, target=ctx.author, amount=1)
            await ctx.send("자동 경고 부여됨")

    @commands.Cog.listener(name="on_guild_join")
    async def onGuildJoin(self, guild: discord.Guild):
        os.mkdir(f"{Path}/{guild.id}")
        os.mkdir(f"{Path}/{guild.id}/Members")
        os.mkdir(f"{Path}/{guild.id}/Memo")
        os.mkdir(f"{Path}/{guild.id}/Role")
        os.mkdir(f"{Path}/{guild.id}/Welcome")

    @commands.command(name="setPunishRole", aliases=["정지_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setPunishRole(self, ctx: commands.Context, role: discord.Role):
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Role"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Role")
        with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "w") as File:
            Data = { "roleID": role.id }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setDefaultRole", aliases=["기본_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setDefaultRole(self, ctx: commands.Context, role: discord.Role):
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Role"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Role")
        with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "w") as File:
            Data = { "roleID": role.id }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setBotRole", aliases=["봇_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setBotRole(self, ctx: commands.Context, role: discord.Role):
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Role"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Role")
        with open(f"{Path}/{ctx.guild.id}/Role/BotRole.json", "w") as File:
            Data = { "roleID": role.id }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setWelcomeChannel")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setWelcomeChannel(self, ctx: commands.Context, channel:discord.TextChannel=None):
        if channel is None:
            await ctx.send("채널 언급/채널 이름이 필요합니다.")
        else:
            try:
                await ctx.send("환영 메시지를 보낼 채널을 멘션해주십시오")
                async def setChannel(msg: discord.TextChannel):
                    return msg.message.content and msg.message.author == ctx.message.author
                Channel = await self.client.wait_for(event="on_message", timeout=500.0, check=setChannel)
            except asyncio.TimeoutError:
                await ctx.send("시간 초과")
            else:
                try:
                    with open(f"{Path}/{ctx.guild.id}/Welcome/Channel.json") as File:
                        Data = { "ChannelID": Channel.id }
                        json.dump(obj=Data, fp=File, indent=4)
                        await ctx.send("채널 설정 완료")
                except Exception as E:
                    await ctx.send(E)

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
    async def attendance(self, ctx: commands.Context, *, comment=None):
        msg = ctx.message
        if comment is None:
            comment = " "
        else:
            comment = f"\n\n> {comment}"
        
        path = f"/DaeGal/Data/Guild/{ctx.guild.id}/Members/attendanceList.json"
        try:
            if time.strftime(r"%Y-%m-%d", time.localtime()) == SimpleJSON.Read(path)[f"{msg.author.id}"]["lastAttendance"]:
                Embed = discord.Embed(
                    title="이미 출석했습니다",
                    description="하루에 한 번만 출석할 수 있습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
            else:
                Data = SimpleJSON.Read(path)
                Data[f"{msg.author.id}"]["lastAttendance"] = time.strftime(r"%Y-%m-%d", time.localtime())
                Data[f"{msg.author.id}"]["count"] += 1
                SimpleJSON.BackupWrite(path, Data)
                count = str(Data[f"{msg.author.id}"]["count"])
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {count}회 입니다 {comment}",
                    color=DaeGal_Utils.EmbedColors.Green
                )
                await ctx.send(embed=Embed)
        except KeyError:
            Data = SimpleJSON.Read(path)
            DictData = {
                f"{ctx.author.id}": {
                    "count": 1,
                    "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime())
                }
            }
            Data.update(DictData)
            SimpleJSON.BackupWrite(path, Data)
            count = str(Data[f"{msg.author.id}"]["count"])
            Embed = discord.Embed(
                title="✅",
                description=f"현재 {ctx.author}님의 출석 횟수는 {count}회 입니다 {comment}",
                color=DaeGal_Utils.EmbedColors.Green
            )
            await ctx.send(embed=Embed)
        except FileNotFoundError:
            with open(f"/home/pi/Desktop/Bot/Data/Guild/{ctx.guild.id}/Members/attendanceList.json", 'x') as F:
                obj = {
                    f"{ctx.author.id}": {
                        "count": 1,
                        "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime())
                    }
                }
                SimpleJSON.BackupWrite(path, obj)
                count = str(obj[f"{msg.author.id}"]["count"])
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {count}회 입니다 {comment}",
                    color=DaeGal_Utils.EmbedColors.Green
                )
                await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(Guild(client))
