import asyncio
import os
from pathlib import Path
from shutil import copyfile
from subprocess import Popen

import discord
from discord import app_commands
from discord.ext import commands

l = """
 ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
 ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
 ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║
 ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║
 ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║
 ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝

             ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗
             ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝
             ██╔████╔██║███████║██████╔╝█████╔╝
             ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
             ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗
             ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""
print(l)

with open("config.json") as file:
    config = eval(file.read())

if not Path("database").is_file():
    with open("database", "w+") as file:
        file.write("{}")

initial_extensions = [
    "cogs.Music",
    "cogs.Functionality",
    "cogs.Administration",
    "cogs.Activity",
    "cogs.Cleanup",
    "cogs.Shrug",
    "cogs.ReactionRoles",
    "cogs.VoiceListener",
]

bot = commands.Bot(
    command_prefix=config["prefix"],
    description="An easy to use multipurpose Discord bot!",
    intents=discord.Intents.all(),
)

if __name__ == "__main__":

    async def setup():
        for extension in initial_extensions:
            print(extension)
            await bot.load_extension(extension)

    asyncio.get_event_loop().run_until_complete(setup())


node_server = Popen("npm start", shell=True, cwd="./cogs/MarkBot-Activity")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online!")


bot.run(config["discord_token"], reconnect=True)
