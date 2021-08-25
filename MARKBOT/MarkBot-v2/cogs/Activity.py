# For Discord
from discord.ext import commands


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


class _Activity(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="activity", pass_context=True)
    async def _activity(self, ctx: commands.Context):
        """Command to launch activities. These activities are in beta, they might not work well"""
        if not ctx.invoked_subcommand:
            await ctx.send_help("activity")

    @_activity.command(pass_context=True, name="youtube")
    async def _youtube(self, ctx: commands.Context):
        """Command to launch the Youtube Together activity"""
        pass

    @_activity.command(pass_context=True, name="poker")
    async def _poker(self, ctx: commands.Context):
        """Command to launch the Poker Night activity"""
        pass

    @_activity.command(pass_context=True, name="chess")
    async def _chess(self, ctx: commands.Context):
        """Command to launch the Chess in the Park activity"""
        pass

    @_activity.command(pass_context=True, name="fishington")
    async def _fishing(self, ctx: commands.Context):
        """Command to launch the Fishington.io activity"""
        pass

    @_activity.command(pass_context=True, name="betrayal")
    async def _betrayal(self, ctx: commands.Context):
        """Command to launch the Betrayal.io activity"""
        pass

    @_activity.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send('You are not connected to any voice channel.')
            raise commands.CommandError(
                'User Invoked activity command without being in a voice channel')


def setup(bot):
    bot.add_cog(_Activity(bot))
