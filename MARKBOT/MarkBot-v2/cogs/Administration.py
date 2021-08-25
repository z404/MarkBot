# For Discord
from os import popen
import discord
from discord.ext import commands
from subprocess import Popen


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
        self.node_server = Popen(
            "npm start", shell=True, cwd="./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity")

    # Logging system
    @commands.Cog.listener()
    async def on_command(self, ctx):
        logchannel = self.bot.get_channel(int(config['log-channel']))
        try:
            await logchannel.send(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            await logchannel.send(f"Private message > {ctx.author} > {ctx.message.clean_content}")

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
        self.node_server.kill()
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

    # Check if the user is admin before the execution of the above commands
    @_changestatus.before_invoke
    @changenick.before_invoke
    @terminate.before_invoke
    async def ensure_admin(self, ctx: commands.Context):
        if str(ctx.message.author.id) not in config['admin_list']:
            await ctx.send("I don't need to listen to you! you aren't an admin!")
            raise commands.CommandError("Unauthorised command used!")


def setup(bot):
    bot.add_cog(AdminControls(bot))
