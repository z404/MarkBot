# For Discord
from code import interact
from os import popen
import discord
from discord.ext import commands
# from discord_slash import cog_ext, SlashContext
import tabulate
import psutil
import datetime
import traceback
# Function to write into database


def write_db(db: dict) -> None:
    with open("database", 'w+') as file:
        file.write(str(db))


# Function to get database
def get_db() -> dict:
    with open('database') as file:
        return eval(file.read())


# Function to get config file
with open('config.json') as file:
    config = eval(file.read())


# Cog for admin controld
class AdminControls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.now()

    # Error logging system
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        errorlogchannel = self.bot.get_channel(
            int(config['error-log-channel']))
        
        if ctx.message.clean_content.startswith(config['prefix']):
            try:
                await errorlogchannel.send(f"`{ctx.author}` has used the command `{ctx.message.clean_content}` with the following error: \n```py\n{error}``` in server {ctx.guild.name}")
            except AttributeError:
                await errorlogchannel.send(f"`{ctx.author}` has used the command `{ctx.message.clean_content}` with the following error: \n```py\n{error}``` in Private Message")
        else:
            command_with_options = ctx.interaction.data['name']
            try:
                for i in ctx.interaction.data['options']:
                    if "options" in i.keys():
                        command_with_options += ' ['+str(i['name']) + ': ' + \
                            str(list([str(x['value']) for x in i["options"]]))+']'
                    elif "value" in i.keys():
                        command_with_options += ' [' + \
                            str(i['name'])+": "+str(i['value'])+']'
                    else:
                        command_with_options += ' ['+str(i['name'])+"]"
            except KeyError:
                pass
            errorlogchannel = self.bot.get_channel(
                int(config['error-log-channel']))
            
            try:
                await errorlogchannel.send(f"{ctx.author} has used the SLASH command `{command_with_options}` with the following error: \n```py\n{error}``` in server {ctx.guild.name}")
            except AttributeError:
                await errorlogchannel.send(f"{ctx.author} has used the SLASH command `{command_with_options}` with the following error: \n```py\n{error}``` in Private Message")
        tb = traceback.format_exception(
            type(error), error, error.__traceback__)
        trace = (''.join([i.replace("`", "") for i in tb]))
        await errorlogchannel.send(f"```py\n{trace}```")

    # Logging system
    @commands.Cog.listener()
    async def on_command(self, ctx):
        logchannel = self.bot.get_channel(int(config['log-channel']))
        if ctx.message.clean_content.startswith(config['prefix']):
            try:
                await logchannel.send(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
            except AttributeError:
                await logchannel.send(f"Private Message > {ctx.author} > {ctx.message.clean_content}")
        else:
            command_with_options = ctx.interaction.data['name']
            try:
                for i in ctx.interaction.data['options']:
                    if "options" in i.keys():
                        command_with_options += ' ['+str(i['name']) + ': ' + \
                            str(list([str(x['value']) for x in i["options"]]))+']'
                    elif "value" in i.keys():
                        command_with_options += ' [' + \
                            str(i['name'])+": "+str(i['value'])+']'
                    else:
                        command_with_options += ' ['+str(i['name'])+"]"
            except KeyError:
                pass
            logchannel = self.bot.get_channel(int(config['log-channel']))
            try:
                await logchannel.send(f"[Slash] {ctx.guild.name} > {ctx.author} > {command_with_options}")
            except AttributeError:
                await logchannel.send(f"Private message > {ctx.author} > {command_with_options}")

    # Command to reload cogs
    @commands.command(pass_context=True, hidden=True, name="reloadcog")
    async def reloadcog(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    # Command to change someone's nickname in a server, if they are not the owner of the server
    @commands.command(pass_context=True, hidden=True)
    async def changenick(self, ctx: commands.Context, member, *newnick):
        '''Changes nickname of any user, if the user is below the bot and if sender has admin perms'''
        newnick = " ".join(list(newnick))
        await ctx.message.delete()
        if '<' in member:
            member = ctx.message.guild.get_member(int(member.strip('<@!>')))
        else:
            member = ctx.message.guild.get_member(int(member))
        await member.edit(nick=newnick)

    # Command to kill the bot
    @commands.command(hidden=True)
    async def terminate(self, ctx: commands.Context):
        await ctx.send("It's getting dark.. Maybe I'll take a little nap..")
        await self.bot.close()

    # Command to change status of the bot
    @commands.command(name='changestatus', aliases=['chst'], hidden=True)
    async def _changestatus(self, ctx: commands.Context, typeofstatus, *message):
        '''Changes the bot\'s status to the given parameters'''
        message = ' '.join(message)
        if typeofstatus.lower() == 'playing':
            await self.bot.change_presence(activity=discord.Game(message))
        elif typeofstatus.lower() == 'watching':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))
        elif typeofstatus.lower() == 'listeningto':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        elif typeofstatus.lower() == 'streaming':
            if 'twitch' not in message.split()[-1]:
                await ctx.send('Please provide a twitch url')
            else:
                await self.bot.change_presence(activity=discord.Streaming(name=' '.join(message.split()[:-1]), url=message.split()[-1]))
        elif typeofstatus.lower() == 'online':
            await self.bot.change_presence(status=discord.Status.online)
        elif typeofstatus.lower() == 'idle':
            await self.bot.change_presence(status=discord.Status.idle)
        elif typeofstatus.lower() == 'dnd':
            await self.bot.change_presence(status=discord.Status.dnd)
        else:
            await ctx.send('Wrong format! format = <type> <message> <url (for stream)> Choose type from ["playing","watching","listeningto","streaming"]. You can also set status as ["online","idle","dnd"]')

    # Command to change status of the bot
    @commands.command(name='botstats', hidden=True)
    async def _botstats(self, ctx: commands.Context):
        '''Shows the bot\'s stats'''
        # create channel with channel id
        channel = self.bot.get_channel(int(config['log-channel']))
        count_log = 0
        async with ctx.typing():
            async for message in channel.history(oldest_first=True, limit=None):
                if message.author == self.bot.user:
                    count_log = count_log + 1
        # create an embed
        embed = discord.Embed(
            title="Bot Stats", description="Displays all stats of the bot")
        embed.add_field(name="Ping", value="The bot's ping is {}ms".format(
            round(self.bot.latency * 1000)), inline=False)
        embed.add_field(
            name="Uptime", value=f"{datetime.datetime.now() - self.start_time}", inline=False)
        embed.add_field(name="Servers and members", value="Server count: {}\nMember count: {}".format(
            len(self.bot.guilds), sum([len(x.members) for x in self.bot.guilds])), inline=False)
        embed.add_field(name="Commands", value="Command count: {}".format(
            count_log))
        embed.add_field(name="Computer Stats", value="CPU Usage: {}%\nRAM Usage: {}%".format(
            psutil.cpu_percent(), psutil.virtual_memory().percent), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="serverstats", hidden=True)
    async def _serverstats(self, ctx: commands.Context, page: int = 1):
        heading = [["Name", "Members", "Owner"]]
        list_of_servers = []
        for server in self.bot.guilds:
            list_of_servers.append([server.name, len(
                server.members), server.owner])
        total_servers = len(list_of_servers)
        total_members = sum([x[1] for x in list_of_servers])
        pages = int(len(list_of_servers) / 5)
        if page > pages+1 or page < 1:
            await ctx.send("Page does not exist")
        else:
            # embed = discord.Embed(
            # title="Server Stats", description="Displays all stats of the bot")
            heading.extend(list_of_servers[(page-1)*5:page*5])
            tabulate_list = tabulate.tabulate(heading, tablefmt="fancy_grid")
            # embed.add_field(name="Totals", value="Total servers: {}\nTotal members: {}".format(
            # total_servers, total_members), inline=False)
            # embed.add_field(name="Page {}/{}".format(page, pages+1),
            #                 value="```"+tabulate_list+"```", inline=False)
            # await ctx.send(embed=embed)
            await ctx.send(("**Server Stats**\nTotal servers: {}\nTotal members: {} \n\n**Page {}/{} **```"+tabulate_list+"```").format(total_servers, total_members, page, pages+1))
        # tabletext = tabulate.tabulate(
        #     list_of_servers, headers="firstrow", tablefmt="fancy_grid")

    # Check if the user is admin before the execution of the above commands
    @_botstats.before_invoke
    @_serverstats.before_invoke
    @_changestatus.before_invoke
    @changenick.before_invoke
    @terminate.before_invoke
    @reloadcog.before_invoke
    async def ensure_admin(self, ctx: commands.Context):
        if str(ctx.message.author.id) not in config['admin_list']:
            await ctx.send("I don't need to listen to you! you aren't an admin!")
            raise commands.CommandError("Unauthorised command used!")


async def setup(bot):
    await bot.add_cog(AdminControls(bot))
