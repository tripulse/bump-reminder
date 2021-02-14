import os
import logging

from discord.ext.commands import Bot, when_mentioned

# attach logger to discord.py and set to INFO level
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

bot = Bot(command_prefix=when_mentioned)
bot.logger = logging.getLogger()

bot.load_extension("cogs")
bot.run(os.environ["DISCORD_BOT_TOKEN"])
