# Copy paste this for other cogs

import discord
from discord.ext import commands
import wikipedia
import wolframalpha
from currency_converter import CurrencyConverter
from tabulate import tabulate


def write_db(db: str) -> None:
    with open("database", 'w+') as file:
        file.write(db)


def get_db() -> dict:
    with open('database') as file:
        return eval(file.read())


class Functionality(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open('creds.txt') as file:
            app_id = file.readlines()[4].strip().rstrip('\n ')
        client = wolframalpha.Client(app_id)
        self.wolframclient = client
        self.db = get_db()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        logchannel = self.bot.get_channel(844599292442181653)
        try:
            await logchannel.send(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            await logchannel.send(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    @commands.command(name="resetshrugchannel")
    async def _resetshrugchannel(self, ctx: commands.Context):
        '''Resets Shrug channel in a server'''
        def check_if_server_has_shrug(server_id):
            for i in self.db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True, i
            return False, None
        ret = check_if_server_has_shrug(ctx.guild.id)
        if ret[0]:
            del(self.db[ret[1]])
            write_db(self.db)
            await ctx.send("Successfully reset shrug channel!")
        else:
            await ctx.send("What's a shrug channel? I can't reset what I don't know. I'm not a supercomputer y'know")

    @commands.command(name="setshrugchannel")
    async def _setshrugchannel(self, ctx: commands.Context, channel: discord.TextChannel):
        '''Set Shrug channel in a server'''
        def check_if_server_has_shrug(server_id):
            for i in self.db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True
            return False
        if check_if_server_has_shrug(ctx.guild.id):
            await ctx.send("This server already has a shrug channel! Type `!resetshrugchannel` to reset shrug channel settings for this server!")
        else:
            await ctx.send("Please wait while I figure out what a shrug means to humans")
            counter = 0
            message_count = {}
            async for message in channel.history(oldest_first=True, limit=None):
                if message.content == "¯\\_(ツ)_/¯" or repr(message.content) == r"'¯\\\\_(ツ)\\_/¯'":
                    try:
                        message_count[message.author] += 1
                    except:
                        message_count[message.author] = 1
            self.db[str(ctx.guild.id)+str(channel.id) +
                    'shrugchan'] = message_count
            write_db(self.db)
            await ctx.send("Shrug channel is now configured!")

    @commands.command(name="shrugleaderboard")
    async def _shrugleaderboard(self, ctx: commands.Context):
        '''Displays a shrug leaderboard for the server'''
        def check_if_server_has_shrug(server_id):
            for i in self.db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True, i
            return False, None
        ret = check_if_server_has_shrug(ctx.guild.id)
        if ret[0]:
            leaderdata = self.db[ret[1]]
            X = list(leaderdata.keys())
            Y = list(leaderdata.values())
            userlst = [x for _, x in sorted(zip(Y, X))]
            userlst.reverse()
            finaldict = []
            for i in userlst:
                try:
                    finaldict.append([str(i.nick), str(leaderdata[i])])
                except:
                    finaldict.append([str(i), str(leaderdata[i])])
            headers = ["User", "Shrugs"]
            table = tabulate(finaldict, headers, tablefmt="fancy_grid")
            # await ctx.send("Leaderboard:\n```"+table+"```")
            desc = "```yaml\n"+table+"```\n Total shrugs: "+str(sum(Y))
            embed = discord.Embed(title="Leaderboard",
                                  description=desc, color=0x00ff00)
            await ctx.send(embed=embed)
            # await ctx.send(str(leaderdata))
        else:
            await ctx.send("No shrug channel has been set! Set a shrug channel by typing `!setshrugchannel`")

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


def setup(bot):
    bot.add_cog(Functionality(bot))
