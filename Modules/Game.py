import asyncio
from discord.ext import commands
import discord
import random
import SimpleJSON

Path = "/DaeGal/Data" # 데이터 저장할 경로

def getUserData(ctx: commands.Context) -> dict:
    try:
        SimpleJSON.Read(f"{Path}/User/{ctx.author.id}.json")["Economy"]
    except FileNotFoundError:
        SimpleJSON.Write(f"{Path}/User/{ctx.author.id}.json", { 
            "Economy": { 
                "money": 5000 
            } 
        })
    except KeyError:
        tempdata: dict = SimpleJSON.Read(f"{Path}/User/{ctx.author.id}.json")
        tempdata.update({ 
            "Economy": { 
                "money": 5000 
            } 
        })
        SimpleJSON.Write(f"{Path}/User/{ctx.author.id}.json", tempdata)
    finally:
        return SimpleJSON.Read(f"{Path}/User/{ctx.author.id}.json")

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

    @commands.command(name="getMoney", aliases=["돈받기", "ㄷㅂㄱ", "eqr"])
    @commands.cooldown(rate=2, per=10800, type=commands.BucketType.user)
    async def claimMoney(self, ctx: commands.Context):
        userData: dict = getUserData(ctx)
        if userData["Economy"]["money"] != 0:
            return await ctx.send(embed=discord.Embed(
                title="오류",
                description="잔고가 비어있을 경우에만 사용이 가능합니다",
                color=0xFF0000
            ))
        else:
            userData["Economy"]["money"] = 500
            SimpleJSON.Write(f"{Path}/User/{ctx.author.id}.json", {
                "Economy": {
                    "money": 500
                }
            })
            return await ctx.send(embed=discord.Embed(
                title="성공",
                description="500원을 받았습니다",
                color=0x00FF00
            ))

    @commands.cooldown(1, 3, type=commands.BucketType.user)
    @commands.command(name="도박", aliases=["ㄷㅂ", "eq", "ehqkr", "bet"])
    async def do_bak(self, ctx:commands.Context, command: str):
        try:
            betmoney = int(command)
        except ValueError:
            if command.startswith("/"):
                try:
                    betmoney = int(getUserData(ctx)["Economy"]["money"] / int(command.replace("/", "")))
                except ValueError:
                    return await ctx.send(
                        embed=discord.Embed(
                            title="오류",
                            description="올바른 금액을 입력해 주세요",
                            color=0xFF0000
                        )
                    )
            else:
                return await ctx.send(
                    embed=discord.Embed(
                        title="오류",
                        description="올바른 금액을 입력해 주세요",
                        color=0xFF0000
                    )
                )

        # 베팅은 가진 액수에서 차감
        if betmoney < 0:
            return await ctx.send(embed=discord.Embed(
                title="오류",
                description="올바른 금액을 입력해주세요",
                color=0xFF0000
            ))

        multiple: list = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            2, 2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3,
            4, 4,
            5,
            10
        ]
        
        userdata: dict = getUserData(ctx)

        if userdata["Economy"]["money"] == 0:
            return await ctx.send(embed=discord.Embed(
                title="돈이 없네요!", # 제목
                description="돈이 없어요...", # 설명
                color=0xFF7F00 # 색깔은 주황색으로
            ) \
            .set_thumbnail(url=r"https://cdn.discordapp.com/attachments/805808631312023582/805809017624461312/4797c3873fe25139.jpg") \
            .set_footer(text="?돈받기 명령어를 사용해 회생해보세요"))

        elif userdata["Economy"]["money"] < betmoney:
            return await ctx.send(embed=discord.Embed(
                title="오류",
                description="베팅할 금액이 가진 돈보다 큽니다",
                color=0xFF0000
            ))

        if userdata["Economy"]["money"] == betmoney:
            allinalert = await ctx.send(embed=discord.Embed(
                title="경고",
                description=f"올인하여 가진 돈을 모두 잃을 경우 되돌릴 수 없습니다!\n계속 하시겠습니까?",
                color=0xFFAA00
            ))
            for emoji in ["\N{HEAVY LARGE CIRCLE}", "\N{CROSS MARK}"]:
                await allinalert.add_reaction(emoji)

            def check(reaction:discord.Reaction, user:discord.User):
                return user == ctx.author and str(reaction.emoji)

            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=30.0)
            except asyncio.TimeoutError:
                return await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="요청한 시간이 만료되었습니다",
                    color=0xFF0000
                ))

            if str(reaction.emoji) == "❌":
                return await ctx.send(embed=discord.Embed(
                    title="알림",
                    description="베팅이 취소되었습니다",
                    color=0x00FF00
                ))
            elif str(reaction.emoji) == "⭕️":
                await ctx.send(embed=discord.Embed(
                    title="알림",
                    description="올인합니다",
                    color=0x00FF00
                )) 

        multipleresult = random.choice(multiple)
        result = betmoney * multipleresult

        if not result == 0:
            userdata["Economy"]["money"] += result
        else:
            if (userdata["Economy"]["money"] - betmoney) < 0: 
                userdata["Economy"]["money"] = 0
            else: 
                userdata["Economy"]["money"] -= betmoney

        SimpleJSON.Write(f"{Path}/User/{ctx.author.id}.json", userdata)

        Embed = discord.Embed(
            title="결과",
            color=0x00FF00
        ) \
        .add_field( name="베팅 금액", value=f"`{betmoney}`원",       inline=False ) \
        .add_field( name="배수",      value=f"`{multipleresult}`배", inline=False ) 

        if result != 0:
            Embed.add_field( name="딴 돈", value=f"`{result}`", inline=False ) 
        else:
            Embed.add_field( name="잃은 돈", value=f"`{-betmoney}`", inline=False ) 

        Embed.add_field( name="잔고", value=f"`{int(userdata['Economy']['money'])}`원", inline=False )

        await ctx.reply(embed=Embed)
    
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
    