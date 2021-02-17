import discord
from discord.ext import commands

import os
import asyncio
import json
from os.path import join
from re import split
import SimpleJSON
import DaeGal_Utils
import Main

Path = f"/DaeGal/Data"

class Docs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help", aliases=["도움말", "Help", "도움"])
    async def help(self, ctx:commands.Context, category=None, command=None):
        with open(f"{Path}/Help/Help/Help.json", "r") as File:
            Docs = json.load(fp=File)

            if category is None:
                Embed = discord.Embed(
                    title="카테고리 목록",
                    color=0xFFCC00
                )
                for Cat in Docs.keys():
                    Embed.add_field(
                        name=str(Cat).strip("`"), 
                        value=", ".join(Docs[Cat]["`info`"]["commandList"]), 
                        inline=True
                    )
                
                await ctx.send(embed=Embed)
                # 카테고리 목록
            elif command is None:
                try:
                    category = f"`{category}`"
                    Embed = discord.Embed(
                        title=f"명령어 목록: {category} ",
                        color=0xFFCC00
                    )
                    for Com in Docs[category].keys():
                        Embed.add_field(
                            name=str(Com).strip("`"),
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
                    
    @commands.command(name="_help")
    @commands.check(Main.isOwner)
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

    @commands.command(name="변경사항", aliases=["changelog"])
    async def changelog(self, ctx: commands.Context, version="Lastest"):
        BotConfig = "/DaeGal/Data/Config.json"
        LogPath   = ""

        
        with open(BotConfig, "r") as File:
            versionName = json.load(fp=File)["version"]
            if version == "Lastest":
                LogPath += f"/DaeGal/Data/Bot/ChangeLog/{versionName}.md"
            else:
                LogPath += f"/DaeGal/Data/Bot/ChangeLog/{version}.md"

        try:
            with open(LogPath, 'r') as ChangeLog:
                Content = ChangeLog.read()
                embed = discord.Embed(
                    title=f"변경 사항 버전: {version} ",
                    description=f"```md\n" \
                                f"{Content}\n"\
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

def setup(client):
    client.add_cog(Docs(client))