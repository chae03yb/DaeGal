from discord.ext import commands
import Main

DataPath = "/home/pi/Desktop/Bot/Data"

class CustomCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="cmd")
    @commands.check(Main.isOwner)
    async def cmd(self, ctx: commands.Context, option, title, *, command=None):
        return await ctx.send("아직 개발중인 기능입니다.")
        # 미완성
        if option == "-s" or "--save":
            if command is None:
                return await ctx.send("수행할 작업을 입력해야 합니다.")
            else:
                try:
                    with open(F"{DataPath}/CustomCommands/{ctx.message.author.id}/{title}.txt", "w", encoding = "utf-8") as File:
                        pass
                except Exception as E:
                    return await ctx.send(F"E {E}")
        # 미완성
        elif option == "-e" or "--execute":
            with open(F"{DataPath}/CustomCommands/{ctx.message.author.id}/{title}.txt", "r", encoding = "utf-8") as commandFile:
                pass
        # 테스트 필요
        elif option == "-v" or "--view":
            with open(F"{DataPath}/CustomCommands/{ctx.message.author.id}/{title}.txt", "r", encoding = "utf-8") as commandData:
                try:
                    await ctx.send(F"```{commandData}```")
                except Exception as E:
                    await ctx.send(F"E: {E}")
        else:
            return await ctx.send("유효하지 않은 옵션입니다.")
    
    @commands.group(name="shell")
    @commands.check(Main.isOwner)
    async def shell(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send("실행할 명령어를 입력해주세요.")

    @commands.command(name="cmdedit")
    @commands.check(Main.isOwner)
    async def cmdedit(self, ctx: commands.Context, option, title, *, command=None):
        return
        if option == "-e" or "--edit":
            pass
        elif option == "-d" or "--delete":
            pass

def setup(client):
    client.add_cog(CustomCommands(client))