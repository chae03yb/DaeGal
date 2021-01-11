import asyncio
import json
import os
import discord
from discord.ext import commands
from discord.utils import get
import Main

Path = "/home/pi/Desktop/Bot/Data/Guild"
ONE_HOUR = 60 * 60

class GuildUser_Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name="kick_", aliases=["추방_"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_(self, ctx: commands.Context, *targets):
        def check(message):
            return message.content == "Y" and message.channel == ctx.channel
        try:
            targets[0]
        except IndexError:
            await ctx.send("추방할 대상을 지정해주세요")
        else:
            targetlist = list(targets)
            await ctx.send("정말로 서버에서 추방하시겠습니까?\n\n\"Y\"로 수락")
            try:
                await self.client.wait_for("message", check=check, timeout=15.0)
            except asyncio.TimeoutError:
                await ctx.send("취소되었습니다.")
            else:
                for Num in targetlist:
                    await targets[Num].kick(reason=f"Kicked by {ctx.author.name}")
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

    @commands.command(name="punish_", aliases=["정지_"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def punish_(self, ctx: commands.Context, target: discord.Member=None, time: float=0):
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
                await target.add_roles(get(ctx.guild.roles, id=PunishRole))
                await target.remove_roles(get(ctx.guild.roles, id=DefaultRole))
                await asyncio.sleep(time * ONE_HOUR)
                await ctx.send("대상을 정지했습니다.")
            await Start(ctx)
            await asyncio.sleep(time)
            await self.cancelPunish_(ctx=ctx, target=target, auto=True)

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

    @warnings.command(name="warning_", aliases=["경고_"])
    @commands.has_permissions(administrator=True)
    async def warning_(self, ctx: commands.Context, target: discord.Member=None, amount: int=1):
        if target is None:
            return await ctx.send("대상이 필요합니다.")
        if "Members" not in os.listdir(f"{Path}/{ctx.guild.id}/"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Members/")

        Config      = None

        if "PunishConfig.json" in os.listdir(f"{Path}/{ctx.guild.id}/"):
            Config = json.load(fp=open(f"{Path}/{ctx.guild.id}/PunishConfig.json", "r"))
        if "DefaultRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Role") and "PunishRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Roles"):
            return await ctx.send("기본 역할과 정지 역할을 설정하지 않았습니다.")
        jsonData = {}
        try:
            with open(f"{Path}/{ctx.guild.id}/Members/WarningList.json", "r") as warningList:
                jsonData.update(json.load(fp=warningList))
        except json.JSONDecodeError:
            pass
        except FileNotFoundError:
            open(f"{Path}/{ctx.guild.id}/Members/WarningList.json", "w").close()

        with open(f"{Path}/{ctx.guild.id}/Members/WarningList.json", "w") as File:
            try:
                jsonData[str(target.id)]
            except KeyError:
                jsonData.update({ str(target.id): 0 })
            finally:
                jsonData[str(target.id)] += amount
                json.dump(fp=File, obj=jsonData, indent=4)

        Embed = discord.Embed(
            title="성공",
            description=f"현재 누적 경고: {str(jsonData[str(target.id)])}",
            color=0xFF3333
        )
        await ctx.send(embed=Embed)
        
        if "PunishConfig.json" in os.listdir(f"{Path}/{ctx.guild.id}/") and Config["AutoPunish"] and (jsonData[str(target.id)] <= Config["WarningLimit"]):
            with open(f"/home/pi/Desktop/Bot/Data/Guild/{ctx.guild.id}/PunishConfig.json", "r") as DefaultPunishTime:
                Time = json.load(fp=DefaultPunishTime)["DefaultPunishTime"]
                await self.punish_(ctx=ctx, target=target, time=Time)
    
    @warnings.command(name="view")
    async def view(self, ctx: commands.Context, target: discord.Member=None):
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
    client.add_cog(GuildUser_Test(client))
