from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *


async def pig_message(guild_id, lang) -> discord.Embed:
    last_feed = await GuildPig.get_last_feed(guild_id)
    embed = generate_embed(title=translate(Locales.GuildPig.message_title, lang,
                                           {'pig': await GuildPig.get_name(guild_id)}),
                           description=translate(Locales.GuildPig.message_desc, lang,
                                                 {'weight': await GuildPig.get_weight(guild_id),
                                                  'kg': translate(hryak.locale.Locale.Global.kg, lang),
                                                  'last_feed': translate(Locales.GuildPig.never_fed, lang)
                                                  if last_feed is None else f'<t:{last_feed}:R>'}),
                           prefix=Func.generate_prefix('🐷'),
                           timestamp=False)
    return embed


async def top(inter, lang, response) -> discord.Embed:
    """Same layout as the user top, with server names instead of user names."""
    leader_emojis = ['🥇', '🥈', '🥉']
    guilds_list = response.get('guilds')

    def generate_line(place, guild):
        name = inter.client.get_guild(int(guild[0]))
        return f'> {leader_emojis[place] if place < 3 else place + 1}・{name if name is not None else guild[0]}' \
               f' - **{guild[1]}** {guild[2]}\n'

    fields = []
    best_guilds_field = {'name': translate(Locales.Top.best_of_the_bests, lang),
                         'value': '',
                         'inline': False}
    for n, i in enumerate(guilds_list[:3]):
        best_guilds_field['value'] += generate_line(n, i)
    fields.append(best_guilds_field)
    other_guilds_field = {'name': translate(Locales.Top.also_not_bad, lang),
                          'value': '',
                          'inline': False}
    for n, i in enumerate(guilds_list[3:]):
        other_guilds_field['value'] += generate_line(n + 3, i)
    if other_guilds_field['value']:
        fields.append(other_guilds_field)
    guild_position = response.get('guild_position')
    if guild_position is not None:
        position_line = f"\n\n{translate(Locales.GuildPig.top_your_position, lang, {'place': guild_position + 1})}"
        if other_guilds_field['value']:
            other_guilds_field['value'] += position_line
        elif best_guilds_field['value']:
            best_guilds_field['value'] += position_line
    if not best_guilds_field['value']:
        fields = []
    embed = generate_embed(title=translate(Locales.GuildPig.top_title, lang),
                           description=translate(Locales.GuildPig.top_desc, lang) if fields
                           else translate(Locales.GuildPig.top_empty, lang),
                           prefix=Func.generate_prefix('🐖'),
                           inter=inter,
                           thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                               config.image_links['top']),
                           fields=fields)
    return embed


async def fed(inter, lang, guild_id, response) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPig.fed_title, lang,
                                           {'pig': await GuildPig.get_name(guild_id)}),
                           description=translate(Locales.GuildPig.fed_desc, lang,
                                                 {'weight_added': response['weight_added'],
                                                  'weight': response['weight'],
                                                  'kg': translate(hryak.locale.Locale.Global.kg, lang),
                                                  'try_again': response['try_again']}),
                           prefix=Func.generate_prefix('🌾'),
                           inter=inter)
    return embed


async def not_ready(inter, lang, response) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPig.not_ready_title, lang),
                           description=translate(Locales.GuildPig.not_ready_desc, lang,
                                                 {'try_again': response['try_again']}),
                           color=config.warn_color,
                           prefix=Func.generate_prefix('warn'),
                           inter=inter)
    return embed


async def help_(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPig.help_title, lang),
                           description=translate(Locales.GuildPig.help_desc, lang),
                           prefix=Func.generate_prefix('🐷'),
                           inter=inter)
    return embed


async def setup(inter, lang, channel) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPigSetup.scd_title, lang),
                           description=translate(Locales.GuildPigSetup.scd_desc, lang,
                                                 {'pig': await GuildPig.get_name(inter.guild.id),
                                                  'channel': channel.mention}),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def no_permissions(inter, lang, channel=None) -> discord.Embed:
    """Without a channel it means hryak could not make one itself."""
    if channel is None:
        description = translate(Locales.GuildPigSetup.cant_create_desc, lang)
    else:
        description = translate(Locales.GuildPigSetup.no_permissions_desc, lang, {'channel': channel.mention})
    embed = generate_embed(title=translate(Locales.GuildPigSetup.no_permissions_title, lang),
                           description=description,
                           color=config.error_color,
                           prefix=Func.generate_prefix('error'),
                           inter=inter)
    return embed
