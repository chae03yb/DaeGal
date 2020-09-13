# 디스코드
import discord
from discord.ext import commands

import asyncio
import os

class Bot(commands.Cog, name="봇"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping", aliases=["핑"])
    async def ping(self, ctx):
        await ctx.send(f"pong! `{int(self.client.latency * 1000)}ms`")
    
    @commands.command(name = "invite", aliases = ["초대"])
    async def Invite(self, ctx):
        Embed = discord.Embed(title="초대 링크", url=\
            "https://discord.com/api/oauth2/authorize?client_id=736998050383396996&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D736998050383396996%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D736998&scope=bot")
        await ctx.send(embed=Embed)

    @commands.command(name="logout", hidden=True)
    @commands.is_owner()
    async def Logout(self, ctx):
        try:
            await ctx.send("종료중...")
            await self.client.logout()
            print(f"Terminated by {ctx.author.name}")
            os._exit(0)
        except Exception as E:
            await ctx.send(f"E: {E}")
    """
    @commands.command(name="help", aliases=["도움", "도움말"])
    async def Help(self, ctx: commands.Context, com=None):
    """    

def setup(client):
    client.add_cog(Bot(client))