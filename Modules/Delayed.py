# Guild.py
class Guild:
    # @commands.command(name="setWelcomeMsg")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setWelcomeMsg(self, ctx: commands.Context, option=None):
        if option == "del":
            os.remove(f"{Path}/{ctx.guild.id}/Welcome/Msg")
            await ctx.send("삭제 완료")
        try:
            async def setMessage(msg):
                return msg.message.content and msg.message.author == ctx.message.author

            Embed = discord.Embed(
                title="환영 메세지의 내용을 입력해주세요"
            )
            await ctx.send(embed=Embed)
            Message = await self.client.wait_for(event="message", timeout=500.0, check=setMessage)
        except asyncio.TimeoutError:
            await ctx.send("시간 초과")
        else:
            if Message == "None":
                return await ctx.send("설정을 종료합니다")
            try:
                with open(f"{Path}/{ctx.guild.id}/Welcome/Message", "w") as File:
                    File.write(Message)
                    await ctx.send("메세지 설정 완료")
            except Exception as E:
                Embed = discord.Embed(
                    title="오류",
                    description=f"```{E}```",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)

