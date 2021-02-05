from discord.ext import commands
import Main
import discord
import DaeGal_Utils

DataPath = "/home/pi/Desktop/Bot/Data"

class CustomCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="cmd")
    @commands.check(Main.isOwner)
    async def customCommands(self, ctx: commands.Context, *, cmd: str):
        seperatedCMD = cmd.split(";\n")
        for c in seperatedCMD:
            editedCMD = c.replace('(', ' ')
            editedCMD.replace(')', ' ')
            # old: a(arg1=ㅁㄴㅇㄹ, arg2=135);
            # new: a arg1=ㅁㄴㅇㄹ, arg2=135
            CMDargs = editedCMD.replace(old=editedCMD.split(' ')[0], new=' ')
            CMDargs = CMDargs.lstrip()
            # CMDargs: arg1=ㅁㄴㅇㄹ, arg2=135
            CMDargs = CMDargs.split(', ')
            # CMDargs: [arg1=ㅁㄴㅇㄹ, arg2=135]
            await ctx.invoke(command=editedCMD.split(' ')[0], )

    # invoke로 명령어 호출
    @customCommands.error()
    async def cmd_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errEmbed = discord.Embed(
                title="오류",
                description=f"```{error}```",
                color=DaeGal_Utils.EmbedColors.Red
            )
            await ctx.send(embed=errEmbed)

def setup(client):
    client.add_cog(CustomCommands(client))