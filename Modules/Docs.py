import discord
from discord.ext import commands

import os
import asyncio
import json
from os.path import join
from re import split

Path = f"/home/pi/Desktop/Bot/Data"

class Docs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # @commands.command(name="Help", aliases=["도움말", "help", "도움"])
    async def Help(self, ctx: commands.Context, Target=None):
        return await ctx.send("재작업중....")
        try:
            if Target.startswith("." or "/"):
                return
        except AttributeError:
            pass
        Path = "/home/pi/Desktop/Bot/Data/Help/Help"
        try:
            if Target is None:
                NoCat = []
                Embed = discord.Embed(
                    title="명령어 목록",
                    # description="`(카테고리)/(명령어)` 형식으로 명령어 확인 가능",
                    color=0x7289DA
                )

                # for Category in os.listdir(Path):
                #     if os.path.isdir(f"{Path}/{Category}"):
                #         commandsList = []
                #         for command in os.listdir(f"{Path}/{Category}"):
                #             commandsList.append(f"`{command}`")
                #         Embed.add_field(name=Category, value=", ".join(commandsList))
                #     else:
                #         NoCat.append(f"`{Category}`")
                
                def commandReturner():
                    comList = []
                    for command in os.listdir(Path):
                        pass
                    return 
                
                def categoryReturner():
                    catSet = set()
                    for cat in os.listdir(Path):
                        catSet.add(cat.split(";")[0])
                    return catSet
                    # Embed.add_field(name=Filename.split(";")[0], value=", ".join(commandsList))

                # if bool(NoCat) == True:
                #     Embed.add_field(name="기타", value=", ".join(NoCat))
                # for cat in os.listdir(Path): # cat: category;command
                #     category = cat.split(";")[0]
                #     commands = ["asdf"]
                #     if cat.split(";")[1] == "info":
                #         pass
                #     else:
                #         commands.append(cat.split(";")[1])
                    
                # Embed.add_field()
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

    @commands.command(name="help", aliases=["도움말", "Help", "도움"])
    async def _help(self, ctx:commands.Context, category=None, command=None):
        with open(f"{Path}/Help/Help/Help.json", "r") as File:
            Docs = json.load(fp=File)

            if category is None:
                Embed = discord.Embed(
                    title="카테고리 목록",
                    description=", ".join(list(Docs.keys()))
                )
                await ctx.send(embed=Embed)
                # 카테고리 목록
            elif command is None:
                try:
                    category = f"`{category}`"
                    Embed = discord.Embed(
                        title=f"명령어 목록: {category} ",
                        description=", ".join(list(Docs[category].keys()))
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
                try:
                    category = f"`{category}`"
                    command  = f"`{command}`"
                    Help = Docs[category][command]
                    Embed = discord.Embed(
                        title=f"명령어: {category}/{command}",
                        description=Help["description"],
                        color=0xFFCC00 # int(Docs[category][command]["color"], 16)
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
                            Embed.add_field(name="별칭", value=", ".join(Help["aliases"]), inline=False)
                        else:
                            Embed.add_field(name="별칭", value="**없음**", inline=False)

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