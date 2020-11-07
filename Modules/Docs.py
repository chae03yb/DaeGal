import discord
from discord.ext import commands

import os
import os.path
import asyncio

import Main

class Docs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="Help", aliases=["도움말", "help", "도움"])
    async def Help(self, ctx: commands.Context, Target: str=None):
        Path = "/home/pi/Desktop/Bot/Data/Help/Help"
        if Target is None:
            NoCat = []
            Embed = discord.Embed(
                title="명령어 목록",
                description="`(카테고리)/(명령어)` 형식으로 명령어 확인 가능",
                color=0x7289DA
            )
            for Category in os.listdir(Path):
                if os.path.isdir(f"{Path}/{Category}"):
                    Embed.add_field(name=Category, value=" ".join(os.listdir(f"{Path}/{Category}")))
                else:
                    NoCat.append(Category)

            if bool(NoCat) == True:
                Embed.add_field(name="기타", value=" ".join(NoCat))

            Embed.set_footer(text="기타 도움말: ?help info")
            await ctx.send(embed=Embed)
        else:
            if Target.startswith("..") or Target.startswith("."):
                return
            elif os.path.isdir(f"{Path}/{Target}"):
                Embed = discord.Embed(
                    title="명령어 목록",
                    description=f"카테고리: {Target}",
                    color=0x7289DA
                )
                Embed.add_field(name=Target, value=" ".join(os.listdir(f"{Path}/{Target}")))
                await ctx.send(embed=Embed)
            else:
                with open(f"{Path}/{Target}", "r") as File:
                    Embed = discord.Embed(
                        title=f"{Target} 도움말",
                        description=File.read(),
                        color=0x7289DA
                    )
                    Embed.set_footer(text="기타 도움말: ?help info")
                    await ctx.send(embed=Embed)
    
    @commands.command(name="memo", aliases=["메모"])
    async def memo(self, ctx: commands.Context, TargetMemo=None):
        Embed = discord.Embed(
            title="메모",
            description="📝: 메모 쓰기\n" \
                        "🔍: 메모 보기\n" \
                        "🗑: 메모 삭제\n" \
                        "🗂: 메모 목록"
        )
        msg = await ctx.send(embed=Embed)
        for emoji in ["📝", "🔍", "🗑", "🗂"]:
            await msg.add_reaction(emoji)
        
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)
        
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
        except asyncio.TimeoutError:
            return
        else:
            Path = f"/home/pi/Desktop/Bot/Data/Guild/{ctx.message.guild.id}/Memo"
            if reaction == "📝":
                if reaction.message.guild.id not in os.listdir(Path):
                    os.mkdir(f"{Path}/{reaction.message.guild.id}")

def setup(client):
    client.add_cog(Docs(client))