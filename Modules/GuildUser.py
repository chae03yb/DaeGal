import asyncio
import json
import os
import discord
from discord.ext import commands
from discord.utils import get
import Main

Path = "/home/pi/Desktop/Bot/Data/Guild"
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
    
def setup(client):
    client.add_cog(GuildUser(client))
