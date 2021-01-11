import discord
from discord.ext import commands
from discord import utils
import json
import os.path
import asyncio
import Main
import decimal

Path = "/home/pi/Desktop/Bot/Data/Guild/"

class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if member.bot == False:
                with open(f"{Path}/{member.guild.id}/Role/DefaultRole.json", "r") as File:
                    await member.add_roles(utils.get(member.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
            if member.bot == True:
                with open(f"{Path}/{member.guild.id}/Role/BotRole.json", "r") as File:
                    await member.add_roles(utils.get(member.guild.roles, id=json.load(File, encoding="utf-8")["roleID"]), atomic=True)
        except FileNotFoundError:
            pass
        try:
            Embed = None
            with open(f"{Path}/{member.guild.id}/Welcome/Message", "r") as File:
                Embed = discord.Embed(
                    color=0x000000,
                    title="환영합니다",
                    description=File.read()
                )
            with open(f"{Path}/{member.guild.id}/Welcome/Channel.json", "r") as File:
                await member.guild.get_channel(json.load(fp=File)["ChannelID"]).send(embed=Embed)
        except FileNotFoundError:
            pass

    @commands.Cog.listener(name="on_guild_join")
    async def onGuildJoin(self, guild: discord.Guild):
        os.mkdir(f"{Path}/{guild.id}")
        os.mkdir(f"{Path}/{guild.id}/Members")
        os.mkdir(f"{Path}/{guild.id}/Memo")
        os.mkdir(f"{Path}/{guild.id}/Role")
        os.mkdir(f"{Path}/{guild.id}/Welcome")

    @commands.command(name="setPunishRole", aliases=["정지_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setPunishRole(self, ctx: commands.Context, role: discord.Role):
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Role"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Role")
        with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "w") as File:
            Data = { "roleID": role.id }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setDefaultRole", aliases=["기본_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setDefaultRole(self, ctx: commands.Context, role: discord.Role):
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Role"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Role")
        with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "w") as File:
            Data = { "roleID": role.id }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setBotRole", aliases=["봇_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setBotRole(self, ctx: commands.Context, role: discord.Role):
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Role"):
            os.makedirs(f"{Path}/{ctx.guild.id}/Role")
        with open(f"{Path}/{ctx.guild.id}/Role/BotRole.json", "w") as File:
            Data = { "roleID": role.id }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setWelcomeChannel")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setWelcomeChannel(self, ctx: commands.Context, channel:discord.TextChannel=None):
        if channel is None:
            await ctx.send("채널 이름/채널 멘션이 필요합니다.")
        else:
            try:
                await ctx.send("환영 메시지를 보낼 채널을 멘션해주십시오")
                async def setChannel(msg: discord.TextChannel):
                    return msg.message.content and msg.message.author == ctx.message.author
                Channel = await self.client.wait_for(event="on_message", timeout=500.0, check=setChannel)
            except asyncio.TimeoutError:
                await ctx.send("시간 초과")
            else:
                try:
                    with open(f"{Path}/{ctx.guild.id}/Welcome/Channel.json") as File:
                        Data = { "ChannelID": Channel.id }
                        json.dump(obj=Data, fp=File, indent=4)
                        await ctx.send("채널 설정 완료")
                except Exception as E:
                    await ctx.send(E)

    # @commands.command(name="setWelcomeMsg")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setWelcomeMsg(self, ctx: commands.Context, option=None):
        if option == "del":
            os.remove(f"{Path}/{ctx.guild.id}/Welcome/Msg")
            return
        try:
            async def setMessage(msg):
                return msg.message.content and msg.message.author == ctx.message.author

            Embed = discord.Embed(
                title="환영 메세지의 내용을 입력해주세요"
            )
            await ctx.send(embed=Embed)
            Message = await self.client.wait_for(event="on_message", timeout=500.0, check=setMessage)
        except asyncio.TimeoutError:
            await ctx.send("시간 초과")
        else:
            if Message == "None":
                await ctx.send("설정을 종료합니다")
                return
            try:
                with open(f"{Path}/{ctx.guild.id}/Welcome/Message", "w") as File:
                    File.write(Message)
                    await ctx.send("메세지 설정 완료")
            except Exception as E:
                await ctx.send(E)

        """if message is None:
            await ctx.send("환영 메세지의 내용을 입력해주세요")
            return
        if not os.path.exists(f"{Path}/{ctx.guild.id}"):
            os.mkdir(f"{Path}/{ctx.guild.id}")
        with open(f"{Path}/{ctx.guild.id}/WelcomeMsg.txt", "w") as File:
            File.write(message)
            await ctx.send("설정 완료")
        if CID is None:
            await ctx.send("채널 ID가 필요합니다")
            return
        if not os.path.exists(f"{Path}/{ctx.guild.id}/Channel"):
            os.makedirs(f"{Path}/{ctx.guild.id}")
        with open(f"{Path}/{ctx.guild.id}/GuildConfig.json", "w") as File:
            Data = { "WelcomeChannel": CID }
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")"""

    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clear(self, ctx: commands.Context, reach: int, *, keyword=None):
        if reach <= 0:
            if reach == -1:
                await ctx.channel.purge(limit=decimal.Decimal("Infinity"))
            else:
                return await ctx.send("범위는 1 이상의 정수로 입력해주세요.")
        elif keyword is None:
            await ctx.channel.purge(limit=reach + 1)
        else:
            def check(ctx: commands.Context):
                if keyword == None:
                    return True
                else:
                    return ctx.content in str(keyword)
            await ctx.channel.purge(limit=reach, check=check)
    
    @commands.command(name="도배")
    @commands.check(Main.isOwner)
    async def asdf(self, ctx, a: int):
        while a:
            await ctx.send("ㅁ")

def setup(client):
    client.add_cog(Guild(client))
