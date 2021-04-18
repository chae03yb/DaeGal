import discord
from discord.ext import commands
import DaeGal_Utils
import SimpleJSON

Path = "/DaeGal/Data"

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="유저등록")
    async def addUser(self, ctx:commands.Context):
        pass

    # SID: JSON 파일 불러온 후 len(JSONDict) 앞 000으로 채움.

def setup(client):
    client.add_cog(User(client))