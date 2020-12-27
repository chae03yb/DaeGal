import sqlite3
import discord
from discord.ext import commands

import json

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="프로필수정", aliases=["EditProfile"])
    async def setProfile(self, ctx, *Description):
        if Description is None:
            await ctx.send("소개가 필요합니다.")
        elif "-r" in Description and len(Description) == 1:
            with open(f"/home/pi/Desktop/Bot/Data/User/Profile/{ctx.author.id}.txt", "w") as File:
                File.write(" ")
                await ctx.send("소개를 제거했습니다.")
        else:
            with open(f"/home/pi/Desktop/Bot/Data/User/Profile/{ctx.author.id}.txt", "w") as File:
                File.write(" ".join(Description))
                await ctx.send("소개를 변경했습니다.")
    
    @commands.command(name="프로필", aliases=["profile"])
    async def profile(self, ctx, target: discord.User=None):
        if target is None:
            target = ctx.author
        try:
            if target is None:
                with open(f"/home/pi/Desktop/Bot/Data/User/Profile/{ctx.author.id}.txt", "r") as File:
                    Embed = discord.Embed(
                        title=f"{ctx.author.name}님의 프로필",
                        description=File.read()
                    )
                    Embed.set_thumbnail(url=ctx.author.avatar_url)
                    await ctx.send(embed=Embed)
            else:
                with open(f"/home/pi/Desktop/Bot/Data/User/Profile/{target.id}", "r") as File:
                    Embed = discord.Embed(
                        title=f"{target.name}님의 프로필", 
                        description=File.read()
                    )
                    Embed.set_thumbnail(url=target.avatar_url)
                    await ctx.send(embed=Embed)

        except FileNotFoundError:
            if target.bot:
                await ctx.send("봇은 프로필을 생성할 수 없습니다.")
            else:
                with open(f"/home/pi/Desktop/Bot/Data/User/Profile/{ctx.author.id}", "w") as File:
                    await ctx.send("프로필이 생성되었습니다.")

    # @commands.command(name="test")
    # async def test(self, ctx: commands.Context):
    #     UserData = { str(ctx.message.author.id): "000000" }
    #     Data = None
    #     with open("/home/pi/Desktop/Bot/Data/User/UID.jsonc") as File:
    #         nonlocal Data
    #         Data = json.load(File)
    #     Data.update(UserData)
    #     with open("/home/pi/Desktop/Bot/Data/User/SID.jsonc") as File:
    #         json.dump(fp=File, obj=Data)
    #     await ctx.send("asdf")

    @commands.command(name="createUID")
    async def UserID(self, ctx: commands.Context):
        UserID    = None
        ServiceID = None
        con       = sqlite3.connect("/home/pi/Desktop/Bot/Data/User/SID-Data.sqlite3")
        cur       = con.cursor()
        UIDCount  = json.load(fp=open("/home/pi/Desktop/Bot/Data/User/SIDCount.json", "r"))["CurrentCount"]

        if ctx.author.id in cur.execute("select * from Data where=?", (ctx.author.id)).fetchall:
            await ctx.send("이미 존재함.")
        # cur.execute("")
        json.dump(fp=open("/home/pi/Desktop/Bot/Data/User/SIDCount.json", "w"), obj={"CurrentCount":UIDCount+1}, indent=4)

    R"""json으로 ID를 키, 번호를 값으로 하여 딕셔너리로 불러온 다음 for문과 items 함수로 ID를 찾는다"""
    R"""SQL로 불러옴, [0]: SID, [1]: UID"""

def setup(client):
    client.add_cog(User(client))