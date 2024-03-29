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

## DISCORD BOT VERSION OF PROJECT MARk

#Importing nessesary packages
import json
import os
import warnings
from random import randint, choice
from discord import channel
#Importing replit database
try:
    from replit import db
except:
    db={}
#Importing packages required for discord bot
import discord
import asyncio
import functools
import itertools
import math
import random
from async_timeout import timeout
from discord.ext import commands
#Importing packages for music
import youtube_dl
#importing package for searching
import wikipedia
#importing package for math
import wolframalpha
#importing packages for google
try:
    from search_engine_parser import GoogleSearch
except:
    pass
#importing packages for spotify
import spotipy
import spotipy.oauth2 as oauth2
#importing packages for giphy
import giphy_client as gc
from giphy_client.rest import ApiException
#import packages for currency conversion
from currency_converter import CurrencyConverter
#importing pretty tables
from tabulate import tabulate
#importing azapi for lyrics
import azapi

print(l)
youtube_dl.utils.bug_reports_message = lambda: ''
warnings.catch_warnings()
warnings.simplefilter("ignore")

class AdminControls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context = True)
    # @commands.has_permissions(administrator=True)
    async def changenick(self, ctx: commands.Context, member, *newnick):
        '''Changes nickname of any user, if the user is below the bot and if sender has admin perms'''
        newnick = " ".join(list(newnick))
        await ctx.message.delete()
        if '<' in member:
            member = ctx.message.guild.get_member(int(member.strip('<@!>')))
        else: member = ctx.message.guild.get_member(int(member))
        await member.edit(nick=newnick)

    @changenick.error
    async def changenick_error(self, ctx, error):
        if "permission" in str(error):
            await ctx.send("You don't have permission to do that mate")

    @commands.command()
    @commands.is_owner()
    async def terminate(self, ctx: commands.Context):
        if ctx.message.author.id == 353835291053785088:
            await ctx.send("It's getting dark.. Maybe I'll take a little nap..")
            await bot.close()

