import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash.model import SlashContext, SlashContext

class slashTest(commands.Cog):
    def __init__(self, client):
        if not hasattr(client, "slash"):
            client.slash = SlashCommand(bot, override_type=True)
        self.client = client
        self.client.slash.get_cog_commands(self)
    
    def cog_unload(self):
        self.client.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="slashTest")
    async def slashTest(self, ctx:SlashContext):
        await ctx.send(content="slashTest!")

def setup(client):
    client.add_cog(slashTest(client))