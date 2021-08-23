# For Discord
import discord
from discord.ext import commands


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


class AdminControls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

    @commands.command(hidden=True)
    async def terminate(self, ctx: commands.Context):
        await ctx.send("It's getting dark.. Maybe I'll take a little nap..")
        await self.bot.close()

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

    @_changestatus.before_invoke
    @changenick.before_invoke
    @terminate.before_invoke
    async def ensure_admin(self, ctx: commands.Context):
        if str(ctx.message.author.id) not in config['admin_list']:
            await ctx.send("I don't need to listen to you! you aren't an admin!")
            raise commands.CommandError("Unauthorised command used!")


def setup(bot):
    bot.add_cog(AdminControls(bot))
