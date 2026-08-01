import os
from dotenv import load_dotenv

load_dotenv()

from .imports import *


def get_env(key, value_type=None):
    value = os.getenv(key)
    if value_type:
        if value_type == list:
            return eval(value)
        elif value_type == bool:
            return value.lower() in ['true']
        return value_type(value)
    return value

TOKEN = get_env('TOKEN')
TEST_TOKEN = get_env('TEST_TOKEN')
TEST = get_env('TEST', bool)
ADMIN_GUILDS = get_env('ADMIN_GUILDS', list)
TEST_GUILDS = get_env('TEST_GUILDS', list)
PUBLIC_TEST_GUILDS = get_env('PUBLIC_TEST_GUILDS', list)
DEVELOPER_USERNAME = get_env('DEVELOPER_USERNAME')

SDC_TOKEN = get_env('SDC_TOKEN')  # https://bots.server-discord.com/
IMGBB_TOKEN = get_env('IMGBB_TOKEN')  # https://api.imgbb.com/
THUMBSNAP_TOKEN = get_env('THUMBSNAP_TOKEN')  # https://thumbsnap.com/
BOTICORD_TOKEN = get_env('BOTICORD_TOKEN')  # https://boticord.top/

# github version
GITHUB_PUBLIC_VERSION = True  # don't change this line

# support guild config

RU_BOT_GUILD_ID = int(get_env('RU_BOT_GUILD'))
EN_BOT_GUILD_ID = int(get_env('EN_BOT_GUILD'))

BOT_GUILDS = {RU_BOT_GUILD_ID: {'type': 'ru.main',
                                'url': get_env('RU_BOT_GUILD_URL'),
                                'guild_count_channel': int(get_env('RU_BOT_STATS_CHANNEL')),
                                # id of a channel (has to be a voice channel)
                                'halyava_channel': int(get_env('RU_BOT_HALYAVA_CHANNEL')),  # id of a channel
                                'not_verified_role': int(get_env('RU_NOT_VERIFIED_ROLE'))},  # id of a role
              EN_BOT_GUILD_ID: {'type': 'en.main',
                                'url': get_env('EN_BOT_GUILD_URL')}}

BOT_AUTH_LINK = get_env('BOT_AUTH_LINK')

BOT_STATS_CHANNEL = int(get_env('RU_BOT_STATS_CHANNEL'))  # id of a channel (has to be a voice channel)
BOT_HALYAVA_CHANNEL = int(get_env('RU_BOT_HALYAVA_CHANNEL'))  # id of a channel

# users
PROMOCODERS = get_env('PROMOCODERS', list)  # users who are able to create promocodes
HALYAVERS = get_env('HALYAVERS', list)  # users who are able to give rewards in "halyava" channel

# paths
TEMP_FOLDER_PATH = get_env('TEMP_FOLDER_PATH')

# webhooks
DEBUGGER_WEBHOOK = get_env('DEBUGGER_WEBHOOK')
REPORT_WEBHOOKS = get_env('REPORT_WEBHOOKS', list)

# redis - optional shared cache, so several bots see the same data
REDIS_HOST = get_env('REDIS_HOST')
REDIS_PORT = get_env('REDIS_PORT', int) if get_env('REDIS_PORT') else 6379
REDIS_PASSWORD = get_env('REDIS_PASSWORD')
REDIS_SSL = get_env('REDIS_SSL', bool) if get_env('REDIS_SSL') else False  # true for rediss://
REDIS_SSL_VERIFY = get_env('REDIS_SSL_VERIFY', bool) if get_env('REDIS_SSL_VERIFY') else False
REDIS_DB = get_env('REDIS_DB', int) if get_env('REDIS_DB') else 0

# db
mysql_info = {
    'host': get_env('DB_HOST'),
    'port': get_env('DB_PORT', int),
    'user': get_env('DB_USER'),
    'password': get_env('DB_PASSWORD'),
    'database': get_env('DB_NAME') if not TEST else get_env('TEST_DB_NAME')
}

if TEST:
    TOKEN = TEST_TOKEN
else:
    TOKEN = TOKEN

# ------------------ not private --------------------

from hryak import setters

# logging disabled for now: no-op instead of writing to a local logs file
async def _disabled_add_log(*args, **kwargs):
    pass
hryak.Func.add_log = _disabled_add_log

hryak.db_api.connection.pool.set_config(**mysql_info)

setters.set_platform('discord')
if REDIS_HOST:
    setters.set_redis_cache(REDIS_HOST, REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,
                            ssl=REDIS_SSL, ssl_verify=REDIS_SSL_VERIFY)
setters.set_test_mode(TEST)
setters.set_bot_guilds(BOT_GUILDS)
setters.set_temp_folder_path(TEMP_FOLDER_PATH)

if TEST:
    setters.set_pig_feed_cooldown(5)
    setters.set_pig_butcher_cooldown(15)
    setters.set_streak_timeout(30)

# embed colors
main_color = 0xc7604c
error_color = 0xc94312
warn_color = 0xe0bb36
success_color = 0x2fc256
premium_color = 0x61dfff

image_links = {'inventory': 'https://thumbsnap.com/i/4EBKi23j.png',
               'invite': 'https://thumbsnap.com/i/JQ3RPzX1.png',
               'trade': 'https://thumbsnap.com/i/Hm1iX2Mj.png',
               'shop': 'https://thumbsnap.com/i/JkjRGKx2.png',
               'top': 'https://thumbsnap.com/i/2QLNAtCR.png',
               'coins_ru_ruble_prices': 'https://i.postimg.cc/yxCJCCcB/IMG-7540.png',
               'image_is_blocked': 'https://thumbsnap.com/i/EQ1EaKmW.png',
               'buffs': 'https://thumbsnap.com/i/ajKoAv44.png',
               'quests': 'https://i.ibb.co/Htmxmxj/Quest-Main-Available-Icon-001.png'}

shops_emojis = {
    'daily_shop': '🎨',
    'case_shop': '📦',
    'consumables_shop': '💊',
    'tools_shop': '🔪',
    'premium_skins_shop': '💵',
    'coins_shop': '🪙',
    'donation_shop': '🍩',
}

payment_methods_for_languages = {
    'ru': ['donatello'],
    'en': []
}
