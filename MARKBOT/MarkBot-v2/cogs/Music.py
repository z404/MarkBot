# Importing packages required for discord bot
import discord
import asyncio
import functools
import itertools
import math
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
# Importing packages for music
import youtube_dl
# importing packages for spotify
import spotipy
import spotipy.oauth2 as oauth2


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


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        # 'audioformat': 'mp3',
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
        try:
            self.requested_string = ctx.message.content
        except:
            self.requested_string = ctx.songname

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

        partial = functools.partial(
            cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(
                'Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(
                    'Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(
            cls.ytdl.extract_info, webpage_url, download=False)
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
                    raise YTDLError(
                        'Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

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
                               description='```css\n{0.source.title}\n```'.format(
                                   self),
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

        self.db = get_db()
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
                # try:
                #    async with timeout(180):  # 3 minutes
                self.current = await self.songs.get()
                # except asyncio.TimeoutError:
                # self.bot.loop.create_task(self.stop())
                # return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            self.db = get_db()
            if (str(self.current.source.channel.guild.id) + 'announce') in self.db.keys():
                pass
            else:
                await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        # self.skip_votes.clear()

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
        self.cli_id = config["spotify_api_key"]
        self.cli_sec = config["spotify_api_secret"]

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
            raise commands.NoPrivateMessage(
                'This command can\'t be used in DM channels.')

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

    @cog_ext.cog_slash(name="join")
    async def _join_slash(self, ctx: SlashContext):
        """Joins a voice channel."""
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.send("Hello there!", hidden=True)

    @commands.command(name='summon')
    # @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError(
                'You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @cog_ext.cog_slash(name="summon")
    async def _summon_slash(self, ctx: SlashContext, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel."""
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        if not channel and not ctx.author.voice:
            raise VoiceError(
                'You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.send("Hello there!!", hidden=True)

    @commands.command(name='leave', aliases=['disconnect', 'yeet'])
    # @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        await ctx.send("I've been yeeted :(")
        del self.voice_states[ctx.guild.id]

    @cog_ext.cog_slash(name="leave")
    async def _leave_slash(self, ctx: SlashContext):
        """Clears the queue and leaves the voice channel."""
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        await ctx.send("I've been yeeted :(")
        del self.voice_states[ctx.guild.id]

    @commands.command(name='now', aliases=['current', 'playing', 'np'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @cog_ext.cog_subcommand(base="now", name="playing")
    async def _now_slash(self, ctx: SlashContext):
        """Displays the currently playing song."""

        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    # @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        # if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_playing():
        ctx.voice_state.voice.pause()
        await ctx.message.add_reaction('⏯')

    @cog_ext.cog_slash(name="pause")
    async def _pause_slash(self, ctx: SlashContext):
        """Pauses the currently playing song."""
        # if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_playing():
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)
        ctx.voice_state.voice.pause()
        await ctx.send("Paused song. Use /resume to resume")

    @commands.command(name='resume')
    # @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        # if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_paused():
        ctx.voice_state.voice.resume()
        await ctx.message.add_reaction('⏯')

    @cog_ext.cog_slash(name="resume")
    async def _resume_slash(self, ctx: SlashContext):
        """Resumes a currently paused song."""
        # if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_playing():
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)
        ctx.voice_state.voice.resume()
        await ctx.send("Resumed song!")

    @commands.command(name='stop')
    # @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        # if not ctx.voice_state.is_playing:
        ctx.voice_state.voice.stop()
        await ctx.message.add_reaction('⏹')

    @cog_ext.cog_slash(name="stop")
    async def _stop_slash(self, ctx: SlashContext):
        """Stops playing song and clears the queue."""
        # if not ctx.voice_state.is_playing and #ctx.voice_state.voice.is_playing():
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)
        ctx.voice_state.songs.clear()
        ctx.voice_state.voice.stop()
        await ctx.send("Song stopped and queue cleared!")

    @commands.command(name='skip', aliases=['n', 'next'])
    async def _skip(self, ctx: commands.Context):
        """Skips a song in queue"""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        #voter = ctx.message.author
        # if voter == ctx.voice_state.current.requester:
        await ctx.message.add_reaction('⏭')
        ctx.voice_state.skip()

        # elif voter.id not in ctx.voice_state.skip_votes:
        #    ctx.voice_state.skip_votes.add(voter.id)
        #    total_votes = len(ctx.voice_state.skip_votes)

        #    if total_votes >= 3:
        #        await ctx.message.add_reaction('⏭')
        #        ctx.voice_state.skip()
        #    else:
        #        await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        # else:
        #   await ctx.send('You have already voted to skip this song.')

    @cog_ext.cog_slash(name="skip")
    async def _skip_slash(self, ctx: SlashContext):
        """Skips a song in queue"""
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)
        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')
        ctx.voice_state.skip()
        await ctx.send("Skipped song!")

    @commands.command(name='queue', aliases=['q'])
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
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(
                i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="queue")
    async def _queue_slash(self, ctx: SlashContext, page: int = None):
        """Shows the player's queue.
        """
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        if page == None:
            page = 1

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(
                i + 1, song)

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

    @cog_ext.cog_slash(name="shuffle")
    async def _shuffle_slash(self, ctx: SlashContext):
        """Shuffles the queue."""
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()

        await ctx.send("Shuffled queue!")

    @cog_ext.cog_slash(name="remove")
    async def _remove_slash(self, ctx: SlashContext, index: int):
        """Shuffles the queue."""
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.send("Song removed at "+str(index))

    @commands.command(name='remove', aliases=['r'])
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @cog_ext.cog_slash(name="toggleannounce")
    async def toggleannounce(self, ctx: commands.Context):
        '''Toggles the announcement of a new song in a server'''
        self.db = get_db()
        if (str(ctx.guild.id)+'announce') not in self.db.keys():
            await ctx.send('Announcement of new songs is toggled off')
            self.db[str(ctx.guild.id) + 'announce'] = True
            write_db(self.db)
        else:
            await ctx.send('Announcement of new songs is toggled on')
            del self.db[str(ctx.guild.id) + 'announce']
            write_db(self.db)

    @commands.command()
    async def toggleannounce(self, ctx: commands.Context):
        '''Toggles the announcement of a new song in a server'''
        self.db = get_db()
        if (str(ctx.guild.id)+'announce') not in self.db.keys():
            await ctx.send('Announcement of new songs is toggled off')
            self.db[str(ctx.guild.id) + 'announce'] = True
            write_db(self.db)
        else:
            await ctx.send('Announcement of new songs is toggled on')
            del self.db[str(ctx.guild.id) + 'announce']
            write_db(self.db)

    @cog_ext.cog_slash(name="play")
    async def _play_slash(self, ctx: SlashContext, search: str):
        try:
            ctx.voice_state
        except:
            ctx.voice_state = self.get_voice_state(ctx)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')
        if not ctx.voice_state.voice:
            destination = ctx.author.voice.channel
            if ctx.voice_state.voice:
                await ctx.voice_state.voice.move_to(destination)
                return

            ctx.voice_state.voice = await destination.connect()
        ctx.songname = search
        await ctx.send("Searching for song..")
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
                    search_new = features['name'] + \
                        ' '+features['artists'][0]['name']
                    source = await YTDLSource.create_source(ctx, search_new, loop=self.bot.loop)
                    song = Song(source)

                    await ctx.voice_state.songs.put(song)
                    await ctx.send('Enqueued {}'.format(str(source)))
                else:
                    response = spotify.playlist_items(search)
                    await ctx.send("Enqueueing "+str(len(response['items']))+" songs. This may take a while..")
                    for i in response['items']:
                        try:
                            search_new = i['track']['name'] + \
                                ' '+i['track']['artists'][0]['name']
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
                    # 'audioformat': 'mp3',
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
                partial = functools.partial(
                    ytdl.extract_info, search, download=False, process=False)
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, partial)
                if 'entries' in list(data.keys()):
                    video = data['entries']
                    count = 0
                    urllst = []
                    for i in video:
                        count += 1
                        urllst.append(i['title'])
                    await ctx.send('Enqueued '+str(count)+' songs')
                    for i in urllst:
                        try:
                            source = await YTDLSource.create_source(ctx, i, loop=self.bot.loop)
                            song = Song(source)
                            await ctx.voice_state.songs.put(song)
                        except:
                            pass
                        # break
                else:
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
                    song = Song(source)

                    await ctx.voice_state.songs.put(song)
                    await ctx.send('Enqueued {}'.format(str(source)))
        except YTDLError as e:
            await ctx.send('An error occurred while processing this request: {}'.format(str(e)))

    @commands.command(name='play', aliases=['p'])
    async def _play(self, ctx: commands.Context, *, search: str, flag=None):
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
                        search_new = features['name'] + \
                            ' '+features['artists'][0]['name']
                        source = await YTDLSource.create_source(ctx, search_new, loop=self.bot.loop)
                        song = Song(source)

                        await ctx.voice_state.songs.put(song)
                        if flag == None:
                            await ctx.send('Enqueued {}'.format(str(source)))
                    else:
                        response = spotify.playlist_items(search)
                        await ctx.send("Enqueueing "+str(len(response['items']))+" songs. This may take a while..")
                        for i in response['items']:
                            try:
                                search_new = i['track']['name'] + \
                                    ' '+i['track']['artists'][0]['name']
                                source = await YTDLSource.create_source(ctx, search_new, loop=self.bot.loop)
                                song = Song(source)
                                await ctx.voice_state.songs.put(song)
                            except:
                                continue
                        if flag == None:
                            await ctx.send("Playlist has been enqueued")

                else:
                    YTDL_OPTIONS = {
                        'format': 'bestaudio/best',
                        'extractaudio': True,
                        # 'audioformat': 'mp3',
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
                    partial = functools.partial(
                        ytdl.extract_info, search,            download=False, process=False)
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, partial)
                    if 'entries' in list(data.keys()):
                        video = data['entries']
                        count = 0
                        urllst = []
                        for i in video:
                            count += 1
                            urllst.append(i['title'])
                        if flag == None:
                            await ctx.send('Enqueued '+str(count)+' songs')
                        for i in urllst:
                            try:
                                source = await YTDLSource.create_source(ctx, i, loop=self.bot.loop)
                                song = Song(source)
                                await ctx.voice_state.songs.put(song)
                            except:
                                pass
                            # break
                    else:
                        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
                        song = Song(source)

                        await ctx.voice_state.songs.put(song)
                        if flag == None:
                            await ctx.send('Enqueued {}'.format(str(source)))
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')

    @commands.group(name="playlist", pass_context=True)
    async def _playlist(self, ctx: commands.Context):
        self.db = get_db()
        if not ctx.invoked_subcommand:
            # Display saved playlists
            try:
                # Make a better display of playlists
                for i in self.db[str(ctx.author.id) + "_saved_playlists"]:
                    await ctx.send(i)
            except KeyError:
                await ctx.send("You don't have any saved playlists!")
        # await self._play(ctx=ctx, search="level of concern", flag=True)

    @_playlist.command(pass_context=True, name="create")
    async def _playlist_create(self, ctx: commands.Context, *, name_of_playlist: str):
        self.db = get_db()
        if " " in name_of_playlist:
            await ctx.send("Playlist names cannot have spaces!")
        else:
            try:
                self.db[str(ctx.author.id) +
                        "_saved_playlists"].update({name_of_playlist: None})
            except:
                self.db[str(ctx.author.id) +
                        "_saved_playlists"] = {name_of_playlist: None}
            await ctx.send("Playlist added!")
            write_db(self.db)
            self.db = get_db()


def setup(bot):
    bot.add_cog(Music(bot))
