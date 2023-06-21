import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def invite_components(lang) -> list:
    components = [
        disnake.ui.Button(
            style=disnake.ButtonStyle.green,
            label=locales['words']['accept'][lang],
            custom_id=f'in:accept',
        ),
        disnake.ui.Button(
            style=disnake.ButtonStyle.red,
            label=locales['words']['reject'][lang],
            custom_id=f'in:reject',
        )
    ]
    return components


def duel_message_url(lang, url) -> list:
    components = [
        disnake.ui.Button(
            style=disnake.ButtonStyle.link,
            label=locales['duel']['message_url_btn'][lang],
            url=url
        )
    ]
    return components