class Functionality(commands.Cog):

    @commands.Cog.listener()
    async def on_command(self, ctx):
        logchannel = bot.get_channel(844599292442181653)
        try:
            await logchannel.send(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            await logchannel.send(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open('creds.txt') as file:
            app_id = file.readlines()[4].strip().rstrip('\n ')
        client = wolframalpha.Client(app_id)
        self.wolframclient = client

    @commands.command(name="resetshrugchannel")
    async def _resetshrugchannel(self, ctx: commands.Context):
        '''Resets Shrug channel in a server'''
        def check_if_server_has_shrug(server_id):
            for i in db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True, i
            return False, None
        ret = check_if_server_has_shrug(ctx.guild.id)
        if ret[0]:
            del(db[ret[1]])
            await ctx.send("Successfully reset shrug channel!")
        else:
            await ctx.send("What's a shrug channel? I can't reset what I don't know. I'm not a supercomputer y'know")

    @commands.command(name="setshrugchannel")
    async def _setshrugchannel(self, ctx: commands.Context, channel: discord.TextChannel):
        '''Set Shrug channel in a server'''
        def check_if_server_has_shrug(server_id):
            for i in db.keys():
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
            db[str(ctx.guild.id)+str(channel.id)+'shrugchan'] = message_count
            await ctx.send("Shrug channel is now configured!")

    @commands.command(name="shrugleaderboard")
    async def _shrugleaderboard(self, ctx: commands.Context):
        '''Displays a shrug leaderboard for the server'''
        def check_if_server_has_shrug(server_id):
            for i in db.keys():
                if str(server_id) == i[:len(str(server_id))] and "shrugchan" in i:
                    return True, i
            return False, None
        ret = check_if_server_has_shrug(ctx.guild.id)
        if ret[0]:
            leaderdata = db[ret[1]]
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
            headers =  ["User", "Shrugs"]
            table = tabulate(finaldict, headers, tablefmt="fancy_grid")
            # await ctx.send("Leaderboard:\n```"+table+"```")
            desc = "```yaml\n"+table+"```\n Total shrugs: "+str(sum(Y))
            embed=discord.Embed(title="Leaderboard", description=desc, color=0x00ff00)
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
                summary = wikipedia.summary(searchmsg,sentences=5)
                #await ctx.send(summary+'\n\nUrl = `'+str(url)+'`')
                embed = discord.Embed()
                embed.title = url.title
                embed.description = summary+'\n\n[Click here to read more]('+url.url+')'
                if url.images != None:
                    embed.set_image(url = url.images[0])
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
                #if i['@title'] == 'Result':
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
    
    @commands.command()
    async def google(self, ctx: commands.Context, *, searchquery):
        '''Gives the first 5 results of a google search of the query'''
        try:
            gsearch = GoogleSearch()
            async with ctx.typing():
                gresults = await gsearch.async_search(searchquery,1)
            embed = discord.Embed()
            embed.title = "Search Results for \""+searchquery+"\""
            descstring = ''
            count = 0
            for i in gresults:
                count+=1
                if count>5:
                    break
                descstring+='\n\n'+str(count)+') ['+i['descriptions']+']('+i['links']+')'
            embed.description = descstring
            await ctx.send(embed=embed)
        except:
            await ctx.send("Google wasn't able to find appropriate results for this query")

    @commands.command(name='currency_converter',aliases=['currconv'])
    async def _currency_converter(self, ctx: commands.Context, value: int, frm: str, to: str):
        '''Converts currency from one unit to another'''
        c = CurrencyConverter()
        try:
            newvalue = c.convert(value, frm.upper(), to.upper())
            await ctx.send(str(value)+' '+frm.upper()+' is equal to '+str(newvalue)+' '+to.upper())
        except Exception as e:
            await ctx.send("An Error occured: "+str(e))

class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        #'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data
        self.requested_string = ctx.message.content

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)

class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed

    def return_request_string(self):
        return self.source.requested_string

class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                #try:
                #    async with timeout(180):  # 3 minutes
                self.current = await self.songs.get()
                #except asyncio.TimeoutError:
                #self.bot.loop.create_task(self.stop())
                #return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            if (str(self.current.source.channel.guild.id) + 'announce') in db.keys():
                pass
            else:
                await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}
        with open('creds.txt') as file:
            creds = file.readlines()
            cli_id = creds[1].strip().rstrip('\n ')
            cli_sec = creds[2].rstrip().rstrip('\n ')
        self.cli_id = cli_id
        self.cli_sec = cli_sec

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    #@commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect','yeet'])
    #@commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        await ctx.send("I've been yeeted :(")
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume', aliases=['vol'])
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing','np'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    #@commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        #if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_playing():
        ctx.voice_state.voice.pause()
        await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    #@commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        #if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_paused():
        ctx.voice_state.voice.resume()
        await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    #@commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        #if not ctx.voice_state.is_playing:
        ctx.voice_state.voice.stop()
        await ctx.message.add_reaction('⏹')

    @commands.command(name='skip',aliases=['n', 'next'])
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        #voter = ctx.message.author
        #if voter == ctx.voice_state.current.requester:
        await ctx.message.add_reaction('⏭')
        ctx.voice_state.skip()

        #elif voter.id not in ctx.voice_state.skip_votes:
        #    ctx.voice_state.skip_votes.add(voter.id)
        #    total_votes = len(ctx.voice_state.skip_votes)

        #    if total_votes >= 3:
        #        await ctx.message.add_reaction('⏭')
        #        ctx.voice_state.skip()
        #    else:
        #        await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        #else:
        #   await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue',aliases=['q'])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove',aliases=['r'])
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def toggleannounce(self, ctx: commands.Context):
        '''Toggles the announcement of a new song in a server'''
        if (str(ctx.guild.id)+'announce') not in db.keys():
            await ctx.send('Announcement of new songs is toggled off')
            db[str(ctx.guild.id) + 'announce'] = True
        else:
            await ctx.send('Announcement of new songs is toggled on')
            del db[str(ctx.guild.id) + 'announce']
        
    @commands.command(name='play',aliases=['p'])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                if 'open.spotify' in search:
                    auth = oauth2.SpotifyClientCredentials(
                        client_id=self.cli_id,
                        client_secret=self.cli_sec
                    )
                    token = auth.get_access_token(as_dict=False)
                    spotify = spotipy.Spotify(auth=token)
                    if 'track' in search:
                        features = spotify.track(search)
                        search_new = features['name']+' '+features['artists'][0]['name']
                        source = await YTDLSource.create_source(ctx, search_new, loop=self.bot.loop)
                        song = Song(source)

                        await ctx.voice_state.songs.put(song)
                        await ctx.send('Enqueued {}'.format(str(source)))
                    else:
                        response = spotify.playlist_items(search)
                        await ctx.send("Enqueueing "+str(len(response['items']))+" songs. This may take a while..")
                        for i in response['items']:
                            try:
                                search_new = i['track']['name']+' '+i['track']['artists'][0]['name']
                                source = await YTDLSource.create_source(ctx, search_new, loop=self.bot.loop)
                                song = Song(source)
                                await ctx.voice_state.songs.put(song)
                            except:
                                continue
                        await ctx.send("Playlist has been enqueued")

                else:
                    YTDL_OPTIONS = {
                        'format': 'bestaudio/best',
                        'extractaudio': True,
                        #'audioformat': 'mp3',
                        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                        'restrictfilenames': True,
                        'noplaylist': True,
                        'nocheckcertificate': True,
                        'ignoreerrors': False,
                        'logtostderr': False,
                        'quiet': True,
                        'no_warnings': True,
                        'default_search': 'auto',
                        'source_address': '0.0.0.0',
                        'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                    }

                    FFMPEG_OPTIONS = {
                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': '-vn',
                    }

                    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS) 
                    partial = functools.partial(ytdl.extract_info, search,            download=False, process=False)
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, partial)
                    if 'entries' in list(data.keys()):
                        video = data['entries']
                        count = 0
                        urllst = []
                        for i in video:
                            count+=1
                            urllst.append(i['title'])
                        await ctx.send('Enqueued '+str(count)+' songs')
                        for i in urllst:
                            try:
                                source = await YTDLSource.create_source(ctx, i, loop=self.bot.loop)
                                song = Song(source)
                                await ctx.voice_state.songs.put(song)
                            except:
                                pass
                            #break
                    else:
                        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
                        song = Song(source)

                        await ctx.voice_state.songs.put(song)
                        await ctx.send('Enqueued {}'.format(str(source)))
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))


    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.deletedict = {}
        with open('creds.txt') as file:
            apikey = file.readlines()[3].strip().rstrip('\n ')
        self.giphy = gc.DefaultApi()
        self.giphykey = apikey

    @commands.command(name='changestatus',aliases=['chst'])
    async def _changestatus(self, ctx: commands.Context, typeofstatus, *message):
        '''Changes the bot\'s status to the given parameters'''
        message = ' '.join(message)
        if typeofstatus.lower() == 'playing':
            await bot.change_presence(activity=discord.Game(message))
        elif typeofstatus.lower() == 'watching':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))
        elif typeofstatus.lower() == 'listeningto':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        elif typeofstatus.lower() == 'streaming':
            if 'twitch' not in message.split()[-1]:
                await ctx.send('Please provide a twitch url')
            else:
                await bot.change_presence(activity=discord.Streaming(name=' '.join(message.split()[:-1]), url=message.split()[-1]))
        elif typeofstatus.lower() == 'online':
            await bot.change_presence(status = discord.Status.online)
        elif typeofstatus.lower() == 'idle':
            await bot.change_presence(status = discord.Status.idle)
        elif typeofstatus.lower() == 'dnd':
            await bot.change_presence(status = discord.Status.dnd)
        else:
            await ctx.send('Wrong format! format = <type> <message> <url (for stream)> Choose type from ["playing","watching","listeningto","streaming"]. You can also set status as ["online","idle","dnd"]')

    @commands.command()
    async def toggleyenglis(self, ctx: commands.Context):
        '''Toggles English to Yenglis translator (credits esteban)'''
        if (str(ctx.channel.id)+str(ctx.guild.id) + 'yenglis') not in db.keys():
            await ctx.send('Translation is toggled on')
            db[str(ctx.channel.id)+str(ctx.guild.id) + 'yenglis'] = True
        else:
            await ctx.send('Translation is toggled off')
            del db[str(ctx.channel.id)+str(ctx.guild.id) + 'yenglis']

    @commands.command()
    async def yenglis(self, ctx: commands.Context, *message):
        '''Translates a single English line to Yenglis (credits esteban)'''
        msg = " ".join(message)
        await ctx.message.channel.send(basicshout(use_rules(replace_words(msg))))

    @commands.command(aliases=['l'])
    async def logo(self, ctx: commands.Context):
        '''Displays Project Mark's logo'''
        await ctx.send('```'+l+'\nDeveloped by Wilford Warfstache#0256, started on April 16th, 2019'+'```')
        await ctx.send(file=discord.File('logo.jpg'))
    
    @commands.command(aliases=['gif','tenor'])
    async def giphy(self, ctx: commands.Context, *, searchquery):
        '''Displays a random gif from giphy based on the search query'''
        try:
            response = self.giphy.gifs_search_get(self.giphykey,searchquery,limit=1,offset=randint(1,10),fmt='gif')
            gif_id = response.data[0]
            await ctx.send(gif_id.images.downsized.url)
        except ApiException:
            await ctx.send("Whoops, an error occured!")
    
    @commands.command(aliases=['inv'])
    async def invite(self, ctx: commands.Context):
        '''Invite the bot to your server!'''
        embedVar = discord.Embed(title="Invite MarkBot to your server!", description="MarkBot is a project that is being worked on since April 19th, 2019. It was developed by [Anish R](https://github.com/z404). Feel free to fork the bot, and send pull requests if you've made any good changes. If you're interested in discussing future features to this bot, dm <@353835291053785088> to discuss it further", color=0x00ff00)
        embedVar.add_field(name="Invite Markbot", value = '[Click here to invite MarkBot](https://discord.com/api/oauth2/authorize?client_id=781403770721402901&permissions=8&scope=bot)\n',inline=False)
        embedVar.add_field(name="Invite MarkBot Beta", value="[Click here to invite MarkBot Beta](https://discord.com/api/oauth2/authorize?client_id=808973332988952586&permissions=8&scope=bot)\nMarkBot Beta is an unstable release, and will not be online at all times, but will have experimental features that aren't present in MarkBot", inline=False)
        embedVar.set_image(url='https://t4.ftcdn.net/jpg/03/75/38/73/360_F_375387396_wSJM4Zm0kIRoG7Ej8rmkXot9gN69H4u4.jpg')
        await ctx.send(embed=embedVar)

