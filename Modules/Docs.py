import discord
from discord.ext import commands
import os
import asyncio
Path = f"/home/pi/Desktop/Bot/Data"

class Docs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="Help", aliases=["도움말", "help", "도움"])
    async def Help(self, ctx: commands.Context, Target: str=None):
        try:
            if Target.startswith("." or " "):
                return
        except AttributeError:
            pass
        Path = "/home/pi/Desktop/Bot/Data/Help/Help"
        try:
            if Target is None:
                NoCat = []
                Embed = discord.Embed(
                    title="명령어 목록",
                    description="`(카테고리)/(명령어)` 형식으로 명령어 확인 가능",
                    color=0x7289DA
                )

                for Category in os.listdir(Path):
                    if os.path.isdir(f"{Path}/{Category}"):
                        commandsList = []
                        for command in os.listdir(f"{Path}/{Category}"):
                            commandsList.append(f"`{command}`")
                        Embed.add_field(name=Category, value=", ".join(commandsList))
                    else:
                        NoCat.append(f"`{Category}`")

                if bool(NoCat) == True:
                    Embed.add_field(name="기타", value=", ".join(NoCat))

                Embed.set_footer(text="기타 도움말: ?help info")
                await ctx.send(embed=Embed)
            else:
                if os.path.isdir(f"{Path}/{Target}"):
                    Embed = discord.Embed(
                        title="명령어 목록",
                        description=f"카테고리: {Target}",
                        color=0x7289DA
                    )
                    Embed.add_field(name=Target, value="`"+"`, `".join(os.listdir(f"{Path}/{Target}"))+"`")
                    Embed.set_footer(text="기타 도움말: ?help info")
                    await ctx.send(embed=Embed)
                else:
                    with open(f"{Path}/{Target}", "r") as File:
                        Embed = discord.Embed(
                            title=f"{Target} 도움말",
                            description=File.read(),
                            color=0x7289DA
                        )
                        Embed.set_footer(text="기타 도움말: ?help info")
                        await ctx.send(embed=Embed)
        except FileNotFoundError:
            Embed = discord.Embed(
                title="오류",
                description="도움말을 찾지 못했습니다.",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
    
    @commands.command(name="memo", aliases=["메모"])
    async def memo(self, ctx: commands.Context, TargetMemo=None):
        ErrorEmbed = discord.Embed(
            title="오류",
            description="시간 초과.",
            color=0xFF0303
        )
        if TargetMemo is None:
            return await ctx.send("메모의 제목도 함께 써주십시오")
        if "/" in TargetMemo or "." in TargetMemo:
            return await ctx.send("허용되지 않은 문자가 있습니다")
        Embed = discord.Embed(
            title="메모",
            description="📝: 메모 쓰기\n" \
                        "🔍: 메모 보기\n" \
                        "🗑: 메모 삭제\n" \
                        "📁: 메모 검색"
        )
        msg = await ctx.send(embed=Embed)
        for emoji in ["📝", "🔍", "🗑", "📁"]:
            await msg.add_reaction(emoji)
        
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji)
        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed=ErrorEmbed)
            await msg.delete(delay=3)
        else:
            reaction = str(reaction.emoji)
            await msg.delete()

            if reaction == "📝":
                Memo = None
                def MemoContent(message: discord.Message):
                    return message.author == ctx.message.author and message.content
                try:
                    await ctx.send("메모의 내용을 입력해주십시오")
                    Memo = await self.client.wait_for("message", timeout=120, check=MemoContent)
                except asyncio.TimeoutError:
                    await ctx.send(embed=ErrorEmbed)
                    await msg.delete(delay=3)
                else:
                    async def writeFile():
                        try:
                            open(f"{Path}/Guild/{ctx.guild.id}/Memo/{TargetMemo}", "w").close()
                        except FileNotFoundError:
                            pass
                        finally:
                            with open(f"{Path}/Guild/{ctx.guild.id}/Memo/{TargetMemo}", "w") as File:
                                File.write(Memo.content)
                                await ctx.send("완료.")
                    try:
                        await writeFile()
                    except FileNotFoundError:
                        os.mkdir(f"{Path}/Guild/{ctx.guild.id}/Memo")
                        await writeFile()

            elif reaction == "🔍":
                try:
                    with open(f"{Path}/Guild/{ctx.guild.id}/Memo/{TargetMemo}") as Memo:
                        Embed = discord.Embed(
                            title=f"메모: {TargetMemo}",
                            description=Memo.read()
                        )
                        await ctx.send(embed=Embed)
                except FileNotFoundError:
                    await ctx.send("메모가 없습니다.")

            elif reaction == "🗑":
                try:
                    def deleteCheck(answer):
                        return answer.author == ctx.message.author and answer.content == "Y"
                    await ctx.send("메모 삭제를 원하신다면 Y를 입력해주십시오")
                    await self.client.wait_for("message", timeout=600, check=deleteCheck)
                except asyncio.TimeoutError:
                    await ctx.send(embed=ErrorEmbed)
                    # return "시간 초과"
                else:
                    try:
                        os.remove(f"{Path}/Guild/{ctx.guild.id}/Memo/{TargetMemo}")
                        await ctx.send("삭제 완료")
                    except FileNotFoundError:
                        await ctx.send("메모가 없습니다.")
            
            elif reaction == "📁":
                searchResult = []
                for result in os.listdir(f"{Path}/Guild/{ctx.guild.id}/Memo/"):
                    if TargetMemo in result:
                        searchResult.append(f"`{result}`")

                Embed = None
                if not searchResult:  
                    Embed = discord.Embed(
                        title=f"검색: {TargetMemo}",
                        description="검색 결과가 없습니다."
                    )
                else:
                    Embed = discord.Embed(title=f"검색 결과: {TargetMemo}")
                    Embed.add_field(name="결과", value=f", ".join(searchResult))
                await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(Docs(client))