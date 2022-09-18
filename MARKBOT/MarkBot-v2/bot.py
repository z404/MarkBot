from discord.ext import commands
import discord
from discord import app_commands
from pathlib import Path
from subprocess import Popen
import os
from shutil import copyfile
import asyncio

l = '''
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
'''
print(l)

with open('config.json') as file:
    config = eval(file.read())

if not Path('database').is_file():
    with open('database', 'w+') as file:
        file.write('{}')

initial_extensions = ['cogs.Music',
                      'cogs.Functionality',
                      'cogs.Administration',
                      'cogs.Activity',
                      'cogs.Cleanup',
                      'cogs.Shrug',
                      'cogs.ReactionRoles',
                      'cogs.VoiceListener']

bot = commands.Bot(
    command_prefix=config['prefix'], description='An easy to use multipurpose Discord bot!', intents=discord.Intents.all())

if __name__ == '__main__':
    async def setup():
        for extension in initial_extensions:
            print(extension)
            await bot.load_extension(extension)

    asyncio.get_event_loop().run_until_complete(setup())



if not os.path.isdir("./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/config.json"):
    copyfile("config.json", "./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/config.json")

node_server = Popen("npm start", shell=True,
                    cwd="./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online!")

bot.run(config['discord_token'], reconnect=True)
