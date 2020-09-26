import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="help")
    async def Help(self, ctx: commands.Context, cmd=None):
        if cmd is None:
            Embed = discord.Embed(
                title="대갈 도움말",
                description="세부 도움말 확인: `?help [명령어]`",
                color=0x000000
            )
            Embed.add_field(name="봇", value="`핑` | `초대`", inline=True)
            Embed.add_field(name="서버관리", value="", inline=True)
        if cmd == "": pass