import discord
from discord.ext import commands
import os

class User(commands.Cog, name = "프로필"):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "소개변경", aliases = ["introduce"])
    async def setProfile(self, ctx, Description = None):
        if Description is None:
            await ctx.send("소개가 필요합니다.")
        if Description == "-h":
            await ctx.send("`?소개 변경 <소개>`")
        elif Description == "-remove":
            with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "w") as File:
                File.write(" ")
                await ctx.send("소개를 제거했습니다.")
        else:
            with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "w") as File:
                File.write(Description)
                await ctx.send("소개를 변경했습니다.")
    
    @commands.command(name = "프로필", aliases = ["profile"])
    async def profile(self, ctx, target: discord.User = None):
        if target is None:
            try:
                with open(f"/home/pi/Desktop/Bot/Data/Profile/{ctx.author.id}.txt", "r") as File:
                    Embed = discord.Embed(title = f"{ctx.author.name}님의 프로필", description = File.read())
                    Embed.set_thumbnail(url = ctx.author.avatar_url)
                    await ctx.send(embed = Embed)
            except FileNotFoundError:
                await ctx.send("대상의 프로필이 없습니다")
        else:
            try:
                with open(f"/home/pi/Desktop/Bot/Data/Profile/{target.id}.txt", "r") as File:
                    Embed = discord.Embed(title = f"{target.name}님의 프로필", description = File.read())
                    Embed.set_thumbnail(url = target.avatar_url)
                    await ctx.send(embed = Embed)
            except FileNotFoundError:
                await ctx.send("대상의 프로필이 없습니디.")

def setup(client):
    client.add_cog(User(client))