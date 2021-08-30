from os import popen
import discord
from discord.ext import commands
from time import sleep
import random


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
class Cleanup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="cleanup", pass_context=True)
    async def _cleanup(self, ctx: commands.Context):
        """Commands to cleanup a text channel."""
        if not ctx.invoked_subcommand:
            await ctx.send_help("cleanup")

    @_cleanup.command(pass_context=True, name="commands")
    async def _commands(self, ctx: commands.Context, *which_prefix):
        """Delete all messages that are bot commands.
            Provide specific prefixes to target(optional)"""
        def is_undesired(message):
            prefixes = list(which_prefix) if len(
                list(which_prefix)) > 0 else "! . ? ' (".split()
            starts_with_prefix = None
            for i in prefixes:
                if message.content.startswith(i):
                    starts_with_prefix = i
                    break
            if starts_with_prefix:
                return True
            return False
        await ctx.channel.purge(limit=100, check=is_undesired)
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        msg = await ctx.send(f'This channel {grammar} {choice}')
        sleep(3)
        await msg.delete()

    @_cleanup.command(pass_context=True, name="bots")
    async def _bots(self, ctx: commands.Context, which_bot: discord.Member = None):
        """Delete all messages by bots.
            Provide mention of specific bot(optional)"""
        if which_bot == None:
            def is_undesired(message): return message.author.bot
            await ctx.channel.purge(limit=100, check=is_undesired)
        else:
            def is_undesired(message):
                return message.author == which_bot and message.author.bot
            await ctx.channel.purge(limit=100, check=is_undesired)
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        msg = await ctx.send(f'This channel {grammar} {choice}')
        sleep(3)
        await msg.delete()

    @_cleanup.command(pass_context=True, name="people", hidden=True)
    async def _people(self, ctx: commands.Context, which_person: discord.Member = None):
        """Delete last 100 messages by people.
            Provide mention of specific specific people(optional)"""
        if which_person == None:
            def is_undesired(message):
                return message.author.bot == False
            await ctx.channel.purge(limit=100, check=is_undesired)
        else:
            def is_undesired(message):
                return message.author == which_person and not (message.author.bot)
            await ctx.channel.purge(limit=100, check=is_undesired)
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        msg = await ctx.send(f'This channel {grammar} {choice}')
        sleep(3)
        await msg.delete()


def setup(bot):
    bot.add_cog(Cleanup(bot))
