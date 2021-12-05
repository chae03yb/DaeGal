import discord
from discord.ext import commands

import DaeGal_Utils
import SimpleJSON
import sqlite3

Path = "/DaeGal/Data"

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="register", aliases=["회원가입"])
    async def addUser(self, ctx:commands.Context):
        nextsid = DaeGal_Utils.getLastUserID(Path) + 1
        # DaeGal_Utils/createUser(discord_id) -> bool
        # if success: next
        # else: failed

        if DaeGal_Utils.existUser(Path, ctx.author.id):
            return await ctx.send(embed=discord.Embed(
                title="실패",
                description=f"이미 등록된 유저입니다",
                color=0xFF0000
            ))
        else:
            try:
                SimpleJSON.Read(f"{Path}/User/{ctx.author.id}.json")
            except FileNotFoundError:
                SimpleJSON.Write(f"{Path}/User/{ctx.author.id}.json", {})
            finally:
                try:
                    con: sqlite3.Connection = sqlite3.connect(f"{Path}/User/SIDList.sqlite3")
                    cur: sqlite3.Cursor     = con.cursor()

                    cur.execute("INSERT INTO User (USERID) VALUES (?);", [ ctx.author.id ])
                except Exception as E:
                    await ctx.send(embed=discord.Embed(
                        title="오류",
                        description=f"```{E}```",
                        color=0xFF0000
                    ))
                finally:
                    con.commit()
                    con.close()

                SimpleJSON.Update(f"{Path}/User/{ctx.author.id}.json", {
                    "serviceid": nextsid
                })

            await ctx.send(embed=discord.Embed(
                title="성공",
                description=f"유저를 성공적으로 등록하였습니다, 당신의 유저 번호는 `{nextsid}`입니다",
                color=0x00FF00
            ))

    # SID: JSON 파일 불러온 후 len(JSONDict) 앞 000으로 채움.

def setup(client):
    client.add_cog(User(client))