class Encoder(commands.Cog):
            
    def __init__(self, bot):
        self.bot = bot

    # from text to something coded
    @commands.group(name="to", pass_context=True)
    async def _to(self, ctx):
        """Convert text to a coded something."""
        if not ctx.invoked_subcommand:
            await ctx.send('```-to \n\nConvert text to a coded something.\n\nCommands:\n\tbinary   Convert text to binary.\n\tmorse    Convert text to morse.\n\treversed Reverses your text\n\nType -help command for more info on a command.\nYou can also type -help category for more info on a category.```')

    @_to.command(pass_context=True, name="binary")
    async def _binary(self, ctx, *, text):
        """Convert text to binary."""
        try:
            await ctx.message.delete()
        except:
            pass
        alpha_to_binary = {
        " ": "00100000", "!": "00100001", "?": "00111111", ":": "00111010", ";": "00111011", "\"": "00100010", "'": "00100111", "/": "00101111", "\\": "01011100", "{": "01111011", "}": "01111101", "(": "00101000", ")": "00101001", ".": "00101110",
        "A": "01000001", "B": "01000010", "C": "01000011", "D": "01000100", "E": "01000101", "F": "01000110", "G": "01000111", "H": "01001000", "I": "01001001", "J": "01001010", "K": "01001011", "L": "01001100", "M": "01001101", "N": "01001110", "O": "01001111", "P": "01010000", "Q": "01010001", "R": "01010010", "S": "01010011", "T": "01010100", "U": "01010101", "V": "01010110", "W": "01010111", "X": "01011000", "Y": "01011001", "Z": "01011010",
        "a": "01100001", "b": "01100010", "c": "01100011", "d": "01100100", "e": "01100101", "f": "01100110", "g": "01100111", "h": "01101000", "i": "01101001", "j": "01101010", "k": "01101011", "l": "01101100", "m": "01101101", "n": "01101110", "o": "01101111", "p": "01110000", "q": "01110001", "r": "01110010", "s": "01110011", "t": "01110100", "u": "01110101", "v": "01110110", "w": "01110111", "x": "01111000", "y": "01111001", "z": "01111010",
        "0": "00110000", "1": "00110001", "2": "00110010", "3": "00110011", "4": "00110100", "5": "00110101", "6": "00110110", "7": "00110111", "8": "00111000", "9": "00111001"}
        try:
            binary = [alpha_to_binary[char] for char in text]
        except KeyError:
            await ctx.send("One of the characters you filled in is not in the list.")
            return
        except:
            await ctx.send("An unknown error occured while translating your text.")
            return
        await ctx.send("<@"+str(ctx.author.id)+"> Said:\n```fix\n"+" ".join(binary)+"```")

    @_to.command(pass_context=True, name="morse")
    async def _morse(self, ctx, *, text):
        """Convert text to morse."""
        try:
            await ctx.message.delete()
        except:
            pass
        alpha_to_morse = {
        " ": " ", ".": ".-.-.-", "!": "-.-.--", "?": "..--..", ":": "---...", ";": "-.-.-.", "\"": ".-..-.", "'": ".----.", "/": "-..-.", "(": "-.--.", ")": "-.--.-",
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
        "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..",
        "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----."}
        try:
            morse = [alpha_to_morse[char] for char in text]
        except KeyError:
            await ctx.send("One of the characters you filled in is not in the list.")
            return
        except:
            await ctx.send("An unknown error occured while translating your text.")
            return
        await ctx.send("<@"+str(ctx.author.id)+"> Said:\n```fix\n"+" ".join(morse)+'```')
        
    @_to.command(pass_context=True, name="reversed")
    async def _reversed(self, ctx, *, msg):
        """Reverses your text"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send("<@"+str(ctx.author.id)+"> Said:\n```fix\n"+msg[::-1]+'```')
        
    # from something coded to text
    @commands.group(name="from", pass_context=True)
    async def _from(self, ctx):
        """Convert a coded something to text."""
        if not ctx.invoked_subcommand:
            await ctx.send('```-from \n\nConvert a coded something to text.\n\nCommands:\n\tbinary   Convert binary to text.\n\tmorse    Convert morse to text.\n\treversed Unreverses your text\n\nType -help command for more info on a command.\nYou can also type -help category for more info on a category.```')

    @_from.command(pass_context=True)
    async def binary(self, ctx, *, binary):
        """Convert binary to text."""
        try:
            await ctx.message.delete()
        except:
            pass
        binary = binary.split()
        binary_to_alpha = {
        "00100000": " ", "00100001": "!", "00111111": "?", "00111010": ":", "00111011": ";", "00100010": "\"", "00100111": "'", "00101111": "/", "01011100": "\\", "01111011": "{", "01111101": "}", "00101000": "(", "00101001": ")", "00101110": ".",
        "01000001": "A", "01000010": "B", "01000011": "C", "01000100": "D", "01000101": "E", "01000110": "F", "01000111": "G", "01001000": "H", "01001001": "I", "01001010": "J", "01001011": "K", "01001100": "L", "01001101": "M", "01001110": "N", "01001111": "O", "01010000": "P", "01010001": "Q", "01010010": "R", "01010011": "S", "01010100": "T", "01010101": "U", "01010110": "V", "01010111": "W", "01011000": "X", "01011001": "Y", "01011010": "Z",
        "01100001": "a", "01100010": "b", "01100011": "c", "01100100": "d", "01100101": "e", "01100110": "f", "01100111": "g", "01101000": "h", "01101001": "i", "01101010": "j", "01101011": "k", "01101100": "l", "01101101": "m", "01101110": "n", "01101111": "o", "01110000": "p", "01110001": "q", "01110010": "r", "01110011": "s", "01110100": "t", "01110101": "u", "01110110": "v", "01110111": "w", "01111000": "x", "01111001": "y", "01111010": "z",
        "00110000": "0", "00110001": "1", "00110010": "2", "00110011": "3", "00110100": "4", "00110101": "5", "00110110": "6", "00110111": "7", "00111000": "8", "00111001": "9"}
        try:
            alpha = [binary_to_alpha[char] for char in binary]
        except KeyError:
            await ctx.send("One of the characters you filled in is not in the list.")
            return
        except:
            await ctx.send("An unknown error occured while translating your text.")
            return
        await ctx.send("<@"+str(ctx.author.id)+"> Converted binary to text:\n```fix\n"+" ".join(alpha)+'```')
        
    @_from.command(pass_context=True)
    async def morse(self, ctx, *, morse):
        """Convert morse to text."""
        try:
            await ctx.message.delete()
        except:
            pass
        morse = morse.split()
        morse_to_alpha = {
        " ": " ", ".-.-.-": ".", "-.-.--": "!", "..--..": "?", "---...": ":", "-.-.-.": ";", ".-..-.": "\"", ".----.": "'", "-..-.": "/", "-.--.": "(", "-.--.-": ")",
        ".-": "a", "-...": "b", "-.-.": "c", "-..": "d", ".": "e", "..-.": "f", "--.": "g", "....": "h", "..": "i", ".---": "j", "-.-": "k", ".-..": "l", "--": "m", "-.": "n", "---": "o", ".--.": "p", "--.-": "q", ".-.": "r", "...": "s", "-": "t", "..-": "u", "...-": "v", ".--": "w", "-..-": "x", "-.--": "y", "--..": "z",
        "-----": "0", ".----": "1", "..---": "2", "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9"}
        try:
            alpha = [morse_to_alpha[char] for char in morse]
        except KeyError:
            await ctx.send("One of the characters you filled in is not in the list.")
            return
        except:
            await ctx.send("An unknown error occured while translating your text.")
            return
        await ctx.send("<@"+str(ctx.author.id)+"> Converted Morse to text:\n```fix\n"+"".join(alpha)+'```')
        
    @_from.command(pass_context=True)
    async def reversed(self, ctx, *, msg):
        """Unreverses your text"""
        try:
            ctx.message.delete()
        except:
            pass
        await ctx.send("<@"+str(ctx.author.id)+"> Unreversed the message to:\n```fix\n"+msg[::-1]+'```')

with open('.prefix') as file:
    prefix = file.read().rstrip('\n ')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),description='Developed by Wilford Warfstache#0256, started on April 16th, 2019', intents=intents)

bot.add_cog(Music(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Functionality(bot))
bot.add_cog(Encoder(bot))
bot.add_cog(AdminControls(bot))

def basicshout(input):
    return input[0].lower()+input[1:].upper()

def replace_words(inp):
    if inp[:4].lower() == 'what': inp+= ' ma'
    inp = ' ' + inp.lower() + ' '
    word_dict = {
        # ' fuck': [' fugg'],
        ' goodnight ': [' goodnite ', ' nitenite '],
        ' i dont ': [' ion '],
        ' want to ': [' wanna '],
        ' ion wanna ': [' ionwanna '],
        ' gonna ': [' gon '],
        ' discrete ': [' discreet '],
        ' english ': [' yenglis '],
        ' yes ': [' yee ', ' ye '],
        ' oh no ':[' wohno ', ' wono '],
        ' peace ': [' pspice '],
        ' lol ': [' lel ', ' xDD ', ' lmaoo ',' xDDD '], #can add more later
        ' if ': [' yif '],
        ' study ': [' stedy '],
        ' i am ': [' i iz '],
        ' im ': [' i iz '],
        ' is ': [' iz ']
    }
    for x, y in word_dict.items():
        inp = inp.replace(x,choice(y))
    return inp.strip()

def use_rules(inp):
    inp = ' ' + inp.lower() + ' '
    rules = {
        'ing ': ['in '],
        'ck': ['cc' , 'gg'],
        'sh ': ['s '],
        ' s': [' sh'],
        ' shh': [' sh'],
        ' e': [' ye'],
        'k': ['g'],
        'me ': ['m '],
        ' m ': [' me '],
        ' aw': [' wo'],
        # ' a': [' ye'],
        ' yere ': [' are '],
        'y ': ['i '],
        ' qu': [' qw'],
    }
    for x, y in rules.items():
        
        inp = inp.replace(x,choice(y))
    return inp.strip()

async def shrugupdate(message, key):
    db[key][message.author] += 1

@bot.event
async def on_message(message):
    msg = str(message.content)
    if (str(message.channel.id)+str(message.guild.id) + "yenglis") in db.keys() and not message.author.bot and message.content[0] != prefix:
        await message.channel.send(basicshout(use_rules(replace_words(msg))))
    if (str(message.guild.id)+str(message.channel.id)+'shrugchan') in db.keys() and(message.content == "¯\\_(ツ)_/¯" or repr(message.content) == r"'¯\\\\_(ツ)\\_/¯'"):
        await shrugupdate(message, str(message.guild.id)+str(message.channel.id)+'shrugchan')
    else: await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Bot is online')
    await bot.change_presence(activity=discord.Game('with Life\'s decisions'))

with open('creds.txt') as file:
    TOKEN = file.readlines()[0].strip().rstrip('\n ')

bot.run(TOKEN)
