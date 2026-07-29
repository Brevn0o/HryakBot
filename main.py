import asyncio
import ssl
import logging

logging.basicConfig(level=logging.INFO)

def loop_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, ssl.SSLError) and "bad record mac" in str(exc).lower():
        logging.warning("[SSL] bad record mac caught: %s", exc)
        # you can schedule a retry or pool reset here, e.g.:
        # asyncio.create_task(reset_pool())
        return  # swallow it
    # fallback for everything else
    loop.default_exception_handler(context)

# install this **before** you start your bot
loop = asyncio.get_event_loop()
loop.set_exception_handler(loop_exception_handler)

from pig_code.core import *
from pig_code.utils.functions import Translator
from pig_code.utils import error_callbacks


class PigBot:

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        if not config.TEST:
            self.bot = commands.AutoShardedBot(command_prefix='NO_PREFIX', intents=intents, strict_localization=True, shard_count=5,
                                               max_messages=1000, chunk_guilds_at_startup=False,
                                               activity=discord.Activity(
                                                   type=discord.ActivityType.watching,
                                                   name=f'/help'))
        else:
            self.bot = commands.Bot(command_prefix='NO_PREFIX', intents=intents, strict_localization=True, chunk_guilds_at_startup=False)

        self.bot.setup_hook = self.setup_hook

    async def setup_hook(self):
        await hryak.db_api.connection.pool.create_pool()
        print('> Pool is created')
        cogs_path = 'pig_code/cogs'
        for file in os.listdir(cogs_path):
            if file.endswith('.py'):
                print(f"> Loading cog: {file}")
                await self.bot.load_extension(f'{cogs_path.replace("/", ".")}.{file[:-3]}')
        await self.bot.tree.set_translator(Translator())


    def run(self, token):
        self.bot.run(token)


bot_instance = PigBot()


@bot_instance.bot.tree.error
async def on_app_command_error(inter: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    await error_callbacks.error(error, inter)


bot_instance.run(config.TOKEN)


