from hryak.game_functions import GameFunc

from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *


async def generate_basic_buffs_embed(inter, lang, thumbnail_url=None):
    description = f'{translate(Locales.Buffs.main_page_desc, lang)}\n'
    buffs = await hryak.game_functions.GameFunc.get_all_pig_buffs(inter.user.id, inter.client)
    for buff in buffs:
        if await Item.exists(buff):
            description += f'\n- {await Pig.get_buff_name(buff, lang)} x{await Pig.get_buff_amount(inter.user.id, buff)}'
            if await Item.get_buff_duration(buff) is not None:
                description += f'\n{translate(Locales.Buffs.buff_expires_in, lang, {'expiration_timestamp': await Pig.get_buff_expiration_timestamp(inter.user.id, buff)})}'
    if description == f'{translate(Locales.Buffs.main_page_desc, lang)}\n':
        description += f'\n{translate(Locales.Buffs.main_page_no_buffs_desc, lang)}'
    embed = generate_embed(
        title=translate(Locales.Buffs.main_page_title, lang),
        description=description,
        prefix=Func.generate_prefix('⚡'),
        inter=inter,
        thumbnail_url=thumbnail_url
    )
    return embed


async def generate_buffs_multipliers_embed(inter, lang, buff_type: str, thumbnail_url=None):
    title = None
    description = None
    title = translate(hryak.locale.Locale.BuffTypes[buff_type], lang)
    match buff_type:
        case 'weight':
            description = f'{translate(Locales.Buffs.weight_buffs_desc, lang)}\n\n'
        case 'pooping':
            description = f'{translate(Locales.Buffs.pooping_buffs_desc, lang)}\n\n'
        case 'vomit_chance':
            description = f'{translate(Locales.Buffs.vomit_chance_desc, lang)}\n\n'
    base_multiplier_value_text = translate(Locales.Buffs.base_multiplier_value, lang,
                                           {'mult': round(hryak.config.base_buff_multipliers[buff_type] * 100)})
    description += f'- {base_multiplier_value_text}'

    buffs = await hryak.GameFunc.get_all_pig_buffs(inter.user.id, inter.client)

    def sort_key(x):
        val = x[1].get(buff_type, '')
        if val.startswith('x'):
            return 1, float(val[1:]) if val[1:] else float('inf')
        else:
            return 0, float(val[1:]) if val.startswith('+') and val[1:] else float(val) if val else float('inf')

    buffs = dict(sorted(buffs.items(), key=sort_key))

    for buff in buffs:
        if buff_type in buffs[buff]:
            description += f'\n- {await Pig.get_buff_name(buff, lang)}: **{buffs[buff][buff_type][0]}{round(float(buffs[buff][buff_type][1:]) * 100)}%**'
    calculated_buffs = await GameFunc.calculate_buff_multipliers(inter.user.id, False, inter.client)
    description += f'\n> {translate(Locales.Buffs.final_multiplier_value, lang,
                                    {'mult': round(calculated_buffs[buff_type] * 100)})}'
    embed = generate_embed(
        title=title,
        description=description,
        prefix=Func.generate_prefix('⚡'),
        inter=inter,
        thumbnail_url=thumbnail_url,
    )
    return embed
