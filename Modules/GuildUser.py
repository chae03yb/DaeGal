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
        except discord.errors.Forbidden:
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
    async def punish(self, ctx:commands.Context, target:discord.Member=None, time:float=0):
        if target is None:
            return await ctx.send(embed=discord.Embed(
                title="오류",
                description="대상이 필요합니다",
                color=0xFF0000
            ))
        elif time <= 0:
            return await ctx.send(embed=discord.Embed(
                title="오류",
                description="올바른 시간을 설정해주세요",
                color=0xFF0000
            ))
        else:
            try:
                SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")["Role"]["Punish"]
                SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")["Role"]["Member"]
            except FileNotFoundError:
                return await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="역할을 설정해야 합니다",
                    color=0xFF0000
                ))
            except KeyError:
                return await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="필요한 역할중 하나가 설정되지 않았습니다",
                    color=0xFF0000
                ) \
                .add_field(name="필요한 역할 목록", value="`정지` 역할, `멤버` 역할"))
            else:
                PunishRole: int = SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")["Role"]["Punish"]
                MemberRole: int = SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")["Role"]["Member"]

                async def Start(ctx:commands.Context):
                    await target.add_roles(discord.utils.get(ctx.guild.roles, id=PunishRole))
                    await target.remove_roles(discord.utils.get(ctx.guild.roles, id=MemberRole))
                    await ctx.send(embed=discord.Embed(
                        description=f"{time} 시간동안 유저를 정지합니다",
                        color=0xFF0000
                    ))
                    await asyncio.sleep(time * ONE_HOUR)

                await Start(ctx)
                await asyncio.sleep(time)
                await self.release(ctx=ctx, target=target, auto=True)

    @commands.command(name="release", aliases=["정지취소"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def release(self, ctx: commands.Context, target: discord.Member, auto:bool=False):
        guildconfig: str = SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")
        punishrole: int  = guildconfig["Role"]["Punish"]
        memberrole: int  = guildconfig["Role"]["Member"]

        await target.add_roles(discord.utils.get(ctx.guild.roles, id=memberrole))
        await target.remove_roles(discord.utils.get(ctx.guild.roles, id=punishrole))

        await ctx.send(embed=discord.Embed(
            title="알림",
            description="정지가 끝났습니다",
            color=0x00FF00
        ))

    @commands.command(name="warning", aliases=["경고"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def warning(self, ctx:commands.Context, target:discord.Member=None, amount:int=1, *, reason:str=None):
        wpath: str = f"{Path}/{ctx.guild.id}/Members/WarningList.json"

        if target is None:
            Embed = discord.Embed(
                title="오류",
                description="대상이 설정되지 않았습니다",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        else:
            wdata: dict = None
            try:
                wdata = SimpleJSON.Read(wpath)
                if f"{target.id}" not in wdata.keys():
                    wdata.update({ f"{target.id}": 0 })
                    SimpleJSON.Write(Path=wpath, Object=wdata)
            except FileNotFoundError:
                SimpleJSON.Write(wpath, { f"{target.id}": 0 })
            except Exception as E:
                await ctx.send(embed=discord.Embed(
                    title="오류",
                    description=f"```E: {E}```",
                    color=0xFF0000
                ))
            finally:
                wdata = SimpleJSON.Read(wpath)
                wdata[f"{target.id}"] += amount
                SimpleJSON.Write(Path=wpath, Object=wdata)

                Embed: discord.Embed = None

                if reason is None: Embed = discord.Embed( title="성공", color=0xFF0000 ) \
                    .set_footer(text=f"현재 경고 횟수: {wdata[f'{target.id}']}회")
                else:               Embed = discord.Embed( title="성공", color=0xFF0000, description=f"경고 사유: {reason}" ) \
                    .set_footer(text=f"현재 경고 횟수: {wdata[f'{target.id}']}회")

                Embed.add_field(name="대상", value=target.mention)

                await ctx.message.delete()
                await ctx.send(embed=Embed)
     
    @commands.command(name="warninglist", aliases=["wl"])
    @commands.guild_only()
    async def warninglist(self, ctx: commands.Context, target: discord.Member=None):
        try:
            if target is None: target = ctx.author
            try:
                warncount = SimpleJSON.Read(f"{Path}/{ctx.guild.id}/Members/WarningList.json")[f"{target.id}"]
                Embed = discord.Embed(
                    title="경고 목록", 
                    description=f"사용자: {target}", 
                    color=0xFF0000
                ) \
                .add_field(name="경고 횟수", value=warncount)
                await ctx.send(embed=Embed)
            except KeyError:
                return await ctx.send(embed=discord.Embed(
                    description="당신은 아직 경고를 받지 않았습니다",
                    color=0x00FF00
                ))
        except FileNotFoundError:
            return await ctx.send(embed=discord.Embed(
                description="이 서버에 경고를 받은 사용자가 없습니다",
                color=0x00FF00
            ))
    
def setup(client):
    client.add_cog(GuildUser(client))
