import asyncio
import json
import os
import discord
from discord.ext import commands
from discord.utils import get
import Main
import SimpleJSON
import DaeGal_Utils

Path = "/home/pi/Desktop/Bot/Data/Guild"
ONE_HOUR = 60 * 60

class GuildUser_Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name="kick_", aliases=["추방_"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_(self, ctx: commands.Context, target: discord.Member=None):
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
    
    @commands.command(name="ban_", aliases=["차단_"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_(self, ctx: commands.Context, target: discord.Member=None):
        def check(reaction, user):
            return reaction, user == ctx.message.author and str(reaction.emoji)
        if target is None:
            await ctx.send("대상을 지정해주세요.")
        else:
            Embed = discord.Embed(
                title=f"{target.display_name} 차단",
                description=f"정말로 {target.display_name}을(를) 차단하시겠습니까?",
                color=0xFF0000
            )
            try:
                send = await ctx.send(embed=Embed)
                await self.client.wait_for("message", check=check, timeout=15.0)
                for emoji in ["✔", "❌"]:
                    await send.add_reaction(emoji)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                if check == "✔":
                    await target.ban(reason=f"Banned by {ctx.author.name}")
                    await ctx.send("완료.")
                else:
                    await ctx.send("취소되었습니다.")

    @commands.command(name="cancelpunish_", aliases=["정지취소_"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def cancelPunish_(self, ctx: commands.Context, target: discord.Member, auto:bool=False):
        with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r") as punishRole:
            PunishRole  = json.load(fp=punishRole)["roleID"]
        with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r") as defaultRole:
            DefaultRole = json.load(fp=defaultRole)["roleID"]
        await target.add_roles(get(ctx.guild.roles, id=DefaultRole))
        await target.remove_roles(get(ctx.guild.roles, id=PunishRole))
        if auto == True: await ctx.channel.send("정지가 끝났습니다.")
        elif auto == False: await ctx.channel.send("정지가 취소되었습니다.")

    @commands.command(name="+role_", aliases=["+역할_"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addRole_(self, ctx: commands.Context, target: discord.Member, role: discord.Role=None):
        await target.add_roles(role) # discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
        await ctx.send(f"{target.name}에게 \"{role.name}\" 역할을 추가했습니다.")
    
    @commands.command(name="-role_", aliases=["-역할_"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removeRole_(self, ctx: commands.Context, target: discord.Member, role: discord.Role=None):
        await target.remove_roles(role)
        await ctx.send(f"{target.name}의 \"{role.name}\" 역할을 제거했습니다")

    @commands.group(name="warnings")
    @commands.guild_only()
    async def warnings(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("수행할 작업을 포함해주세요.")               

    @warnings.command(name="view")
    async def view(self, ctx: commands.Context, target: discord.Member=None):
        try:
            if target is None:
                target = ctx.author
            with open(F"{Path}/{ctx.guild.id}/Members/WarningList.json", 'r', encoding="utf-8") as List:
                try:
                    jsonData = json.load(List)
                    userWarningCount = jsonData[str(target.id)]
                    Embed=discord.Embed(
                        title="경고 목록",
                        description=f"사용자: {target}",
                        color=0xFF0000
                        )
                    Embed.add_field(
                        name="경고 횟수",
                        value=userWarningCount
                        )
                    await ctx.send(embed=Embed)
                except KeyError:
                    return await ctx.send("당신은 아직 경고를 받지 않았습니다.")
        except FileNotFoundError:
            return await ctx.send("이 서버에는 아직 경고를 받은 사람이 없습니다.")
    
def setup(client):
    client.add_cog(GuildUser_Test(client))
