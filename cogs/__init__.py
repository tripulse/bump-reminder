from cogs.main import Main
from discord.ext.commands import Bot


def setup(bot: Bot):
    bot.add_cog(Main(bot))
