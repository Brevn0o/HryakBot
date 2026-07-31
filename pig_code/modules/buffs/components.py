import asyncio
import datetime
import random

from ...core import *
from ...utils import *


async def choose_user(inter, lang, users):
    options = []
    for user_id in users:
        options.append(discord.SelectOption(
            label=await User.get_discord_name(inter.client, user_id),
            value=user_id,
        ))
    return discord.ui.Select(options=options, custom_id='view_profile',
                             placeholder=translate(Locales.Top.placeholder, lang))
