import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def profile(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['profile']['profile_title'][lang],
        description=locales['profile']['profile_desc'][lang].format(balance=User.get_money(inter.author.id)),
        prefix=Func.generate_prefix('🐽'),
        thumbnail_url=inter.author.avatar.url,
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        fields=[{'title': locales['profile']['pig_field_title'][lang],
                 'value': locales['profile']['pig_field_value'][lang].format(
                     pig_name=Pig.get_name(inter.author.id, 0),
                     weight=Pig.get_weight(inter.author.id, 0))}]
    )
    return embed


def set_language(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['set_language']['scd_title'][lang],
                                    description=locales['set_language']['scd_desc'][
                                        lang],
                                    prefix=Func.generate_prefix('scd'),
                                    footer=Func.generate_footer(inter),
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed
