from os import name
import discord
from discord.ext import commands
from discord.ext.commands import cog
from discord_slash import cog_ext, SlashContext
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

    @commands.has_permissions(manage_messages=True)
    @commands.group(name="cleanup", pass_context=True)
    async def _cleanup(self, ctx: commands.Context):
        """Commands to cleanup a text channel."""
        if not ctx.invoked_subcommand:
            await ctx.send_help("cleanup")

    @_cleanup.error
    async def _error_handler(self, ctx: commands.Context, error):
        await ctx.send("You don't have the permissions to use this command! :)")

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
        await ctx.message.delete()
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        msg = await ctx.send(f'This channel {grammar} {choice}')
        sleep(3)
        await msg.delete()

    @_cleanup.command(pass_context=True, name="people")
    async def _people(self, ctx: commands.Context, which_person: discord.Member = None, number_of_people: int = None):
        """Delete last 100 messages by people.
            Provide mention of specific specific people(optional)"""
        if number_of_people == None:
            number_of_people = 100
        if which_person == None:
            def is_undesired(message):
                return message.author.bot == False
            await ctx.channel.purge(limit=number_of_people, check=is_undesired)
        else:
            def is_undesired(message):
                return message.author == which_person and not (message.author.bot)
            await ctx.channel.purge(limit=number_of_people, check=is_undesired)
        await ctx.message.delete()
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        msg = await ctx.send(f'This channel {grammar} {choice}')
        sleep(3)
        await msg.delete()

    @_cleanup.command(pass_context=True, name="purge")
    async def _purge(self, ctx: commands.Context, num: int = None):
        """Delete last 100 messages."""
        await ctx.channel.purge(limit=num+1 if num != None else 101)
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        msg = await ctx.send(f'This channel {grammar} {choice}')
        sleep(3)
        await msg.delete()

    @commands.has_permissions(manage_messages=True)
    @cog_ext.cog_subcommand(name="commands", base="cleanup")
    async def _commands_slash(self, ctx: SlashContext, which_prefix: str = None):
        """Delete all messages that are bot commands.
            Provide specific prefixes to target(optional)"""
        if which_prefix == None:
            which_prefix = "! . ? ' ("
        which_prefix = [i for i in which_prefix if i != ' ']

        def is_undesired(message):
            prefixes = which_prefix if len(
                which_prefix) > 0 else "! . ? ' (".split()
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
        await ctx.send(f'This channel {grammar} {choice}', hidden=True)

    @commands.has_permissions(manage_messages=True)
    @cog_ext.cog_subcommand(name="bots", base="cleanup")
    async def _bots_slash(self, ctx: SlashContext, which_bot: discord.Member = None):
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
        # await ctx.message.delete()
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        await ctx.send(f'This channel {grammar} {choice}', hidden=True)

    @commands.has_permissions(manage_messages=True)
    @cog_ext.cog_subcommand(name="people", base="cleanup")
    async def _people_slash(self, ctx: SlashContext, which_person: discord.Member = None, number_of_messages: int = None):
        """Delete last 100 messages by people.
            Provide mention of specific specific people(optional)"""
        if number_of_messages == None:
            number_of_messages = 100
        if which_person == None:
            def is_undesired(message):
                return message.author.bot == False
            await ctx.channel.purge(limit=number_of_messages, check=is_undesired)
        else:
            def is_undesired(message):
                return message.author == which_person and not (message.author.bot)
            await ctx.channel.purge(limit=number_of_messages, check=is_undesired)
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        await ctx.send(f'This channel {grammar} {choice}', hidden=True)

    @commands.has_permissions(manage_messages=True)
    @cog_ext.cog_slash(name="purge")
    async def _purge_slash(self, ctx: commands.Context, num: int = None):
        """Deletes last 100 messages."""
        await ctx.channel.purge(limit=num+1 if num != None else 101)
        ways_to_clean = [
            "washed", "scrubbed", "cleansed", "cleaned", "polished", "spotless",
            "usoiled", "unstained", "unspotted", "unsullied", "unblemished", "immaculate", "pristine"
        ]
        choice = random.choice(ways_to_clean)
        grammar = "has been" if choice[-2:] == "ed" else "is now"
        await ctx.send(f'This channel {grammar} {choice}', hidden=True)

    @_commands_slash.error
    @_bots_slash.error
    @_people_slash.error
    @_purge_slash.error
    async def _error_handler(self, ctx: SlashContext, error):
        await ctx.send("You don't have the permissions for this command")


def setup(bot):
    bot.add_cog(Cleanup(bot))
