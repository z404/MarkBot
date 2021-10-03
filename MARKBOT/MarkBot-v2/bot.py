from discord.ext import commands
import discord
from pathlib import Path
from discord_slash import SlashCommand, SlashContext
from subprocess import Popen
import os
from shutil import copyfile

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
                      'cogs.Shrug']

bot = commands.Bot(
    command_prefix=config['prefix'], description='An easy to use multipurpose Discord bot!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

if not os.path.isdir("./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/config.json"):
    copyfile("config.json", "./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/config.json")

node_server = Popen("npm start", shell=True,
                    cwd="./MARKBOT/MarkBot-v2/cogs/MarkBot-Activity")


@ bot.event
async def on_ready():
    print("Bot is online!")

bot.run(config['discord_token'], bot=True, reconnect=True)
