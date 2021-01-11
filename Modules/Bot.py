import discord
from discord import activity
from discord.ext import commands
import os
import json
import ConsoleColors as CC
import Main
#from Log import writeLog

from discord_slash import SlashContext, SlashCommand

Path = "/home/pi/Desktop/Bot/Data/Guild"
PresenceCount = 0

class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.ChangePresence.start()

    @commands.command(name="ping", aliases=["핑"])
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"pong! `{int(self.client.latency * 1000)}ms`")
    
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
            await ctx.send(f"E: {E}")

    # @commands.command(name="setPrefix", aliases=["접두사_설정"])
    async def setPrefix(self, ctx: commands.Context, prefix='?'):
        try:
            with open(f"{Path}/{ctx.guild.id}/GuildConfig.json", "r+") as File:
                json.dump(obj={ "Prefix": prefix }.update(json.load(fp=File)), fp=File, indent=4)
                await ctx.send("설정 성공.")
        except Exception as E:
            await ctx.send(
                f"설정 실패.\n"\
                f"사유: {E}"
            )

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game("help: ?help"))

    @commands.command(name="changePresence")
    async def changePresence(self, ctx:commands.Context, activity=None):
        await self.client.change_presence(activity=discord.Game(activity))
        await ctx.send("상태 메시지를 변경했습니다")
    
    # @commands.command(name="addStatus", aliases=["+Status", "+status", "상태추가", "+상태"])
    async def addStatus(self, ctx: commands.Context, status=None):
        if status is None:
            return await ctx.send("상태 메시지를 같이 입력해주십시오.")
        with open("/home/pi/Desktop/Bot/Data/Bot/Presence", "a") as File:
            File.write(status+"\n")
            await ctx.send("완료")

    @commands.command(name="eval")
    @commands.check(Main.isOwner)
    async def Eval(self, ctx:commands.Context, *statement):
        await ctx.send(eval(" ".join(statement)))
"""
    @commands.command(name="onrdtst")
    @commands.check(Main.isOwner)
    async def on_ready_test(self, ctx: commands.Context):
        jsonData = {}
        with open(f"/home/pi/Desktop/Bot/Data/Init.json", "w") as InitFile:
            try:
                Data = json.load(fp=InitFile)["loginCount"]
                jsonData.update({"loginCount": Data})
                writeLog(f"Logged in as {self.client.user}")
            except KeyError:
                jsonData.update({"loginCount": 0})
            except Exception as E:
                await ctx.send(E)
            finally:
                jsonData["loginCount"] += 1
                json.dump(fp=InitFile, obj=jsonData, indent=4)
"""
def setup(client):
    client.add_cog(Bot(client))