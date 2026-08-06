from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *


async def pig_message(guild_id, lang) -> discord.Embed:
    last_feed = await GuildPig.get_last_feed(guild_id)
    inventory = await GuildPig.get_inventory(guild_id)
    embed = generate_embed(title=translate(Locales.GuildPig.message_title, lang,
                                           {'pig': await GuildPig.get_name(guild_id)}),
                           description=translate(Locales.GuildPig.message_desc, lang,
                                                 {'weight': await GuildPig.get_weight(guild_id),
                                                  'kg': translate(hryak.locale.Locale.Global.kg, lang),
                                                  'coins': await Item.get_amount('coins', inventory=inventory),
                                                  'coins_emoji': await Item.get_emoji('coins'),
                                                  'last_feed': translate(Locales.GuildPig.never_fed, lang)
                                                  if last_feed is None else f'<t:{last_feed}:R>'}),
                           prefix=Func.generate_prefix('🐷'),
                           # the pig's own message is all about the pig, so it gets the
                           # big image slot rather than the corner thumbnail
                           image_url=await DisUtils.generate_guild_pig(guild_id),
                           timestamp=False)
    return embed


async def admin_message(guild_id, lang) -> discord.Embed:
    """The panel that sits in the staff-only channel."""
    inventory = await GuildPig.get_inventory(guild_id)
    embed = generate_embed(title=translate(Locales.GuildPigAdmin.message_title, lang),
                           description=translate(Locales.GuildPigAdmin.message_desc, lang,
                                                 {'coins': await Item.get_amount('coins', inventory=inventory),
                                                  'coins_emoji': await Item.get_emoji('coins')}),
                           prefix=Func.generate_prefix('🛠️'),
                           timestamp=False)
    return embed


async def weekly_rewards(guild_id, lang, response) -> discord.Embed:
    """The weekly pooping, announced in the notifications channel.

    People are mentioned rather than looked up - discord renders the name for us, and the
    alternative is fetching every feeder of the week just to print them.
    """
    medals = ['🥇', '🥈', '🥉']
    emoji = await Item.get_emoji(response['item_id'])
    paid = sorted(((uid, r) for uid, r in response['rewards'].items() if r['paid']),
                  key=lambda pair: pair[1]['place'])
    # only the top few are named. everybody was paid either way - an embed field stops at
    # 1024 characters, which a busy server would blow straight past, and discord rejects
    # the whole message when it does
    shown = paid[:hryak.config.guild_pig_reward_top_shown]
    lines = ''
    for user_id, reward in shown:
        place = reward['place']
        lines += (f"{medals[place] if place < 3 else f'{place + 1}.'}・<@{user_id}> - "
                  f"**{reward['amount']}** {emoji} "
                  f"({reward['kg']} {translate(hryak.locale.Locale.Global.kg, lang)})\n")
    if len(paid) > len(shown):
        lines += translate(Locales.GuildPig.pooped_more, lang, {'count': len(paid) - len(shown)})
    return generate_embed(
        title=translate(Locales.GuildPig.pooped_title, lang,
                        {'pig': await GuildPig.get_name(guild_id)}),
        description=translate(Locales.GuildPig.pooped_desc, lang,
                              {'total': response['total_poop'], 'emoji': emoji,
                               'total_kg': response['total_kg'],
                               'kg': translate(hryak.locale.Locale.Global.kg, lang),
                               'feeders': len(paid),  # everyone paid, not just the ones named
                               'weight_bonus': response['weight_bonus']}),
        prefix=Func.generate_prefix('💩'),
        color=config.success_color,
        timestamp=False,
        fields=[{'name': translate(Locales.GuildPig.pooped_who, lang), 'value': lines}] if lines else None)


