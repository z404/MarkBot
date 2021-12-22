# For Discord
import discord
from discord.ext import commands
# from discord_slash import cog_ext, SlashContext
from tabulate import tabulate


# Function to write into database
def write_db(db: dict) -> None:
    with open("database", 'w+') as file:
        file.write(str(db))


# Function to get database
def get_db() -> dict:
    with open('database') as file:
        return eval(file.read())


# Loading the config file
with open('config.json') as file:
    config = eval(file.read())


class Shrug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = get_db()

    @commands.group(name="shrug", pass_context=True)
    async def _shrug(self, ctx: commands.Context):
        """Command to manage a shrug channel"""
        if not ctx.invoked_subcommand:
            # TODO: Add help command here for shrug channel management
            pass

    @_shrug.command(pass_context=True, name="reset")
    async def _reset(self, ctx: commands.Context):
        '''Resets Shrug channel in a server'''
        def check_if_server_has_shrug(server_id):
            for i in self.db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True, i
            return False, None
        ret = check_if_server_has_shrug(ctx.guild.id)
        if ret[0]:
            del(self.db[ret[1]])
            write_db(self.db)
            await ctx.send("Successfully reset shrug channel!")
        else:
            await ctx.send("What's a shrug channel? I can't reset what I don't know. I'm not a supercomputer y'know")

    @_shrug.command(pass_context=True, name="set")
    async def _set(self, ctx: commands.Context, channel: discord.TextChannel):
        '''Set Shrug channel in a server'''
        def check_if_server_has_shrug(server_id):
            for i in self.db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True
            return False
        if check_if_server_has_shrug(ctx.guild.id):
            await ctx.send("This server already has a shrug channel! Type `!resetshrugchannel` to reset shrug channel settings for this server!")
        else:
            await ctx.send("Please wait while I figure out what a shrug means to humans")
            counter = 0
            message_count = {}
            async for message in channel.history(oldest_first=True, limit=None):
                if message.content == "¯\\_(ツ)_/¯" or repr(message.content) == r"'¯\\\\_(ツ)\\_/¯'":
                    try:
                        message_count[message.author.id] += 1
                    except:
                        message_count[message.author.id] = 1
            self.db[str(ctx.guild.id)+str(channel.id) +
                    'shrugchan'] = message_count
            write_db(self.db)
            await ctx.send("Shrug channel is now configured!")

    @_shrug.command(pass_context=True, name="leaderboard")
    async def _leaderboard(self, ctx: commands.Context):
        '''Displays a shrug leaderboard for the server'''
        def check_if_server_has_shrug(server_id):
            for i in self.db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True, i
            return False, None
        ret = check_if_server_has_shrug(ctx.guild.id)
        if ret[0]:
            leaderdata = self.db[ret[1]]
            X = list(leaderdata.keys())
            Y = list(leaderdata.values())
            userlst = [x for _, x in sorted(zip(Y, X))]
            userlst.reverse()
            finaldict = []
            for i in userlst:
                finaldict.append(
                    [str(ctx.guild.get_member(i)), str(leaderdata[i])])
            headers = ["User", "Shrugs"]
            table = tabulate(finaldict, headers, tablefmt="fancy_grid")
            # await ctx.send("Leaderboard:\n```"+table+"```")
            desc = "```yaml\n"+table+"```\n Total shrugs: "+str(sum(Y))
            embed = discord.Embed(title="Leaderboard",
                                  description=desc, color=0x00ff00)
            await ctx.send(embed=embed)
            # await ctx.send(str(leaderdata))
        else:
            await ctx.send("No shrug channel has been set! Set a shrug channel by typing `!setshrugchannel`")

    # @cog_ext.cog_subcommand(name="reset", base="shrug")
    # async def _reset_slash(self, ctx: SlashContext):
    #     '''Resets Shrug channel in a server'''
    #     def check_if_server_has_shrug(server_id):
    #         for i in self.db.keys():
    #             if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
    #                 return True, i
    #         return False, None
    #     ret = check_if_server_has_shrug(ctx.guild.id)
    #     if ret[0]:
    #         del(self.db[ret[1]])
    #         write_db(self.db)
    #         await ctx.send("Successfully reset shrug channel!")
    #     else:
    #         await ctx.send("What's a shrug channel? I can't reset what I don't know. I'm not a supercomputer y'know")

    # @cog_ext.cog_subcommand(name="set", base="shrug")
    # async def _set_slash(self, ctx: SlashContext, channel: discord.TextChannel):
    #     '''Set Shrug channel in a server'''
    #     def check_if_server_has_shrug(server_id):
    #         for i in self.db.keys():
    #             if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
    #                 return True
    #         return False
    #     if check_if_server_has_shrug(ctx.guild.id):
    #         await ctx.send("This server already has a shrug channel! Type `!resetshrugchannel` to reset shrug channel settings for this server!")
    #     else:
    #         await ctx.send("Please wait while I figure out what a shrug means to humans")
    #         counter = 0
    #         message_count = {}
    #         async for message in channel.history(oldest_first=True, limit=None):
    #             if message.content == "¯\\_(ツ)_/¯" or repr(message.content) == r"'¯\\\\_(ツ)\\_/¯'":
    #                 try:
    #                     message_count[message.author.id] += 1
    #                 except:
    #                     message_count[message.author.id] = 1
    #         self.db[str(ctx.guild.id)+str(channel.id) +
    #                 'shrugchan'] = message_count
    #         write_db(self.db)
    #         await ctx.send("Shrug channel is now configured!")

    # @cog_ext.cog_subcommand(name="leaderboard", base="shrug")
    # async def _leaderboard_slash(self, ctx: SlashContext):
    #     '''Displays a shrug leaderboard for the server'''
    #     def check_if_server_has_shrug(server_id):
    #         for i in self.db.keys():
    #             if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
    #                 return True, i
    #         return False, None
    #     ret = check_if_server_has_shrug(ctx.guild.id)
    #     if ret[0]:
    #         leaderdata = self.db[ret[1]]
    #         X = list(leaderdata.keys())
    #         Y = list(leaderdata.values())
    #         userlst = [x for _, x in sorted(zip(Y, X))]
    #         userlst.reverse()
    #         finaldict = []
    #         for i in userlst:
    #             finaldict.append(
    #                 [str(ctx.guild.get_member(i)), str(leaderdata[i])])
    #         headers = ["User", "Shrugs"]
    #         table = tabulate(finaldict, headers, tablefmt="fancy_grid")
    #         # await ctx.send("Leaderboard:\n```"+table+"```")
    #         desc = "```yaml\n"+table+"```\n Total shrugs: "+str(sum(Y))
    #         embed = discord.Embed(title="Leaderboard",
    #                               description=desc, color=0x00ff00)
    #         await ctx.send(embed=embed)
    #         # await ctx.send(str(leaderdata))
    #     else:
    #         await ctx.send("No shrug channel has been set! Set a shrug channel by typing `!setshrugchannel`")


def setup(bot):
    bot.add_cog(Shrug(bot))
