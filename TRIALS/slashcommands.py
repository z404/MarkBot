
with open('config.json') as file:
    config = eval(file.read())

from discord.ext import commands
from dislash import InteractionClient

bot = commands.Bot(command_prefix="!")
inter_client = InteractionClient(bot)


@inter_client.slash_command(description="Sends Hello")
async def hello(interaction):
    await interaction.reply("Hello!")

bot.run(config['discord_token'], bot=True, reconnect=True)
