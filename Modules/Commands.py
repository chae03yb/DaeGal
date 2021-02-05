from discord.ext import commands
import CustomCommands as cmd

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cmd.CustomCommands.shell.command(name = "write")
    async def write(self, ctx: commands.Context, *, msg: str):
        await ctx.send(msg)

def setup(client):
    client.add_cog(Commands(client))