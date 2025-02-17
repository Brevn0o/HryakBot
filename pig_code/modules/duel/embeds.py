from ...core import *
from ...utils import *


def fight_is_starting(inter, lang, user: discord.User, time_to_start: int, chances) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.Duel.fight_is_starting_title, lang, {'time_to_start': time_to_start}),
        description=translate(Locales.Duel.fight_is_starting_desc, lang, {'pig1': Pig.get_name(inter.user.id), 'pig2': Pig.get_name(user.id)}),
        prefix=Func.generate_prefix('⚔️'),
        inter=inter,
        fields=[{'name': f'{Pig.get_name(inter.user.id)}',
                 'value': translate(Locales.Duel.fight_starting_field_value, lang, {'weight': Pig.get_weight(inter.user.id), 'chance': chances[0]}),
                 'inline': True},
                {'name': f'{Pig.get_name(user.id)}',
                 'value': translate(Locales.Duel.fight_starting_field_value, lang, {'weight': Pig.get_weight(user.id),
                                                                               'chance': chances[1]}),
                 'inline': True
                 },
                ],
    )
    return embed


def fight_is_going(inter, lang, user: discord.User, gif) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.Duel.fight_is_going_title, lang),
        description=translate(Locales.Duel.fight_is_going_desc, lang, {'pig1': Pig.get_name(inter.user.id), 'pig2': Pig.get_name(user.id)}),
        image_url=gif,
        prefix=Func.generate_prefix('⚔️'),
        inter=inter,
    )
    return embed


def user_won(inter, lang, user: discord.User, money_earned, gif) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.Duel.fight_ended_title, lang),
        description=translate(Locales.Duel.fight_ended_desc, lang, {'pig': Pig.get_name(user.id), 'user': user.mention, 'money_earned': money_earned}),
        thumbnail_url=gif,
        prefix=Func.generate_prefix('🎉'),
        inter=inter
    )
    return embed
