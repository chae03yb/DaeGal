import discord
from discord.ext import commands
import asyncio

class Others(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command(name = "vote", aliases = ["투표"])
    async def makeVote(self, ctx: commands.Context, itemAmount: int, *, description = None):
        itemList = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        waitTime = 5.0
        maxItemErrMsg = f"투표 항목은 최대 {len(itemList)}개입니다.\n\n{int(waitTime)}초 후 이 메시지와 사용된 명령은 삭제됩니다."
        minItemErrMsg = f"투표 항목은 최소 2개 이상이어야 합니다.\n\n{int(waitTime)}초 후 이 메시지와 사용된 명령은 삭제됩니다."
        emptyErrMsg = f"내용을 적어주세요\n\n{int(waitTime)}초 후 이 메시지와 사용된 명령은 삭제됩니다."

        async def sleepAndDelete(ctx):
            def check(ctx: commands.Context):
                return ctx.message.content == maxItemErrMsg or minItemErrMsg or emptyErrMsg
            await asyncio.sleep(waitTime)
            await ctx.channel.purge(limit = 35, check=check)

        if itemAmount > len(itemList):
            await ctx.channel.send(maxItemErrMsg)
            await sleepAndDelete(ctx=ctx)
        elif itemAmount < 2:
            await ctx.channel.send(minItemErrMsg)
            await sleepAndDelete(ctx=ctx)
        if description is None:
            await ctx.channel.send(emptyErrMsg)
            await sleepAndDelete(ctx=ctx) 
        else:
            def check(ctx: commands.Context):
                return ctx.message.content == description
            await ctx.channel.purge(limit=3, check=check)
            Embed = discord.Embed(
                color=0x000000,
                title="투표",
                description=f"작성자: {ctx.message.author}"
            )
            Embed.add_field(name=f"투표 항목: {itemAmount}", value=description, inline=False)
            msg = await ctx.channel.send(embed=Embed)

            for i in range(0, itemAmount):
                await msg.add_reaction(itemList[i])

    # @commands.command(name="timer", aliases=["타이머"])
    async def timer(self, ctx:commands.Context, time=None):
        if time is None:
            Embed = discord.Embed(
                title="오류",
                description="시간을 입력해주세요",
                color=0xFF0000
            )
            await ctx.send(embed=Embed)
        
        asyncio.sleep()

    @commands.command(name="echo", aliases=["따라하기", "말하기"])
    async def echo(self, ctx:commands.Context, *, args):
        await ctx.reply(args)

def setup(client):
    client.add_cog(Others(client))
