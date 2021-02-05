import discord
from discord import activity
from discord.ext import commands
import os
import json
import ConsoleColors as CC
import Main
import SimpleJSON
#from Log import writeLog

Path = "/DaeGal/Data/Guild"
PresenceCount = 0

class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.ChangePresence.start()

    @commands.command(name="ping", aliases=["핑"])
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"pong! `{int(self.client.latency * 1000)}ms`")

    @commands.command(name="statusCheck")
    async def statusCheck(self, ctx:commands.Context):
        await ctx.send("Main bot is online!")
    
    @commands.command(name="invite", aliases=["초대"])
    async def Invite(self, ctx: commands.Context):
        Embed = discord.Embed(title="봇 초대 링크", url=\
            r"https://discord.com/api/oauth2/authorize?client_id=736998050383396996&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D736998050383396996%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D736998&scope=bot")
        await ctx.send(embed=Embed)

    @commands.command(name="sleep")
    @commands.check(Main.isOwner)
    async def sleep(self, ctx: commands.Context):
        try:
            await ctx.send("종료중...")
            await self.client.logout()
            print("--------------------------------------------------")
            print(f"Terminated by {CC.EFCT.REVERSE_PHASE} {ctx.author.name} {CC.EFCT.CLEAR}")
            os._exit(0)
        except Exception as E:
            errEmbed = discord.Embed(
                title="오류",
                description=f"{E}",
                color=0xFF0000
                )
            await ctx.send(embed=errEmbed)

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game("help: ?help"))

    @commands.command(name="changePresence")
    @commands.check(Main.isOwner)
    async def changePresence(self, ctx:commands.Context, activity=None):
        await self.client.change_presence(activity=discord.Game(activity))
        embed = discord.Embed(
            title="성공",
            description="상태 메시지를 변경했습니다",
            color=0x30e330
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Bot(client))