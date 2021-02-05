import discord
from discord.ext import commands
import asyncio
import os
import json
import Main

class MailService(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="mail", aliases=["메일"])
    @commands.dm_only()
    @commands.check(Main.isOwner)
    async def mail(self, ctx: commands.Context):
        Path = "/home/pi/Desktop/Bot/Data/Mail"
        Embed = discord.Embed(
            color=0x000000,
            title="메일",
            description="반응을 달아 무슨 작업을 할지 알려주세요."
        )
        Embed.add_field(name="✉️", value="메일 목록", inline=True)
        Embed.add_field(name="📩", value="읽지 않은 메일", inline=True)
        Embed.add_field(name="📨", value="메일 쓰기", inline=True)
        Embed.add_field(name="⚙️", value="설정", inline=True)
        msg = await ctx.send(embed=Embed)

        L = [ "✉️", "📩", "📨", "⚙️" ]
        for emoji in L:
            await msg.add_reaction(emoji)

        def choice(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=300, check=choice)
            del user
        except asyncio.TimeoutError:
            return
        else:
            try:
                with open("/home/pi/Desktop/Bot/Data/User/UserList.json", "r") as File:
                    User = json.load(fp=File, encoding="ascii")[str(ctx.message.author.id)]
                    reaction = str(reaction.emoji)

                    if reaction == "✉️": # 메일 목록
                        Embed = discord.Embed(
                            title="메일 목록",
                            description=" ".join(os.listdir(f"{Path}/{User}")),
                            color=0x000000
                        )
                        await ctx.send(embed=Embed)
                        # str(6) SID : int(18) UID
                    elif reaction == "📩": # 읽지 않은 메일
                        await ctx.send("2")
                    elif reaction == "📨": # 메일 쓰기
                        def SendMail(msg: commands.Context):
                            return msg.message.content

                        try:
                            await self.client.wait_for("message", check=SendMail, timeout=1800)
                        except asyncio.TimeoutError:
                            await ctx.send("시간 초과")
                        else:
                            pass
                    elif reaction == "⚙": # 설정
                        await ctx.send("4")
            except KeyError:
                await ctx.send("등록되지 않은 사용자입니다.")

def setup(client):
    client.add_cog(MailService(client))