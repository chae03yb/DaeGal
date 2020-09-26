import discord
from discord.ext import commands

import json
import pickle

class ManageServer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "setPunishRole", aliases=["징벌자역할설정"])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setPunishRole(self, ctx: commands.Context, role: discord.Role):
        with open(f"/home/pi/Desktop/Bot/Data/Role/PunishRole/{ctx.guild.id}.p", "wb") as File:
            pickle.dump(file=File, obj=role)
            await ctx.send("설정 완료")
    
    @commands.command(name = "setDefaultRole", aliases=["기본역할설정"])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setDefaultRole(self, ctx: commands.Context, role: discord.Role):
        with open(f"/home/pi/Desktop/Bot/Data/Role/DefaultRole/{ctx.guild.id}.p", "wb") as File:
            pickle.dump(file=File, obj=role)
            await ctx.send("설정 완료.")
    
    @commands.command(name = "setBotRole", aliases=["봇역할설정"])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setBotRole(self, ctx: commands.Context, role: discord.Role):
        with open(f"/home/pi/Desktop/Bot/Data/Role/BotRole/{ctx.guild.id}.p", "wb") as File:
            pickle.dump(file=File, obj=role)
            await ctx.send("설정 완료.")
    
    @commands.command(name = "setWelcomeMessage", aliases=["환영메시지설정"])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setWelcomeMessage(self, ctx: commands.Context, message = None):
        if message is None:
            await ctx.send("환영 메세지의 내용을 입력해주세요.")
        else:
            with open(f"/home/pi/DesktopBot/Data/GuildData/WelcomMessage/{ctx.guild.id}.txt", "w") as File:
                File.write(message)
                await ctx.send("설정 완료.")

    # @commands.command(name="createChannel", aliases=["채널생성", "+채널", "+channel"])
    # async def createChannel(self, ctx: commands.Context, channelName=None, )
    
    """
    @commands.command(name = "setWarnLimit")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def setWarnLimit(self, ctx: commands.Context, limit: int = None, autoPunish: bool = False):
        """
    
def setup(client):
    client.add_cog(ManageServer(client))