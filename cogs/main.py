import asyncio
import re

from datetime import datetime, timedelta
from discord.ext.commands import (
    Bot,
    Cog,
    command,
    Context,
    RoleConverter,
    TextChannelConverter,
)
from discord import Message, TextChannel
from sqlitedict import SqliteDict
from cogs._utils import strfdelta


class Main(Cog):
    def __init__(self, bot: Bot):
        self.bump_roles = SqliteDict("guild-bump-roles.sqlite3", autocommit=True)
        self.loop = bot.loop  # event loop spawned by bot.run()

    @staticmethod
    def is_successful_bump(msg: Message):
        """Tell if a discord message is a successful DISBOARD bump."""

        successful_bump = r"""<@!?\d+>,\s*
\s*Bump done :thumbsup:
\s*Check it on DISBOARD: https://disboard\.org/"""

        if len(msg.embeds) != 1 or msg.author.id != 302050872383242240:
            return False
        elif re.match(successful_bump, msg.embeds[0].description) is None:
            return False
        else:
            return True

    def ping_target(self, channel: TextChannel):
        asyncio.ensure_future(
            channel.send(
                f"A bump is available %s!" % self.bump_roles[channel.guild.id]
            ),
            loop=self.loop,
        )

    @command(aliases=["schping", "schedping", "sping", "sp"])
    async def scheduleping(
        self, ctx: Context, channel: TextChannelConverter = None, scanlimit: int = None
    ):
        """Scan the last successful bump throughout the current channel and schedule a ping to do after
        remaining time if available.

        Scan is performed to <scanlimit> amount of messages in <channel> text channel only if they are
        specified."""

        if ctx.guild.id not in self.bump_roles:
            await ctx.send("No bumper role was set to notify")
            return

        bump_time = None
        channel = ctx.channel if channel is None else channel

        async for msg in channel.history(limit=scanlimit):
            if self.is_successful_bump(msg):
                bump_time = msg.created_at
                break  # discard everything else

        if bump_time is None:
            await ctx.send("Scan revealed no successful bump")

        time_diff = datetime.utcnow() - bump_time

        if time_diff >= timedelta(hours=2):
            self.ping_target(ctx.channel)
        else:
            delay = timedelta(hours=2) - time_diff

            self.loop.call_later(delay.total_seconds(), self.ping_target, ctx.channel)

            await ctx.send(
                strfdelta(
                    delay, "Ping scheduled to be called %H hrs %M min %S secs later"
                )
            )

    @command(aliases=["sr", "roleset", "rset"])
    async def setrole(self, ctx: Context, role: RoleConverter):
        """Set the bump role for the current guild, empty implies to unset the bump role."""

        if ctx.guild.id in self.bump_roles and role is None:
            del self.bump_roles[ctx.guild.id]
        else:
            self.bump_roles[ctx.guild.id] = role.mention

    @Cog.listener()
    async def on_message(self, msg: Message):
        if msg.guild.id in self.bump_roles:
            if self.is_successful_bump(msg):
                self.loop.call_later(7200, self.ping_target, msg.channel)
