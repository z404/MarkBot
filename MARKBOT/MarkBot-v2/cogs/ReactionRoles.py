import discord
from discord.ext import commands
import json
import atexit
import uuid
import asyncio
from discord.ext.commands.converter import EmojiConverter, PartialEmojiConverter
from discord_slash import cog_ext, SlashContext

reaction_roles_data = {}

try:
    with open("reaction_roles.json") as file:
        reaction_roles_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as ex:
    with open("reaction_roles.json", "w") as file:
        json.dump({}, file)


@atexit.register
def store_reaction_roles():
    with open("reaction_roles.json", "w") as file:
        json.dump(reaction_roles_data, file)


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None:
            await user.add_roles(role, reason="ReactionRole")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None:
            await user.remove_roles(role, reason="ReactionRole")

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction(
        self,
        ctx,
        emote,
        role: discord.Role,
        channel: discord.TextChannel,
        title,
        message,
    ):
        embed = discord.Embed(title=title, description=message)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction_add(self, ctx, emote, role: discord.Role, channel: discord.TextChannel, message_id):
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, message_id)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reactions(self, ctx):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title="Reaction Roles")
        if data is None:
            embed.description = "There are no reaction roles set up right now."
        else:
            for index, rr in enumerate(data):
                emote = rr.get("emote")
                role_id = rr.get("roleID")
                role = ctx.guild.get_role(role_id)
                channel_id = rr.get("channelID")
                message_id = rr.get("messageID")
                embed.add_field(
                    name=index,
                    value=f"{emote} - @{role} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
                    inline=False,
                )
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction_remove(self, ctx, index: int):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title=f"Remove Reaction Role {index}")
        rr = None
        if data is None:
            embed.description = "Given Reaction Role was not found."
        else:
            embed.description = (
                "Do you wish to remove the reaction role below? Please react with 🗑️."
            )
            rr = data[index]
            emote = rr.get("emote")
            role_id = rr.get("roleID")
            role = ctx.guild.get_role(role_id)
            channel_id = rr.get("channelID")
            message_id = rr.get("messageID")
            _id = rr.get("id")
            embed.set_footer(text=_id)
            embed.add_field(
                name=index,
                value=f"{emote} - @{role} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
                inline=False,
            )
        msg = await ctx.send(embed=embed)
        if rr is not None:
            await msg.add_reaction("🗑️")

            def check(reaction, user):
                return(user == ctx.message.author and str(reaction.emoji) == "🗑️")
            msg = await self.bot.get_channel(channel_id).fetch_message(message_id)
            await msg.remove_reaction(emote, self.bot.user)
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=15)
                data.remove(rr)
                reaction_roles_data[str(guild_id)] = data
                store_reaction_roles()
            except asyncio.TimeoutError:
                await ctx.send("Timed out. Operation cancelled.")

    def add_reaction(self, guild_id, emote, role_id, channel_id, message_id):
        if not str(guild_id) in reaction_roles_data:
            reaction_roles_data[str(guild_id)] = []
        reaction_roles_data[str(guild_id)].append(
            {
                "id": str(uuid.uuid4()),
                "emote": emote,
                "roleID": role_id,
                "channelID": channel_id,
                "messageID": message_id,
            }
        )
        store_reaction_roles()

    def parse_reaction_payload(self, payload: discord.RawReactionActionEvent):
        guild_id = payload.guild_id
        data = reaction_roles_data.get(str(guild_id), None)
        if data is not None:
            for rr in data:
                emote = rr["emote"]
                if str(payload.message_id) == str(rr["messageID"]):
                    if str(payload.channel_id) == str(rr["channelID"]):
                        if str(payload.emoji) == emote:
                            guild = self.bot.get_guild(guild_id)
                            role = guild.get_role(rr.get("roleID"))
                            user = guild.get_member(payload.user_id)
                            return role, user
        return None, None

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction_role_clear(self, ctx):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        if data is not None:
            print()
            del reaction_roles_data[str(guild_id)]
            store_reaction_roles()
        await ctx.send("Reaction Roles cleared.")

    @commands.has_permissions(manage_channels=True)
    @cog_ext.cog_slash(name="create_reaction_role")
    async def reaction_slash(
        self,
        ctx,
        emote: PartialEmojiConverter,
        role: discord.Role,
        channel: discord.TextChannel,
        title,
        message,
    ):
        '''Create a reaction role message'''
        embed = discord.Embed(title=title, description=message)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)
        await ctx.send("Reaction role created.", hidden=True)

    @cog_ext.cog_slash(name="add_reaction_role")
    async def reaction_slash_add(
        self,
        ctx,
        emote: PartialEmojiConverter,
        role: discord.Role,
        channel: discord.TextChannel,
        message_id: str
    ):
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, message_id)
        await ctx.send("Reaction role added.", hidden=True)


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
