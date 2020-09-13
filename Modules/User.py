from discord.ext import commands
import discord

import sqlite3
import os

class User(commands.Cog, name="유저"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="소개변경", aliases=["introduce"])
    async def setProfile(self, ctx, *Description):
        """
        ?소개변경|introduce <소개>
            -h    도움말을 표시합니다.
            -r    소개를 제거합니다.
        """
        if Description is None:
            await ctx.send("소개가 필요합니다.")
        if "-h" in Description and len(Description) == 1:
            await ctx.send("`?소개 변경 <소개>`")
        elif "-r" in Description and len(Description) == 1:
            with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "w") as File:
                File.write(" ")
                await ctx.send("소개를 제거했습니다.")
        else:
            with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "w") as File:
                File.write(" ".join(Description))
                await ctx.send("소개를 변경했습니다.")
    
    @commands.command(name="프로필", aliases=["profile"])
    async def profile(self, ctx, target: discord.User=None):
        """
        ?프로필|profile (대상)
        """
        try:
            """if target.bot:
                await ctx.send("봇은 프로필을 생성할 수 없습니다.")"""
            if target is None:
                with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "r") as File:
                    Embed = discord.Embed(title = f"{ctx.author.name}님의 프로필", description = File.read())
                    Embed.set_thumbnail(url = ctx.author.avatar_url)
                    await ctx.send(embed = Embed)
            else:
                with open(f"/home/pi/Desktop/Bot/Data/Profile/{target.id}.txt", "r") as File:
                    Embed = discord.Embed(title = f"{target.name}님의 프로필", description = File.read())
                    Embed.set_thumbnail(url = target.avatar_url)
                    await ctx.send(embed = Embed)

        except FileNotFoundError:
            with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "w") as File:
                await ctx.send("프로필이 생성되었습니다.")

    @commands.command(name="+customCommand")
    async def customCommand(self, ctx: commands.Context, command=None, do=None):
        if command or do is None:
            await ctx.send("명령어 이름과 동작을 설정해주세요.")
        else:
            pass

    # @commands.Cog.listener(name="on_message")
    # async def on_message(self, ctx: commands.Context):
        # con = sqlite3.connect("/home/pi/Desktop/Bot/Data/Keywords/KeywordData.sqlite3")
        # cur = con.cursor()

        # cur.execute(f"select * from {ctx.author.guild};")

        # SELECT name FROM sqlite_master WHERE type = 'table';

def setup(client):
    client.add_cog(User(client))
