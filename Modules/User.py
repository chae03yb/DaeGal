import discord
from discord.ext import commands
import DaeGal_Utils
import SimpleJSON

PATH = "/home/pi/Desktop/Bot/Data"

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
    async def profile(self, ctx:commands.Context, target:discord.User=None):
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

    @commands.command(name="유저등록")
    async def addUser(self, ctx:commands.Context):
        path = "/home/pi/Desktop/Bot/Data/User/UserDataList.json"
        try:
            SimpleJSON.Read(path)[str(ctx.author.id)]
        except KeyError:
            Data = SimpleJSON.Read(path)
            DictData = {
                str(ctx.author.id): {
                    "UID": str(Data["nextUID"])
                }
            }
            Data["nextUID"] += 1
            Data += DictData
            SimpleJSON.BackupWrite(path, Data)
            Embed = discord.Embed(
                title="성공",
                description="```등록이 완료되었습니다```",
                color=DaeGal_Utils.EmbedColors.Green
            )
            Embed.set_footer(text=f"당신의 UID는 {0} 입니다")
            await ctx.send(embed=Embed)
        except Exception as E:
            Embed = discord.Embed(
                title="오류",
                description=f"```{E}```",
                color=DaeGal_Utils.EmbedColors.Red
            )
            await ctx.send(embed=Embed)
        else:
            Embed = discord.Embed(
                title="오류",
                description="```이미 등록이 완료된 사용자입니다```",
                color=DaeGal_Utils.EmbedColors.Red
            )
            await ctx.send(embed=Embed)

    # SID: JSON 파일 불러온 후 len(JSONDict) 앞 000으로 채움.

def setup(client):
    client.add_cog(User(client))