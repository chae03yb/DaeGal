import discord
from discord.ext import commands
import os
import asyncio
import SimpleJSON

Path = f"/DaeGal/Data"

class Docs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help", aliases=["도움말", "Help", "도움"])
    async def help(self, ctx:commands.Context, category:str=None, command:str=None):
        if category is not None: category = category.lower()
        if command is not None:  command = command.lower()

        Docs = SimpleJSON.Read(Path=f"{Path}/Help/Help/Help.json")

        if category is None:
            Embed = discord.Embed(
                title="카테고리 목록",
                color=0xFFCC00
            )
            for Cat in Docs.keys():
                if not bool(Docs[Cat]["info"]["commandList"]):
                    Embed.add_field(
                        name=f"`{Cat}`",
                        value="`비어있음`",
                        inline=True
                    )
                else:
                    Embed.add_field(
                        name=f"`{Cat}`", 
                        value=", ".join(Docs[Cat]["info"]["commandList"]), 
                        inline=True
                    )

            await ctx.send(embed=Embed)
            
        elif command is None:
            try:
                Embed = discord.Embed(
                    title=f"명령어 목록: `{category}`",
                    color=0xFFCC00
                )
                for Com in Docs[category].keys():

                    Embed.add_field(
                        name=f"`{Com}`",
                        value=f"{Docs[category][Com]['description'].strip('ㅤ')}",
                        inline=False
                    )
                await ctx.send(embed=Embed)
            except KeyError:
                Embed = discord.Embed(
                    title="오류",
                    description=f"`{category}` 카테고리를 찾지 못했습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
        else:
            command = command.strip("`")
            try:
                Help = Docs[category][command]
                Embed = discord.Embed(
                    title=f"명령어: `{category}/{command}`",
                    description=Help["description"],
                    color=0xFFCC00 
                )
                if Help["type"] == "info":
                    Embed.add_field(name="명령어 목록", value=", ".join(Help["commandList"]), inline=False)
                if Help["type"] == "command":
                    if bool(Help["arguments"]):
                        Embed.add_field(name="인수 목록", value="\n".join(Help["arguments"]), inline=False)
                    else:
                        Embed.add_field(name="인수 목록", value="**없음**", inline=False)
                    
                    Embed.add_field(name="사용", value=Help["use"], inline=False)

                    if bool(Help["aliases"]):
                        Embed.add_field(name="별칭", value=", ".join(Help["aliases"]), inline=True)
                    else:
                        Embed.add_field(name="별칭", value="**없음**", inline=True)
                    
                    if Help["isDeprecated"]:
                        Embed.add_field(name="삭제/대체 예정?", value="예")
                    else:
                        Embed.add_field(name="삭제/대체 예정?", value="아니오")
                    
                    Embed.add_field(name="도움말 보는 법", value="[대갈 위키](https://github.com/chae03yb/DaeGal/wiki/Help:-view)", inline=False)
                await ctx.send(embed=Embed)
            except KeyError:
                Embed = discord.Embed(
                    title="오류",
                    description=f"`{command}` 명령어를 찾지 못했습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)

    @commands.command(name="memo", aliases=["메모"])
    async def memo(self, ctx: commands.Context, TargetMemo=None):
        if TargetMemo is None:
            return await ctx.send("메모의 제목도 함께 써주십시오")
        if "/" in TargetMemo or "." in TargetMemo:
            return await ctx.send("허용되지 않은 문자가 있습니다")
        SavePath = None 
        try:
            SavePath = f"{Path}/Guild/{ctx.guild.id}/Memo"
        except AttributeError:
            SavePath = f"{Path}/User/{ctx.author.id}/Memo"
        ErrorEmbed = discord.Embed(
            title="오류",
            description="시간 초과.",
            color=0xFF0303
        )
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
                    try:
                        open(f"{SavePath}/{TargetMemo}", "w").close()
                    except FileNotFoundError:
                        try:
                            os.mkdir(SavePath)
                        except AttributeError:
                            os.mkdir(SavePath)
                    finally:
                        with open(f"{SavePath}/{TargetMemo}", "w") as File:
                            File.write(Memo.content)
                            await ctx.send("완료.")

            elif reaction == "🔍":
                try:
                    with open(f"{SavePath}/{TargetMemo}") as Memo:
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
                        os.remove(f"{SavePath}/{TargetMemo}")
                        await ctx.send("삭제 완료")
                    except FileNotFoundError:
                        await ctx.send("메모가 없습니다.")
            
            elif reaction == "📁":
                searchResult = []
                for result in os.listdir(SavePath):
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