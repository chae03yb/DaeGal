import os
import discord
from discord.ext import commands
from discord import utils
import json
import os.path
import time
import SimpleJSON

Path = "/DaeGal/Data/Guild/"

class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        GuildConfigPath = f"{Path}/{member.guild.id}/GuildConfig.json"
        try:
            if not member.bot:
                SimpleJSON.Read(GuildConfigPath)["Role"]["Member"]
            else:
                SimpleJSON.Read(GuildConfigPath)["Role"]["Bot"]
        except (FileNotFoundError, KeyError):
            return
        else:
            Config = SimpleJSON.Read(GuildConfigPath)

            try:
                if not member.bot:
                    await member.add_roles(utils.get(member.guild.roles, id=Config["Role"]["Member"]), atomic=True)
                else:
                    await member.add_roles(utils.get(member.guild.roles, id=Config["Role"]["Bot"]), atomic=True)
            except discord.errors.Forbidden:
                return

    @commands.Cog.listener(name="on_guild_join")
    async def onGuildJoin(self, guild: discord.Guild):
        os.mkdir(f"{Path}/{guild.id}")
        os.mkdir(f"{Path}/{guild.id}/Members")
        os.mkdir(f"{Path}/{guild.id}/Memo")
        os.mkdir(f"{Path}/{guild.id}/Welcome")

    @commands.command(name="setPunishRole", aliases=["정지_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setPunishRole(self, ctx: commands.Context, role: discord.Role):
        os.makedirs(f"{Path}/{ctx.guild.id}/Role", exist_ok=True)
        with open(f"{Path}/{ctx.guild.id}/Role/PunishRole.json", "w") as File:
            Data = { "Role": {"PunishRole": role.id }}
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setMemberRole", aliases=["멤버_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setDefaultRole(self, ctx: commands.Context, role: discord.Role):
        os.makedirs(f"{Path}/{ctx.guild.id}/Role", exist_ok=True)
        with open(f"{Path}/{ctx.guild.id}/Role/DefaultRole.json", "w") as File:
            Data = { "Role": {"MemberRole": role.id }}
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setBotRole", aliases=["봇_역할_설정"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setBotRole(self, ctx: commands.Context, role: discord.Role):
        os.makedirs(f"{Path}/{ctx.guild.id}", exist_ok=True)
        with open(f"{Path}/{ctx.guild.id}/Role/BotRole.json", "w") as File:
            Data = { "Role": {"BotRole": role.id }}
            json.dump(obj=Data, fp=File, indent=4)
            await ctx.send("설정 완료")
    
    @commands.command(name="setWelcomeChannel")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setWelcomeChannel(self, ctx: commands.Context, channel:discord.TextChannel=None):
        if channel is None:
            return await ctx.send("채널 언급/채널 이름이 필요합니다.")
        try:
            os.makedirs(f"{Path}/{ctx.guild.id}", exist_ok=True)
        except Exception as E:
            await ctx.send(E)
        finally:
            try:
                with open(f"{Path}/{ctx.guild.id}/Config.json") as File:
                    Data = { "Channel": { "WelcomeChannel": channel.id }}
                    json.dump(obj=Data, fp=File, indent=4)
                    await ctx.send("채널 설정 완료")
            except Exception as E:
                await ctx.send(E)
    
    # @commands.command(name="setNoticeChannel", aliases=["공지채널_설정"])
    async def setNoticeChannel(self, ctx:commands.Context, channel:discord.TextChannel=None):
        if channel is None:
            Embed = discord.Embed(
                title="오류",
                description="채널이 필요합니다",
                color=0xFF0000
            )
            return await ctx.send(embed=Embed)

        try:
            with open(f"/DaeGal/Data/Bot/NoticeChannel.json", "r") as rFile:
                Data = json.load(fp=rFile)
                with open(f"/DaeGal/Data/Bot/NoticeChannel.json", "w") as wFile:
                    Data.update({f"{ctx.guild.id}": channel.id})
                    json.dump(fp=wFile, obj=Data, indent=4)
                    Embed = discord.Embed(
                        title="성공",
                        description="공지 채널 설정에 성공했습니다",
                        color=0x00FF00
                    )
                    await ctx.send(embed=Embed)
                    
        except Exception as E:
            Embed = discord.Embed(
                title="실패",
                description=f"공지 채널 설정에 실패했습니다\n```사유: {E}```",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)

    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clear(self, ctx: commands.Context, reach: int, *, keyword=None):
        try:
            Embed = discord.Embed(
                title="성공",
                description=f"{reach}개의 메세지를 삭제했습니다",
                color=0x00FF00
            ).set_footer(text=f"요청자: {ctx.author}")

            if reach <= 0:
                return await ctx.send("범위는 0보다 큰 정수로 입력해주세요.")
            elif keyword is None:
                await ctx.channel.purge(limit=reach + 1)
                await ctx.send(embed=Embed)
            else:
                def check(ctx: commands.Context):
                    if keyword == None:
                        return True
                    else:
                        return ctx.content in str(keyword)
                        
                await ctx.message.delete()
                await ctx.channel.purge(limit=reach + 1, check=check)
                await ctx.send(embed=Embed)
        except Exception as E:
            errEmbed = discord.Embed(
                title="오류",
                description=f"{E}",
                color=0xFF0000
            )
            await ctx.send(embed=errEmbed)
    
    @commands.command(name="출석", aliases = ["ㅊㅊ", "cc"])
    @commands.guild_only()
    async def attendance(self, ctx: commands.Context, *, comment:str=None):
        DataPath = f"/DaeGal/Data/Guild/{ctx.guild.id}/Members"
        DataFile = f"{DataPath}/attendanceList.json"

        os.makedirs(DataPath, exist_ok=True)
        if comment is not None:
            if len(comment) > 500:
                comment = comment.replace(comment[500:], " ...")
            if "\n" in comment: comment = comment.replace(comment[comment.find("\n")], "\n> ")
            comment = f"\n\n> {comment}"
        if comment is None:
            comment = ""
        
        try:
            AttendantData = SimpleJSON.Read(Path=f"{Path}/{ctx.guild.id}/Members/attendanceList.json")

            if time.strftime(r"%Y-%m-%d", time.localtime()) == AttendantData[f"{ctx.author.id}"]["lastAttendance"]:
                Embed = discord.Embed(
                    title="이미 출석했습니다",
                    description="하루에 한 번만 출석할 수 있습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
            else:
                AttendantData[f"{ctx.author.id}"]["lastAttendance"] = time.strftime(r"%Y-%m-%d", time.localtime())
                AttendantData[f"{ctx.author.id}"]["count"] += 1
                SimpleJSON.Write(Path=DataFile, Object=AttendantData)

                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {AttendantData[f'{ctx.author.id}']['count']}회 입니다 {comment}",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)

        except KeyError:
            FileData = SimpleJSON.Read(Path=DataFile)
            FileData.update({ 
                f"{ctx.author.id}": { 
                    "count": 1, 
                    "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime()) 
                }
            })

            SimpleJSON.Write(Path=DataFile, Object=FileData)
            
            Embed = discord.Embed(
                title="✅",
                description=f"현재 {ctx.author}님의 출석 횟수는 1회 입니다 {comment}",
                color=0x00FF00
            )
            await ctx.send(embed=Embed)
        except FileNotFoundError:
            SimpleJSON.Write(Path=DataFile, Object={
                f"{ctx.author.id}": {
                    "count": 1,
                    "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime())
                }
            })
            Embed = discord.Embed(
                title="✅",
                description=f"현재 {ctx.author}님의 출석 횟수는 1회 입니다 {comment}",
                color=0x00FF00
            )
            await ctx.send(embed=Embed)
        finally:
            try:
                await ctx.message.delete()
            except:
                pass

def setup(client):
    client.add_cog(Guild(client))
