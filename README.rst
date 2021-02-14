Reminds of bumping a Discord guild on DISBOARD. It pings a role as per guild, the targetted role is stored in a Sqlite3 database.

Running
  Acquire the token of your bot and put it in ``DISCORD_BOT_TOKEN`` environ. In console run ``python3 bot.py`` which will run forever.

Configuring
  Set a role to be used for notifying users of an available bump by :code:`@BotMention sr role-name`.
 
Schedule
  Go to a guild channel where bumps are done and schedule a ping to bumpers by ``@BotMenton sp``, it will scan through message in the
  current channel until a successful bump is found. You can specify with channel to search in and how many messages to scan at a maximum.
  
If the bot goes down or has to go down repeat the *Schedule* step.