async def top(inter, lang, response, title=None, desc=None, prefix_emoji='🐖') -> discord.Embed:
    """Same layout as the user top, with server names instead of user names.

    title and desc are passed in so the one builder can draw any of the server boards.
    """
    if title is None:
        title = Locales.GuildPig.top_title
    if desc is None:
        desc = Locales.GuildPig.top_desc
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
    embed = generate_embed(title=translate(title, lang),
                           description=translate(desc, lang) if fields
                           else translate(Locales.GuildPig.top_empty, lang),
                           prefix=Func.generate_prefix(prefix_emoji),
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


async def simple(inter, lang, title, description, options: dict = None, prefix='🛍️',
                 color=None) -> discord.Embed:
    """One embed shape for every poll message - only the words differ."""
    return generate_embed(title=translate(title, lang),
                          description=translate(description, lang, options or {}),
                          prefix=Func.generate_prefix(prefix),
                          color=color if color is not None else config.main_color,
                          inter=inter)


async def poll_outcome(lang, response, item_name, currency_emoji=None) -> discord.Embed:
    """What gets posted in the poll channel once a vote closes.

    Every kind of vote is announced the same way - only what a passing one says differs, so
    that is the only thing looked up by kind.
    """
    poll = response['poll']
    options = {'item': item_name, 'price': poll.get('price'), 'currency_emoji': currency_emoji,
               'yes': response['yes'], 'no': response['no'],
               'votes': response['yes'] + response['no'], 'needed': response['needed']}
    by_kind = {
        'shop': {hryak.Status.SUCCESS: (Locales.GuildPig.poll_passed_title,
                                        Locales.GuildPig.poll_passed_desc, config.success_color, 'scd'),
                 hryak.Status.EXPIRED: (Locales.GuildPig.poll_rejected_title,
                                        Locales.GuildPig.poll_rejected_desc, config.error_color, 'error'),
                 hryak.Status.NOT_READY: (Locales.GuildPig.poll_no_quorum_title,
                                          Locales.GuildPig.poll_no_quorum_desc, config.warn_color, 'warn')},
        'wear': {hryak.Status.SUCCESS: (Locales.GuildPig.wear_passed_title,
                                        Locales.GuildPig.remove_passed_desc if poll.get('remove')
                                        else Locales.GuildPig.wear_passed_desc, config.success_color, 'scd'),
                 # a vote that failed leaves the pig alone either way round, so taking
                 # something off and putting it on are announced the same
                 hryak.Status.EXPIRED: (Locales.GuildPig.poll_rejected_title,
                                        Locales.GuildPig.wear_rejected_desc, config.error_color, 'error'),
                 hryak.Status.NOT_READY: (Locales.GuildPig.poll_no_quorum_title,
                                          Locales.GuildPig.wear_no_quorum_desc, config.warn_color, 'warn')}}
    outcomes = {hryak.Status.NO_MONEY: (Locales.GuildPig.poll_no_money_title,
                                        Locales.GuildPig.poll_no_money_desc, config.error_color, 'error'),
                # the pig lost the skin while the server was voting on wearing it
                hryak.Status.NOT_ENOUGH_ITEMS: (Locales.GuildPig.wear_gone_title, Locales.GuildPig.wear_gone_desc,
                                                config.error_color, 'error'),
                **by_kind[response['kind']]}
    title, desc, color, prefix = outcomes[response['status']]
    return generate_embed(title=translate(title, lang),
                          description=translate(desc, lang, options),
                          prefix=Func.generate_prefix(prefix),
                          color=color,
                          timestamp=False)


async def buy_cancelled(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPig.buy_cancelled_title, lang),
                           description=translate(Locales.GuildPig.buy_cancelled_desc, lang),
                           prefix=Func.generate_prefix('🛍️'),
                           inter=inter)
    return embed


async def help_(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPig.help_title, lang),
                           description=translate(Locales.GuildPig.help_desc, lang),
                           prefix=Func.generate_prefix('🐷'),
                           inter=inter)
    return embed


async def setup(inter, lang, channel, poll_channel, notification_channel, admin_channel) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.GuildPigSetup.scd_title, lang),
                           description=translate(Locales.GuildPigSetup.scd_desc, lang,
                                                 {'pig': await GuildPig.get_name(inter.guild.id),
                                                  'channel': channel.mention,
                                                  'poll_channel': poll_channel.mention,
                                                  'notification_channel': notification_channel.mention,
                                                  'admin_channel': admin_channel.mention}),
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
