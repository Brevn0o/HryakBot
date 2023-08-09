import os

import disnake
from disnake.ext import commands

from pig_code.core import config
from pig_code.utils.db_api.tech import *


class PigBot:

    def __init__(self):
        intents = disnake.Intents.default()
        intents.members = True
        if not config.TEST:
            self.pig_bot = commands.AutoShardedInteractionBot(intents=intents, strict_localization=True, shard_count=2,
                                                              max_messages=10000,
                                                          activity=disnake.Activity(type=disnake.ActivityType.watching,
                                                                                    name=f'/help'))
        else:
            self.pig_bot = commands.InteractionBot(intents=intents, strict_localization=True)

    def load_cogs(self):
        cogs_path = 'pig_code/cogs'
        for file in os.listdir(cogs_path):
            if file.endswith('.py'):
                self.pig_bot.load_extension(f'{cogs_path.replace("/", ".")}.{file[:-3]}')


pig_bot = PigBot()
pig_bot.load_cogs()


pig_bot.pig_bot.run(config.TOKEN)
