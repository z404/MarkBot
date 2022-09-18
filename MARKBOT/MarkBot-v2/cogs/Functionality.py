# For Discord
import discord
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
# from discord_slash import cog_ext, SlashContext
# Api to interact with wikipedia
import wikipedia
# Api to interact with wolfram alpha
import wolframalpha
# Api to convert currency
from currency_converter import CurrencyConverter
# Api to beautify tables
from tabulate import tabulate
# Library to make request for url shortener
from urllib.request import urlopen

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


class Functionality(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        client = wolframalpha.Client(config["wolframalpha_key"])
        self.wolframclient = client
        self.db = get_db()

    # URL shortener
    @commands.command(name="tinify", pass_context=True)
    async def _tinify(self, ctx: commands.Context, url):
        """Command to shorten a url using tiny url"""
        apiurl = "http://tinyurl.com/api-create.php?url="
        tinyurl = await self.bot.loop.run_in_executor(None, lambda: urlopen(apiurl + url).read().decode("utf-8"))
        await ctx.send(tinyurl)

    @commands.command(aliases=['wikipedia'])
    async def wiki(self, ctx: commands.Context, *, searchmsg):
        '''Searches wikipedia and shows a summary of the search term'''
        try:
            async with ctx.typing():
                url = wikipedia.page(searchmsg)
                summary = wikipedia.summary(searchmsg, sentences=5)
                # await ctx.send(summary+'\n\nUrl = `'+str(url)+'`')
                embed = discord.Embed()
                embed.title = url.title
                embed.description = summary + \
                    '\n\n[Click here to read more]('+url.url+')'
                if url.images != None:
                    embed.set_image(url=url.images[0])
                await ctx.send(embed=embed)

        except wikipedia.exceptions.PageError:
            await ctx.send("Could not find a page with that search term")
        except wikipedia.exceptions.DisambiguationError:
            await ctx.send("Too many results. Please be more specific")

    @commands.command(aliases=['wolfram'])
    async def math(self, ctx: commands.Context, *, searchquery):
        '''Tries to solve a few basic math problems'''
        try:
            async with ctx.typing():
                res = self.wolframclient.query(searchquery)
            for i in res:
                # if i['@title'] == 'Result':
                #    await ctx.send(i['subpod']['img']['@src'])
                embed = discord.Embed()
                if i['@title'] == 'Input interpretation' or i['@title'] == 'Input':
                    embed.title = 'Input Interpretation:'
                    embed.set_image(url=i['subpod']['img']['@src'])
                    await ctx.send(embed=embed)
                elif i['@title'] == 'Result' or i['@title'] == 'Implicit plot' or i['@title'] == 'Plots' or i['@title'] == 'Surface plot' or i['@title'] == 'Volume of solid':
                    try:
                        embed.title = 'Result'
                        embed.set_image(url=i['subpod']['img']['@src'])
                        await ctx.send(embed=embed)
                    except:
                        embed.title = 'Result'
                        embed.set_image(url=i['subpod'][0]['img']['@src'])
                        await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send('Something went wrong. (Math is in beta) '+str(e))

    @commands.command(name='currency_converter', aliases=['currconv'])
    async def _currency_converter(self, ctx: commands.Context, value: int, frm: str, to: str):
        '''Converts currency from one unit to another'''
        c = CurrencyConverter()
        try:
            newvalue = c.convert(value, frm.upper(), to.upper())
            await ctx.send(str(value)+' '+frm.upper()+' is equal to '+str(newvalue)+' '+to.upper())
        except Exception as e:
            await ctx.send("An Error occured: "+str(e))

    @commands.command(aliases=['l'])
    async def logo(self, ctx: commands.Context):
        '''Displays MarkBot's logo'''
        await ctx.send('```'+l+'\nDeveloped by Wilford Warfstache#0256, started on April 16th, 2019'+'```')
        await ctx.send(file=discord.File('logo.jpg'))

    @commands.command(aliases=['inv'])
    async def invite(self, ctx: commands.Context):
        '''Invite the bot to your server!'''
        embedVar = discord.Embed(title="Invite MarkBot to your server!",
                                 description="MarkBot is a project that is being worked on since April 19th, 2019. It was developed by [Anish R](https://github.com/z404). Feel free to fork the bot, and send pull requests if you've made any good changes. If you're interested in discussing future features to this bot, dm <@353835291053785088> to discuss it further", color=0x00ff00)
        embedVar.add_field(
            name="Invite Markbot", value='[Click here to invite MarkBot](https://discord.com/api/oauth2/authorize?client_id=781403770721402901&permissions=8&scope=bot%20applications.commands)\n', inline=False)
        embedVar.add_field(name="Invite MarkBot Beta",
                           value="[Click here to invite MarkBot Beta](https://discord.com/api/oauth2/authorize?client_id=808973332988952586&permissions=8&scope=bot%20applications.commands)\nMarkBot Beta is an unstable release, and will not be online at all times, but will have experimental features that aren't present in MarkBot", inline=False)
        embedVar.set_image(
            url='https://t4.ftcdn.net/jpg/03/75/38/73/360_F_375387396_wSJM4Zm0kIRoG7Ej8rmkXot9gN69H4u4.jpg')
        await ctx.send(embed=embedVar)

    @commands.command(name="stealemoji")
    async def _stealemoji(self, ctx: commands.Context, emoji: discord.PartialEmoji):
        """If you have nitro, you can use this command to save an emoji of another server to the current server"""
        img = await emoji.url.read()
        name = emoji.name
        emoji = await ctx.guild.create_custom_emoji(name=(name), image=img)
        await ctx.send("Added "+str(emoji))

    @_stealemoji.error
    async def _emoji_error(self, ctx: commands.Context, error):
        if "PartialEmoji" in str(error):
            await ctx.send("Yo this emoji already exists!")

    # @cog_ext.cog_slash(name="invite")
    # async def _invite_slash(self, ctx: SlashContext):
    #     '''Invite the bot to your server!'''
    #     embedVar = discord.Embed(title="Invite MarkBot to your server!",
    #                              description="MarkBot is a project that is being worked on since April 19th, 2019. It was developed by [Anish R](https://github.com/z404). Feel free to fork the bot, and send pull requests if you've made any good changes. If you're interested in discussing future features to this bot, dm <@353835291053785088> to discuss it further", color=0x00ff00)
    #     embedVar.add_field(
    #         name="Invite Markbot", value='[Click here to invite MarkBot](https://discord.com/api/oauth2/authorize?client_id=781403770721402901&permissions=8&scope=bot%20applications.commands)\n', inline=False)
    #     embedVar.add_field(name="Invite MarkBot Beta",
    #                        value="[Click here to invite MarkBot Beta](https://discord.com/api/oauth2/authorize?client_id=808973332988952586&permissions=8&scope=bot%20applications.commands)\nMarkBot Beta is an unstable release, and will not be online at all times, but will have experimental features that aren't present in MarkBot", inline=False)
    #     embedVar.set_image(
    #         url='https://t4.ftcdn.net/jpg/03/75/38/73/360_F_375387396_wSJM4Zm0kIRoG7Ej8rmkXot9gN69H4u4.jpg')
    #     await ctx.send(embed=embedVar)

    # @cog_ext.cog_slash(name="logo")
    # async def _logo_slash(self, ctx: SlashContext):
    #     '''Displays MarkBot's logo'''
    #     await ctx.send('```'+l+'\nDeveloped by Wilford Warfstache#0256, started on April 16th, 2019'+'```')
    #     await ctx.channel.send(file=discord.File('logo.jpg'))

    # @cog_ext.cog_slash(name="math")
    # async def _math_slash(self, ctx: SlashContext, math_string: str):
    #     '''Tries to solve a few basic math problems'''
    #     try:
    #         await ctx.send("Thinking..")
    #         res = self.wolframclient.query(math_string)
    #         for i in res:
    #             # if i['@title'] == 'Result':
    #             #    await ctx.send(i['subpod']['img']['@src'])
    #             embed = discord.Embed()
    #             if i['@title'] == 'Input interpretation' or i['@title'] == 'Input':
    #                 embed.title = 'Input Interpretation:'
    #                 embed.set_image(url=i['subpod']['img']['@src'])
    #                 await ctx.channel.send(embed=embed)
    #             elif i['@title'] == 'Result' or i['@title'] == 'Implicit plot' or i['@title'] == 'Plots' or i['@title'] == 'Surface plot' or i['@title'] == 'Volume of solid':
    #                 try:
    #                     embed.title = 'Result'
    #                     embed.set_image(url=i['subpod']['img']['@src'])
    #                     await ctx.channel.send(embed=embed)
    #                 except:
    #                     embed.title = 'Result'
    #                     embed.set_image(url=i['subpod'][0]['img']['@src'])
    #                     await ctx.channel.send(embed=embed)
    #     except Exception as e:
    #         await ctx.channel.send('Something went wrong. (Math is in beta) '+str(e))

    # @cog_ext.cog_slash(name="wiki")
    # async def _wiki_slash(self, ctx: SlashContext, search_message: str):
    #     '''Searches wikipedia and shows a summary of the search term'''
    #     await ctx.send("Thinking..")
    #     try:
    #         url = wikipedia.page(search_message)
    #         summary = wikipedia.summary(search_message, sentences=5)
    #         # await ctx.send(summary+'\n\nUrl = `'+str(url)+'`')
    #         embed = discord.Embed()
    #         embed.title = url.title
    #         embed.description = summary + \
    #             '\n\n[Click here to read more]('+url.url+')'
    #         if url.images != None:
    #             embed.set_image(url=url.images[0])
    #         await ctx.channel.send(embed=embed)
    #     except wikipedia.exceptions.PageError:
    #         await ctx.channel.send("Could not find a page with that search term")
    #     except wikipedia.exceptions.DisambiguationError:
    #         await ctx.channel.send("Too many results. Please be more specific")

    # @cog_ext.cog_subcommand(base="convert", name="currency")
    # async def _currency_converter_slash(self, ctx: SlashContext, value: float, frm: str, to: str):
    #     '''Converts currency from one unit to another'''
    #     c = CurrencyConverter()
    #     try:
    #         newvalue = c.convert(value, frm.upper(), to.upper())
    #         await ctx.send(str(value)+' '+frm.upper()+' is equal to '+str(newvalue)+' '+to.upper())
    #     except Exception as e:
    #         await ctx.send("An Error occured: "+str(e))

    # @cog_ext.cog_slash(name="tinify")
    # async def _tinify_slash(self, ctx: SlashContext, url: str):
    #     '''Uses tinyurl to shorten a url'''
    #     apiurl = "http://tinyurl.com/api-create.php?url="
    #     tinyurl = await self.bot.loop.run_in_executor(None, lambda: urlopen(apiurl + url).read().decode("utf-8"))
    #     await ctx.send(tinyurl)


async def setup(bot):
    await bot.add_cog(Functionality(bot))
