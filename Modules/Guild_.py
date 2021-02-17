import os
import discord
from discord.ext import commands
import json
import os.path
import time
import SimpleJSON

Path = "/DaeGal/Data/Guild/"

class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="출석테스트")
    @commands.guild_only()
    async def attendance(self, ctx: commands.Context, *, comment=None):
        DataPath = f"/DaeGal/Data/Guild/{ctx.guild.id}/Members"
        DataFile = f"{DataPath}/attendanceList.json"
        AttendanceData = SimpleJSON.Read(DataFile)

        os.makedirs(DataPath, exist_ok=True)
        if comment is not None:
            comment = f"\n\n> {comment}"
        if comment is None:
            comment = " "
        
        try:
            with open(DataFile, 'x') as FileIO:
                obj = {
                    f"{ctx.author.id}": {
                        "count": 1,
                        "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime())
                    }
                }
                json.dump(fp=FileIO, obj=obj, indent=4)
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {obj[str(ctx.author.id)]['count']}회 입니다 {comment}",
                    color=0x00FF00
                )
                # 버그를 확인할 수 있도록 1회 -> obj[str(ctx.author.id)]['count']로 수정
                await ctx.send(embed=Embed)
            
            if time.strftime(r"%Y-%m-%d", time.localtime()) == AttendanceData[f"{ctx.author.id}"]["lastAttendance"]:
                Embed = discord.Embed(
                    title="이미 출석했습니다",
                    description="하루에 한 번만 출석할 수 있습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
            else:
                AttendanceData[f"{ctx.author.id}"]["lastAttendance"] = time.strftime(r"%Y-%m-%d", time.localtime())
                AttendanceData[f"{ctx.author.id}"]["count"] += 1
                SimpleJSON.BackupWrite(DataFile, AttendanceData)
                usrAtCnt = AttendanceData[f"{ctx.author.id}"]['count']
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {usrAtCnt}회 입니다{comment}",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)
        except KeyError:
            FileData = SimpleJSON.Read(DataFile)
            FileData.update({
                f"{ctx.author.id}": {
                    "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime()),
                    "count": 1
                }
            })
            SimpleJSON.BackupWrite(DataFile, FileData)
            Embed = discord.Embed(
                title="✅",
                description=f"현재 {ctx.author}님의 출석 횟수는 {FileData[str(ctx.author.id)]['count']}회 입니다 {comment}",
                color=0x00FF00
            )
            # 버그를 확인할 수 있도록 1회 -> obj[str(ctx.author.id)]['count']로 수정
            await ctx.send(embed=Embed)

    @commands.command(name="출석__")
    @commands.guild_only()
    async def attendance(self, ctx: commands.Context, *, comment=None):
        DataPath = f"/DaeGal/Data/Guild/{ctx.guild.id}/Members"
        DataFile = f"{DataPath}/attendanceList.json"
        AttendanceData = SimpleJSON.Read(DataFile)[f"{ctx.author.id}"]

        os.makedirs(DataPath, exist_ok=True)
        if comment is not None:
            comment = f"\n\n> {comment}"
        if comment is None:
            comment = ""

        try:
            if time.strftime(r"%Y-%m-%d", time.localtime()) == AttendanceData["lastAttendance"]:
                Embed = discord.Embed(
                    title="이미 출석했습니다",
                    description="하루에 한 번만 출석할 수 있습니다",
                    color=0xFF0000
                )
                await ctx.send(embed=Embed)
            else:
                AttendanceData["lastAttendance"] = time.strftime(r"%Y-%m-%d", time.localtime())
                AttendanceData["count"] += 1
                SimpleJSON.BackupWrite(DataFile, AttendanceData)
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 {AttendanceData['count']}회 입니다 {comment}",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)

        except KeyError:
            # FileData = {}
            # with open(DataFile, "r") as FileIO:
            #     FileData = json.load(fp=FileIO)
            #     FileData.update({ f"{ctx.author.id}": { "count": 1, "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime()) }})
            # with open(DataFile, "w") as dFile:
            #     json.dump(fp=dFile, obj=FileData, indent=4)
            FileData = SimpleJSON.Read(DataFile)
            FileData.update({
                f"{ctx.author.id}": {
                    "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime()),
                    "count": 1
                }
            })
            SimpleJSON.BackupWrite(DataFile, FileData)
            Embed = discord.Embed(
                title="✅",
                description=f"현재 {ctx.author}님의 출석 횟수는 1회 입니다 {comment}",
                color=0x00FF00
            )
            await ctx.send(embed=Embed)
        except FileNotFoundError:
            with open(DataFile, "w") as FileIO:
                obj = {
                    f"{ctx.author.id}": {
                        "count": 1,
                        "lastAttendance": time.strftime(r"%Y-%m-%d", time.localtime())
                    }
                }
                json.dump(fp=FileIO, obj=obj, indent=4)
                Embed = discord.Embed(
                    title="✅",
                    description=f"현재 {ctx.author}님의 출석 횟수는 1회 입니다 {comment}",
                    color=0x00FF00
                )
                await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(Guild(client))
