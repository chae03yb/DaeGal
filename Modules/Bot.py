import discord
import discord.utils
from discord.ext import commands
import os
import json
import ConsoleColors as CC
import Main
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

    @commands.command(name="notice", aliases=["공지"])
    async def notice(self, ctx:commands.Context, File:str=None):
        if File is None:
            Embed = discord.Embed(
                title="실패",
                description="공지를 보낼 파일을 선택해야 합니다.",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif not File.endswith(".md"):
            Embed = discord.Embed(
                title="실패",
                description="*.md 파일이 필요합니다",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        else:
            with open(f"/DaeGal/Data/Bot/Notice/{File}", "r") as FileIO:
                Embed = discord.Embed(
                    title=FileIO.readline().strip("#"),
                    description=f"```md\n" \
                                f"{FileIO.read()}\n" \
                                f"```",
                    color=0xFFFF33
                )
                with open("/DaeGal/Data/Bot/NoticeChannel.json", "r") as ChannelListFile:
                    ChannelLists: dict = json.load(fp=ChannelListFile)
                    for ChannelID in ChannelLists.values():
                        Channel = discord.utils.get(self.client.get_all_channels(), id=int(ChannelID))
                        await Channel.send(embed=Embed)
                    await ctx.send("성공")
    
    @commands.command(name="curVersion", aliases=["현재-버전"])
    async def getCurrentVersion(self, ctx:commands.Context):
        with open("/DaeGal/Data/Config.json", "r") as ConfigFile:
            Embed = discord.Embed(
                title="현재 버전",
                description=f"현재 버전은 {json.load(fp=ConfigFile)['version']} 입니다.",
                color=0x7777FF
            )
            await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(Bot(client))