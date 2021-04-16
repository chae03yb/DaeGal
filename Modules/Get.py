import discord
from discord.ext import commands
import SimpleJSON
import Main

Path = "/DaeGal/Data/"

class Get(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Get
    #   - Bot
    #     - Info
    #   - User
    #     - Profile
    #   - Member
    #     - Warning

    # changelog -> get
    
    @commands.core.group(name="Get", aliases=["확인", "get"])
    async def GeneralGet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            Embed = discord.Embed(
                title="오류",
                description="설정할 항목을 선택해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
    
    @GeneralGet.group(name="Bot", aliases=["봇", "bot"])
    async def BotGet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            Embed = discord.Embed(
                title="오류",
                description="설정할 항목을 선택해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
    
    @BotGet.command(name="Version", aliases=["버전", "version"])
    async def version(self, ctx:commands.Context): 
        Data = SimpleJSON.Read(Path=f"{Path}/Config.json")
        Embed = discord.Embed(
            title="현재 버전",
            description=f"현재 버전은 {Data['version']} 입니다.",
            color=0x7777FF
        )
        await ctx.send(embed=Embed)
    
    @BotGet.command(name="ChangeLog", aliases=["변경사항", "changelog"])
    async def changelog(self, ctx:commands.Context, version="Latest"):
        BotConfig = "/DaeGal/Data/Config.json"
        LogPath   = ""
        versionName = SimpleJSON.Read(Path=BotConfig)["version"]

        if version == "Latest":
            LogPath += f"{Path}/Bot/ChangeLog/{versionName}.md"
        else:
            LogPath += f"{Path}/Bot/ChangeLog/{version}.md"
        
        try:
            with open(LogPath, 'r') as ChangeLog:
                Content = ChangeLog.read()
                embed = discord.Embed(
                    title=f"변경 사항\n버전: {version} ",
                    description=f"```md\n" \
                                f"{Content}\n" \
                                f"```",
                    color=0xFFFF33
                )
                await ctx.send(embed=embed)
        except FileNotFoundError:
            embed = discord.Embed(
                title="오류",
                description="해당 버전을 찾을 수 없습니다",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
    
    @BotGet.command(name="Info", aliases=["정보", "info"])
    async def botInfo(self, ctx:commands.Context):
        Embed = discord.Embed(
            title="봇 정보",
            color=0xFF7F00
        )
        Embed.add_field(name="버전", value=f"{SimpleJSON.Read(Path=f'{Path}/Config.json')['version']}", inline=True)
        Embed.add_field(name="지연시간", value=f"`{int(self.client.latency * 1000)}ms`", inline=False)
        Embed.add_field(name="로드된 모듈", value=f"{chr(0x0A).join(Main.Modules)}", inline=True)
        # Embed.add_field(name="로그인 횟수", value=f"{SimpleJSON.Read(Path=f'{Path}/Config.json')['loginCount']} 회", inline=True)

        Embed.set_thumbnail(url=r"https://cdn.discordapp.com/avatars/736998050383396996/ca806a6a4c1fcec5b6d0c0f3a43ad041.png?size=128")
        await ctx.send(embed=Embed)

    @GeneralGet.group(name="User", aliases=["유저", "사용자"])
    async def UserGet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            Embed = discord.Embed(
                title="오류",
                description="설정할 항목을 선택해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)

    @UserGet.command(name="Profile", aliases=["프로필", "profile"])
    async def profile(self, ctx:commands.Context, target:discord.User=None):
        Data = SimpleJSON.Read(Path=f"{Path}/User/UserDataList.json")
        if target is None:
            target = ctx.author
        try:
            if target is None:
                Embed = discord.Embed(
                    title="프로필",
                    description=Data[f"{ctx.author.id}"]["ProfileComment"],
                    color=0xAACCFF
                )
                Embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=Embed)
            else:
                Embed = discord.Embed(
                    title="프로필",
                    description=f"```{Data[f'{target.id}']['ProfileComment']}```",
                    color=0xAACCFF
                )
                Embed.set_thumbnail(url=target.avatar_url)
                await ctx.send(embed=Embed)

        except KeyError:
            Embed = discord.Embed(
                title=f"{target.id}님의 프로필",
                description="** **",
                color=0xAACCFF
            )
            await ctx.send(embed=Embed)

    @GeneralGet.group(name="Member", aliases=["멤버", "member"])
    async def MemberGet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            Embed = discord.Embed(
                title="오류",
                description="설정할 항목을 선택해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)

    @MemberGet.command(name="Warning", aliases=["경고", "warning"])
    async def warninglist(self, ctx:commands.Context, target:discord.Member=None):
        if target is None:
            try:
                Data = SimpleJSON.Read(Path=f"{Path}/Guild/{ctx.guild.id}/Members/WarningList.json")
                Embed = discord.Embed(
                    title=f"경고 목록",
                    description=f"사용자: `{ctx.author}`",
                    color=0xFF0000
                )
                Embed.add_field(name="경고 횟수", value=Data[f"{ctx.author.id}"])
                
                await ctx.send(embed=Embed)
            except KeyError:
                Embed = discord.Embed(
                    description=f"당신은 아직 경고를 받지 않았습니다",
                    color=0xFF0000 
                )
                await ctx.send(embed=Embed)
        else:
            try:
                Data = SimpleJSON.Read(Path=f"{Path}/Guild/{ctx.guild.id}/Members/WarningList.json")
                Embed = discord.Embed(
                    title=f"경고 목록",
                    description=f"사용자: `{target}`",
                    color=0xFF0000
                )
                Embed.add_field(name="경고 횟수", value=Data[f"{target.id}"])
                
                await ctx.send(embed=Embed)
            except KeyError:
                Embed = discord.Embed(
                    description=f"{target} 님은 아직 경고를 받지 않았습니다",
                    color=0xFF0000 
                )
                await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(Get(client))
