from discord.ext import commands
import discord
from pathlib import Path
from discord_slash import SlashCommand, SlashContext

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

initial_extensions = ['cogs.Functionality',
                      'cogs.Administration',
                      'cogs.Music',
                      'cogs.Activity']

bot = commands.Bot(
    command_prefix=config['prefix'], description='An easy to use multipurpose Discord bot!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Bot is online!")

bot.run(config['discord_token'], bot=True, reconnect=True)
