import asyncio
from discord.ext import commands
import discord
import random
import json
import os

Path = "/DaeGal/Data" # 데이터 저장할 경로

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="random", aliases=["랜덤"])
    async def RandomNumberGenerator(self, ctx: commands.Context, Min=None, Max=None):
        random.seed()
        if Min is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="최솟값을 입력해주세요",
                color=0xFF0000
            ))
        elif Max is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="최댓값을 입력해주세요",
                color=0xFF0000
            ))
        elif Min > Max:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="최솟값이 최댓값보다 클 수 없습니다",
                color=0xFF0000
            ))
        else:
            try:
                await ctx.reply(embed=discord.Embed(
                    title="결과",
                    description=f"🎲 {random.randint(int(Min), int(Max))}",
                    color=0xFFFF00
                ))
            except ValueError:
                await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="최솟값/최댓값은 정수만 가능합니다",
                    color=0xFF0000
                ))

    @commands.command(name="dice", aliases=["주사위"])
    async def dice(self, ctx: commands.Context):
        random.seed()
        await ctx.reply(embed=discord.Embed(
            title="결과",
            description=f"🎲 {random.randint(1, 6)}",
            color=0xFFFF00
        ))

    @commands.command(name="choice", aliases=["선택"])
    async def choice(self, ctx: commands.Context, *contents):
        random.seed()
        if bool(contents) is False:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="선택할 항목이 1개 이상 필요합니다",
                color=0xFF0000
            ))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"선택할 항목들: `{'`, `'.join(contents)}`\n\n결과: `{random.choice(contents)}`",
                color=0xFFFF00
            ))
    
    # @commands.command(name="조커뽑기")
    async def joker(self, ctx: commands.Context):
        pass

    # @commands.command(name="도박", aliases=["ㄷㅂ", "eq", "ehqkr"])
    async def do_bak(self, ctx:commands.Context, betType="All_in", betMoney=0):
        return
        # betType = 베팅할 타입
        #   All_in: 올인함
        #   %: 100% 이하의 비율로 베팅함
        #       소숫점 아래는 버림
        #   $: 돈 가진 액수 안에서 베팅함
        Multiple = [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            2, 2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3,
            4, 4,
            5,
            10
        ]
        poorPeopleEmbed = discord.Embed(
            # 임베드 메시지를 만들어요
            title="돈이 없네요!", # 제목
            description="돈이 없어요...", # 설명
            color=0xFF7F00 # 색깔은 주황색으로
        ) \
        .set_thumbnail(url=r"https://cdn.discordapp.com/attachments/805808631312023582/805809017624461312/4797c3873fe25139.jpg") \
        .set_footer(text="돈이 없다면 구걸해보는게 어떨까요?")
                
        if betType != "All_in" and betMoney == 0:
            return await ctx.send("0원을 베팅할 수 없어요")

        if betType == "%": # 베팅 타입이 비율 이라면
            os.makedirs(f"{Path}/Guild/{ctx.guild.id}/Members", exist_ok=True) # 폴더 없으면 자동으로 만들어줌
            # 함수 이름을 뭐로 하지
            async def do_allin(): # 다시 써야 해서 함수로 
                with open(f"{Path}/Guild/{ctx.guild.id}/Members/{ctx.author.id}.json", "r") as File: 
                    # Path(/DaeGal/Data) 여기 경로 아래에 있는
                    # User 폴더 안에 명령어 친 사람의 18자리 ID의 이름을 가진 파일을 보는거임
                    Data = json.load(fp=File)["Economy"]
                    if Data["Money"] == 0:
                        # 돈 없는 그지라면
                        
                        await ctx.send(embed=poorPeopleEmbed) # 만든 임베드 메세지를 임베드 메세지라고 알려준 후 보냄
                    else:
                        # 돈 없는 그지가 아니라면
                        nonlocal betMoney
                        betMoney = Data["Money"] / (100 / betMoney)

                        if int(betMoney) == 0:
                            await ctx.send(embed=poorPeopleEmbed)
                        else:
                            random.seed()
                            Multiple = random.choice()
                            if Multiple != 0:
                                writeData = json.load(fp=File).update({"Economy":{"Money":betMoney*Multiple}})
                                with open(f"{Path}/Guild/{ctx.guild.id}/Members/{ctx.author.id}.json", "w") as UserData:
                                    json.dump(fp=UserData, obj=writeData, indent=4)
                            elif Multiple == 0:
                                writeData = json.load(fp=File).update({"Economy":{"Money":0}})
                                with open(f"{Path}/Guild/{ctx.guild.id}/Members/{ctx.author.id}.json", "w") as UserData:
                                    json.dump(fp=UserData, obj=writeData, indent=4)
                                await ctx.send("꽝이네요...")
                            
                            if Multiple == 10:
                                await ctx.send("10배 당첨이네요!")
            try:
                await do_allin() # 위에 만든 함수
            except FileNotFoundError:
                # 파일을 못찾았을때
                with open(f"{Path}/Guild/{ctx.guild.id}/Members/{ctx.author.id}.json", "w") as File:
                    # 파일을 만듬
                    obj = {
                        "Economy": {
                            "Money": 1000000 # 초기 자금 1000000딸라
                        }
                    }
                    json.dump(fp=File, obj=obj, indent=4) 
                    # obj: 파일에 쓸 내용, indent: 파일 들여쓰기를 띄어쓰기 몇칸으로?
                    await do_allin()
        elif betType == "$": # 베팅 타입이 액수라면
            pass
        else:
            pass
    
    # @commands.command(name="포커", aliases=["poker"])
    async def poker(self, ctx:commands.Context, playerCount:int=1):
        if not playerCount > 1:
            return await ctx.send("참가 인원은 1명보다 작을 수 없습니다")
        PlayerList = []
        def getPlayers(reaction, user):
            return reaction and user
        
        async def startGame():
            await ctx.send("게임을 시작합니다")
        
        async def addUser():
            reaction, user = await self.client.wait_for("reaction_add", check=getPlayers, timeout=30.0)
            PlayerList.append(user.id)
        try:
            await addUser()
        except asyncio.TimeoutError:
            startGame()
        else:
            pass
        
    # 앞으로 만들 예정 #

    # 카드게임
    # 턴제 전략 게임
    # 도박
    # 주식
    # 슬롯머신

def setup(client):
    client.add_cog(Game(client))
    