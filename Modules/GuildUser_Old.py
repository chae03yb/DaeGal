import asyncio
import json
import os
import discord
from discord import utils
from discord.ext import commands

Path = "/home/pi/Desktop/Bot/Data/Guild"
ONE_HOUR = 60 * 60

class GuildUser_Old(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name="kick", aliases=["추방"])
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
    
    @commands.command(name="ban", aliases=["차단"])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, target: discord.Member=None):
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

    @commands.command(name="punish", aliases=["정지"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def punish(self, ctx: commands.Context, target: discord.Member=None, time: float=0):
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
        else:
            with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r") as File:
                await target.add_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r") as File:
                await target.remove_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            await ctx.send("대상을 정지했습니다.")

            await asyncio.sleep(time * ONE_HOUR)

            with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r") as File:
                await target.remove_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r") as File:
                await target.add_roles(utils.get(ctx.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            await ctx.send(f"{target.mention} 정지가 끝났습니다.")
            
    @commands.command(name="+role", aliases=["+역할"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addRole(self, ctx: commands.Context, target: discord.Member=None, role: discord.Role=None):
        await target.add_roles(role)
        await ctx.send(f"{target.name}에게 \"{role.name}\" 역할을 추가했습니다.")
    
    @commands.command(name="-role", aliases=["-역할"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removeRole(self, ctx: commands.Context, target: discord.Member=None, role: discord.Role=None):
        await target.remove_roles(role)
        await ctx.send(f"{target.name}의 \"{role.name}\" 역할을 제거했습니다")
    
    @commands.command(name="warning", aliases=["경고"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def warning(self, ctx: commands.Context, target: discord.Member=None, amount: int=1):
        if target is None:
            return await ctx.send("대상이 필요합니다.")
        if "Members" not in os.listdir(f"{Path}/{ctx.guild.id}/"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Members/")

        PunishRole  = None 
        DefaultRole = None
        Config      = None

        if "PunishConfig.json" in os.listdir(f"{Path}/{ctx.guild.id}/"):
            Config = json.load(fp=open(f"{Path}/{ctx.guild.id}/PunishConfig.json", "r"))
        if "DefaultRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Role") and "PunishRole.json" not in os.listdir(f"{Path}/{ctx.guild.id}/Roles"):
            return await ctx.send("기본 역할과 정지 역할을 설정하지 않았습니다.")
        else:
            PunishRole  = json.load(fp=open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "r"))["roleID"]
            DefaultRole = json.load(fp=open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "r"))["roleID"]

        jsonData = {}
        try:
            jsonData.update(json.load(fp=open(f"{Path}/{ctx.guild.id}/Members/WarningList.json", "r")))
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
"""   
        if "PunishConfig.json" in os.listdir(f"{Path}/{ctx.guild.id}/") and Config["AutoPunish"] and \
            jsonData[str(target.id)] <= Config["WarningLimit"]:
                await target.add_roles(get(ctx.guild.roles, id=PunishRole))
                await target.remove_roles(get(ctx.guild.roles, id=DefaultRole))
                Embed.set_footer(text="자동으로 정지됐습니다.")

                def cancelCheck(msg):
                    return msg.author == ctx.author and msg.content in ["?cancelPunish", "?징벌취소"]
                async def endPunish():
                    await target.remove_roles(get(ctx.guild.roles, id=PunishRole))
                    await target.add_roles(get(ctx.guild.roles, id=DefaultRole))
                try:
                    cancel = await self.client.wait_for("message", check=cancelCheck, timeout=Config)
                except asyncio.TimeoutError:
                    await endPunish()
                    await ctx.send("정지가 끝났습니다.")
                else:
                    await endPunish()
                    await ctx.send("정지가 취소되었습니다.")
"""

def setup(client):
    client.add_cog(GuildUser_Old(client))
