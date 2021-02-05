import discord
from discord.ext import commands
from discord.ext.commands.core import command

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error:discord.errors):
        if isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            Embed = discord.Embed(
                title="오류",
                description=f"````{int(error.retry_after / 60000)}`분 후에 다시 사용해주세요```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, discord.errors.Forbidden):
            Embed = discord.Embed(
                title="오류",
                description=f"```봇 역할의 위치가 대상 역할의 위치보다 아래에 있습니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            Embed = discord.Embed(
                title="오류",
                description=f"```인수가 필요합니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            Embed = discord.Embed(
                title="오류",
                description=f"```이 명령어는 DM에서만 가능합니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, commands.errors.CheckFailure):
            Embed = discord.Embed(
                title="오류",
                description=f"```권한이 부족합니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, commands.UserNotFound):
            Embed = discord.Embed(
                title="오류",
                description=f"```존재하지 않는 유저입니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, commands.MemberNotFound):
            Embed = discord.Embed(
                title="오류",
                description=f"```존재하지 않는 유저입니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, commands.RoleNotFound):
            Embed = discord.Embed(
                title="오류",
                description=f"```존재하지 않는 역할입니다.```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        elif isinstance(error, discord.errors.NotFound):
            Embed = discord.Embed(
                title="오류",
                description=f"```대상이 존재하지 않습니다```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        else:
            Embed = discord.Embed(
                title="오류",
                description=f"```{str(error)}```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
            # await ctx.send(f"E: {error}")

def setup(client):
    client.add_cog(ErrorHandler(client))