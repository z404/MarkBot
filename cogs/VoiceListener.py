# For Discord
import discord
from discord.ext import commands
# from discord_slash import cog_ext, SlashContext
from tabulate import tabulate
import os
import speech_recognition as sr
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


class VoiceListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = get_db()
        self.connections = {
            voice.guild.id: voice for voice in self.bot.voice_clients}
        self.playlists = {}
        self.recognizer = []

    # def vc_required(func):
    #     async def get_vc(self, msg):
    #         vc = await self.get_vc(msg)
    #         if not vc:
    #             return
    #         await func(self, msg, vc)
    #     return get_vc

    async def get_vc(self, message):
        vc = message.author.voice
        if not vc:
            await message.channel.send("You're not in a vc right now")
            return
        connection = self.connections.get(message.guild.id)
        if connection:
            if connection.channel.id == message.author.voice.channel.id:
                return connection

            await connection.move_to(vc.channel)
            return connection
        else:
            vc = await vc.channel.connect()
            self.connections.update({message.guild.id: vc})
            return vc

    def args_to_filters(self, args):
        filters = {}
        if '--time' in args:
            index = args.index('--time')
            try:
                seconds = args[index+1]
            except IndexError:
                return "You must provide an amount of seconds for the time."
            try:
                seconds = int(seconds)
            except ValueError:
                return "You must provide an integer value."
            filters.update({'time': seconds})
        if '--users' in args:
            users = []
            index = args.index('--users')+1
            while True:
                try:
                    users.append(int(args[index]))
                except IndexError:
                    break
                except ValueError:
                    break
                index += 1
            if not users:
                return "You must provide at least one user, or multiple users separated by spaces."
            filters.update({'users': users})
        return filters

    def get_encoding(self, args):
        if '--output' in args:
            index = args.index('--output')
            try:
                encoding = args[index+1].lower()
                if encoding not in discord.Sink.valid_encodings:
                    return
                return encoding
            except IndexError:
                return
        else:
            return 'wav'

    async def finished_callback(self, sink, channel, *args):
        # Note: sink.audio_data = {user_id: AudioData}
        recorded_users = [
            f" <@{str(user_id)}> ({os.path.split(audio.file)[1]}) " for user_id, audio in sink.audio_data.items()]
        for user_id, audio in sink.audio_data.items():
            # send file to channel
            await channel.send(f"<@{user_id}>", file=discord.File(audio.file))
        await channel.send(f"Finished! Recorded audio for {', '.join(recorded_users)}.")

    async def on_voice_state_update(self, member, before, after):
        if member.id != self.user.id:
            return
        # Filter out updates other than when we leave a channel we're connected to
        if member.guild.id not in self.connections and (not before.channel and after.channel):
            return

    @commands.command(name='pause_rec', aliases=['pause_recording'], pass_context=True)
    async def toggle_pause(self, ctx: commands.Context):
        vc = await self.get_vc(ctx)
        vc.toggle_pause()
        await ctx.send(f"The recording has been {'paused' if vc.paused else 'unpaused'}")

    @commands.command(name='stop_rec', aliases=['stop_recording'], pass_context=True)
    async def stop_recording(self, ctx: commands.Context):
        vc = await self.get_vc(ctx)
        vc.stop_recording()

    @commands.command(name="record", pass_context=True)
    async def _record(self, ctx: commands.Context, *args):
        vc = await self.get_vc(ctx)
        args = list(args)
        print(args)
        filters = self.args_to_filters(args)
        print(filters)
        if type(filters) == str:
            return await ctx.send(filters)
        encoding = self.get_encoding(args)
        if encoding is None:
            return await ctx.send("You must provide a valid output encoding.")
        vc.start_recording(discord.Sink(
            encoding=encoding, filters=filters), self.finished_callback, ctx)

        await ctx.send("The recording has started!")

    @commands.command(name="recognize", pass_context=True)
    async def _recognize(self, ctx: commands.Context, user_id: int = None):
        if user_id is None:
            user_id = ctx.author.id
        args = "--time 10 --users user_id"
        await ctx.invoke(self.bot.get_command('record'), args)


async def setup(bot):
    await bot.add_cog(VoiceListener(bot))
