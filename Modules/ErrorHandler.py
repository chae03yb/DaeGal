# 디스코드
import discord
from discord.ext import commands
from discord import utils

import json
import os

# 기타
import ConsoleColors as CC

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"`{int(error.retry_after / 60000)}`분 후에 다시 사용해주세요.")
        elif isinstance(error, discord.NotFound) or isinstance(error, discord.errors.Forbidden):
            await ctx.send("봇 역할의 위치가 대상 역할의 위치보다 아래에 있습니다.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("인수가 필요합니다.")
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.send("이 명령어는 DM에서만 가능합니다.")
        elif isinstance(error, AttributeError):
            await ctx.send(f"AttributeError: {error}")
        else:
            print(f"{CC.BG.RED} E: {error} {CC.EFCT.CLEAR}")

def setup(client):
    client.add_cog(ErrorHandler(client))