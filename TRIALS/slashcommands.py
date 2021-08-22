from discord.ext import commands
import discord
from discord_slash import SlashCommand

with open('config.json') as file:
    config = eval(file.read())

bot = commands.Bot(
    command_prefix=config['prefix'], description='An easy to use multipurpose Discord bot!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("Bot is online!")


@slash.slash(name="ping")
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

bot.run(config['discord_token'], bot=True, reconnect=True)
