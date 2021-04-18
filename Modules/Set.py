import discord
from discord.ext import commands

import SimpleJSON

Path = "./Data"

class Set(commands.Cog): 
    def __init__(self, client):
        self.client = client

    @commands.group(name="set", aliases=["Set", "설정"])
    async def Set(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="설정할 항목이 필요합니다",
                color=0xFF0000
            ))
    
    ############################################
    #                   Guild                  #
    ############################################
    @Set.group(name="Guild")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def guildSet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="설정할 항목이 필요합니다",
                color=0xFF0000
            ))
    
    ############################################
    #                Guild/Role                #
    ############################################
    @guildSet.group(name="Role")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def guildRoleSet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="설정할 항목이 필요합니다",
                color=0xFF0000
            ))

    @guildRoleSet.command(name="Member")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def setMemberRole(self, ctx:commands.Context, role:discord.Role=None):
        Config: dict = None
        ConfigPath = f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json"

        try:
            SimpleJSON.Read(ConfigPath)["Role"]
        except FileNotFoundError:
            SimpleJSON.Write(ConfigPath, {"Role":{}})
        except KeyError:
            tmpData = SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")
            tmpData.update({"Role": {}})
            SimpleJSON.Write(ConfigPath, tmpData)
        finally:
            Config = SimpleJSON.Read(ConfigPath)

        if role is None: 
            try:
                del Config["Role"]["Member"]
            except KeyError:
                await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="멤버 역할이 설정되지 않았습니다",
                    color=0xFF0000
                ))
            else:
                SimpleJSON.Write(ConfigPath, Config)
                await ctx.send(embed=discord.Embed(
                    title="성공",
                    description="멤버 역할을 설정에서 삭제했습니다",
                    color=0x00FF00
                ))
        else:
            Config["Role"].update({ "Member": role.id })
            SimpleJSON.Write(ConfigPath, Config)

            await ctx.send(embed=discord.Embed(
                title="성공",
                description=f"멤버 역할을 {role.name} 으로 지정하였습니다",
                color=0x00FF00
            ))

    @guildRoleSet.command(name="Bot")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def setBotRole(self, ctx:commands.Context, role:discord.Role=None):
        Config: dict = None
        ConfigPath = f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json"

        try:
            SimpleJSON.Read(ConfigPath)["Role"]
        except FileNotFoundError:
            SimpleJSON.Write(ConfigPath, {"Role":{}})
        except KeyError:
            tmpData = SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")
            tmpData.update({"Role": {}})
            SimpleJSON.Write(ConfigPath, tmpData)
        finally:
            Config = SimpleJSON.Read(ConfigPath)

        if role is None: 
            try:
                del Config["Role"]["Bot"]
            except KeyError:
                await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="봇 역할이 설정되지 않았습니다",
                    color=0xFF0000
                ))
            else:
                SimpleJSON.Write(ConfigPath, Config)
                await ctx.send(embed=discord.Embed(
                    title="성공",
                    description="봇 역할을 설정에서 삭제했습니다",
                    color=0x00FF00
                ))
        else:
            Config["Role"].update({ "Bot": role.id })
            SimpleJSON.Write(ConfigPath, Config)

            await ctx.send(embed=discord.Embed(
                title="성공",
                description=f"봇 역할을 {role.name} 으로 지정하였습니다",
                color=0x00FF00
            ))

    @guildRoleSet.command(name="Punish")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def setPunishRole(self, ctx:commands.Context, role:discord.Role=None):
        Config: dict = None
        ConfigPath = f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json"

        try:
            SimpleJSON.Read(ConfigPath)["Role"]
        except FileNotFoundError:
            SimpleJSON.Write(ConfigPath, {"Role":{}})
        except KeyError:
            tmpData = SimpleJSON.Read(f"{Path}/Guild/{ctx.guild.id}/GuildConfig.json")
            tmpData.update({"Role": {}})
            SimpleJSON.Write(ConfigPath, tmpData)
        finally:
            Config = SimpleJSON.Read(ConfigPath)

        if role is None: 
            try:
                del Config["Role"]["Punish"]
            except KeyError:
                await ctx.send(embed=discord.Embed(
                    title="오류",
                    description="징벌 역할이 설정되지 않았습니다",
                    color=0xFF0000
                ))
            else:
                SimpleJSON.Write(ConfigPath, Config)
                await ctx.send(embed=discord.Embed(
                    title="성공",
                    description="징벌 역할을 설정에서 삭제했습니다",
                    color=0x00FF00
                ))
        else:
            Config["Role"].update({ "Punish": role.id })
            SimpleJSON.Write(ConfigPath, Config)

            await ctx.send(embed=discord.Embed(
                title="성공",
                description=f"징벌 역할을 {role.name} 으로 지정하였습니다",
                color=0x00FF00
            ))
    
    ############################################
    #              Guild/Channel               #
    ############################################
    @guildSet.group(name="Channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def guildChannelSet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="설정할 항목이 필요합니다",
                color=0xFF0000
            ))

    @guildChannelSet.command(name="Welcome")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def setWelcomeChannel(self, ctx:commands.Context, channel:discord.TextChannel=None, *, welcomemsg=None):
        pass

    @guildChannelSet.command(name="Notice")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def setNoticeChannel(self, ctx:commands.Context, channel:discord.TextChannel=None):
        pass

    ############################################
    #                   User                   #
    ############################################
    @Set.group(name="User")
    async def userSet(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(
                title="오류",
                description="설정할 항목이 필요합니다",
                color=0xFF0000
            ))

    @userSet.command(name="Profile")
    async def setProfile(self, ctx:commands.Context, *, comment=None):
        Profile: dict = None
        ProfilePath = f"{Path}/User/{ctx.author.id}.json"

        try:
            SimpleJSON.Read(ProfilePath)
        except FileNotFoundError:
            SimpleJSON.Write(ProfilePath, {})
        finally:
            Profile = SimpleJSON.Read(ProfilePath)

        if comment is None:
            try:
                del Profile["comment"]
            except KeyError:
                await ctx.send(embed=discord.Embed(
                    title="실패",
                    description="프로필 메세지가 설정되지 않았습니다",
                    color=0xFF0000
                ))
            else:
                SimpleJSON.Write(ProfilePath, Profile)
                await ctx.send(embed=discord.Embed(
                    title="성공",
                    description="프로필 메세지를 제거했습니다",
                    color=0x00FF00
                ))
        else:
            Profile["comment"] = comment
            SimpleJSON.Write(ProfilePath, Profile)
            await ctx.send(embed=discord.Embed(
                title="성공",
                description="프로필 메세지를 업데이트했습니다",
                color=0x00FF00
            ))

def setup(client):
    client.add_cog(Set(client))