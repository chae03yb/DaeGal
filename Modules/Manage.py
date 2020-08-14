# 디스코드
import discord
from discord.ext import commands
from discord.utils import get

# 파이썬
import os
import asyncio
import pickle

"""GetSetRoles, Punish 함수 수정 필요"""

def GetSetRoles(ctx):
    os.chdir("/home/pi/Desktop/Bot/Data/Manage")
    with open(f"{ctx.guild.id}_SetRoles.setting", "rb") as ReadRoleSetting:
        Purged = pickle.load(ReadRoleSetting)
        Default = pickle.load(ReadRoleSetting)
        Admin = pickle.load(ReadRoleSetting)
        (yield Purged)
        (yield Default)
        (yield Admin)
        os.chdir("/home/pi/Desktop/Bot")

class Manage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "setroles")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def SetRoles(self, ctx, PurgedRole : str, DefaultRole : str, AdminRole : str):
        Purged = PurgedRole
        Default = DefaultRole
        Admin = AdminRole
        os.chdir("/home/pi/Desktop/Bot/Data/Manage")
        with open(f"{ctx.guild.id}_SetRoles.setting", "wb") as WriteRoleSetting:
            pickle.dump(Purged, WriteRoleSetting)
            pickle.dump(Default, WriteRoleSetting)
            pickle.dump(Admin, WriteRoleSetting)
            await ctx.channel.send("역할이 설정되었습니다.")
            os.chdir("/home/pi/Desktop/Bot")
    
    @commands.command(name = "add")
    @commands.has_permissions(administrator = True)
    async def AddRole(self, ctx, Member : discord.Member, *, Role : str):
        r"""멤버에게 역할을 추가합니다. 대상은 멘션 또는 대상의 이름으로 지정할 수 있으며, 역할은 이름으로만 지정할 수 있습니다."""
        await Member.add_roles(get(ctx.guild.roles, name = f"{Role}"))
        await ctx.send()
    
    @commands.command(name = "remove")
    @commands.has_permissions(administrator = True)
    async def RemoveRole(self, ctx, Member : discord.Member, *, Role : str):
        r"""멤버의 역할을 제거합니다. AddRole함수와 마찬가지로 대상은 멘션 또는 대상의 이름으로 지정할 수 있으며, 역할은 이름으로만 지정할 수 있습니다."""
        await Member.remove_roles(get(ctx.guild.roles, name = f"{Role}"))
        await ctx.send()
    
    @commands.command(name = "punish", aliases = ["purge"])
    @commands.has_permissions(administrator = True)
    async def Punish(self, ctx, Member : discord.Member, Time : int):
        r"""멤버에게 징벌을 내립니다. 대상은 멘션 또는 대상의 이름으로 지정할 수 있으며, 징벌 시간은 216000초(1시간) * 시간 입니다."""
        GetMemberRoles = discord.utils.get(Member.roles)
        PunishTime = Time * 216000
        G = GetSetRoles(ctx)
        next(G)
        next(G)
        next(G)
        if GetMemberRoles in Default:
            Role1name = Default
        elif GetMemberRoles in Admin:
            Role1name = Admin
        else:
            return 0

        try:
            async def PunishFunc(ctx, Role1, Role2):
                await Member.remove_roles(get(ctx.guild.roles, name = Role1))
                await Member.add_roles(get(ctx.guild.roles, name = Role2))
            
            await PunishFunc(ctx, Role1name, Role2name)
            await asyncio.sleep(PunishTime)
            await PunishFunc(ctx, Role2name, Role1name)
        except Exception as E:
            await ctx.channel.send(f"E: {E}")

    @commands.command(name = "kick")
    @commands.has_permissions(administrator = True)
    async def Kick(self, ctx, Member : discord.Member, *, reason = None):
        try:
            await ctx.guild.kick()
            await ctx.channel.send(f"{Member}님을 추방했습니다.")
        except Exception as E:
            await ctx.send(f"E: {E}")

def setup(client):
    client.add_cog(Manage(client))