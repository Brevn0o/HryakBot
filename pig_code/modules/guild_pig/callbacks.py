from hryak import Status
from ...utils import *
from . import embeds, components
from ...utils.discord_utils import send_callback, generate_embed
from ...core import *


async def feed(inter):
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.guild_requests.feed_guild_pig(inter.user.id, inter.guild.id)
    if response['status'] == hryak.statuses.Status.NOT_READY:
        await send_callback(inter, embed=await embeds.not_ready(inter, lang, response),
                            ephemeral=True, edit_original_response=False)
        return
    if response['status'] != hryak.statuses.Status.SUCCESS:
        return
    await send_callback(inter, embed=await embeds.fed(inter, lang, inter.guild.id, response),
                        ephemeral=True, edit_original_response=False)
    await update_message(inter.client, inter.guild.id)


async def help_(inter):
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    await send_callback(inter, embed=await embeds.help_(inter, lang),
                        ephemeral=True, edit_original_response=False)


async def donate(inter):
    """Donating from the pig's menu asks for the amount in a modal instead of the
    confirm step the command uses - a modal opened from a component is scoped to the
    message it came from, so anything edited in place would land on the pig's message.
    The tax goes in the modal label so it is still seen before paying.
    """
    from ..other import embeds as other_embeds
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    currency = 'coins'
    result = await modals.get_item_amount(
        inter,
        translate(Locales.GuildPig.donate_modal_title, lang),
        translate(Locales.GuildPig.donate_modal_label, lang,
                  {'tax': await hryak.GameFunc.get_user_tax_percent(inter.user.id, currency)}),
        max_amount=await Item.get_amount(currency, inter.user.id))
    if not result:
        return
    modal_interaction, amount = result

    async def reply(embed, first: bool = False):
        await send_callback(modal_interaction, embed=embed, ephemeral=True,
                            edit_original_response=not first)

    response = await hryak.requests.post_requests.send_money(inter.user.id, amount, currency,
                                                             to_guild=inter.guild.id, confirmed=False)
    if response['status'] == hryak.Status.NO_MONEY:
        await reply(error_callbacks.default_error_embed(
            inter,
            translate(Locales.ErrorCallbacks.not_enough_money_title, lang),
            translate(Locales.ErrorCallbacks.not_enough_money_desc, lang)), first=True)
        return
    confirmation = await DisUtils.confirm_message(
        modal_interaction, lang, ephemeral=True, edit_original_response=False,
        description=translate(Locales.GuildPig.donate_confirm_desc, lang,
                              {'money': amount, 'user': inter.guild.name,
                               'tax': response.get('tax'),
                               'currency_emoji': await Item.get_emoji(currency),
                               'money_with_tax': response.get('amount_with_tax')}))
    if not confirmation:
        await reply(await other_embeds.cancel_sending_money(inter, lang))
        return
    response = await hryak.requests.post_requests.send_money(inter.user.id, amount, currency,
                                                             to_guild=inter.guild.id, confirmed=True)
    if response['status'] == hryak.Status.NO_MONEY:
        await reply(error_callbacks.default_error_embed(
            inter,
            translate(Locales.ErrorCallbacks.not_enough_money_title, lang),
            translate(Locales.ErrorCallbacks.not_enough_money_desc, lang)))
        return
    await reply(await other_embeds.transfer_money(inter, lang, inter.guild, amount, currency))
    await money_moved(inter.client, inter.guild.id, inter.user, amount, currency)
    await update_message(inter.client, inter.guild.id)
    await update_admin_message(inter.client, inter.guild.id)


async def notify(client, guild_id, embed):
    """Posts to the guild's notifications channel.

    Money moving in or out of the server is everyone's business, so it is announced there
    rather than only to whoever moved it. A vote's outcome is not sent here - it belongs
    next to the vote it settles. Quiet when the guild has no such channel, or when hryak can
    no longer post in it: a notification is never worth failing the thing it reports on.
    """
    channel_id = await GuildPig.get_channel(guild_id, key='notification_channel')
    if channel_id is None:
        return False
    channel = client.get_channel(int(channel_id))
    if channel is None:
        return False
    try:
        await channel.send(embed=embed)
    except discord.errors.HTTPException:
        return False
    return True


async def money_moved(client, guild_id, user, amount, currency, withdrawn: bool = False):
    """Announces money going into or out of the server, in the server's own language."""
    lang = await Guild.get_language(guild_id)
    inventory = await GuildPig.get_inventory(guild_id)
    return await notify(client, guild_id, generate_embed(
        title=translate(Locales.GuildPigAdmin.notify_withdraw_title if withdrawn
                        else Locales.GuildPigAdmin.notify_donate_title, lang),
        description=translate(Locales.GuildPigAdmin.notify_withdraw_desc if withdrawn
                              else Locales.GuildPigAdmin.notify_donate_desc, lang,
                              {'user': user.display_name, 'money': amount,
                               'currency_emoji': await Item.get_emoji(currency),
                               'left': await Item.get_amount(currency, inventory=inventory)}),
        prefix=Func.generate_prefix('🏦' if withdrawn else '🪙'),
        color=config.warn_color if withdrawn else config.success_color,
        timestamp=False))


async def admin_only(inter, lang):
    """The panel is in a staff-only channel, but that is a permission the server can change,
    so every action on it checks the right itself rather than trusting the walls."""
    if inter.user.guild_permissions.manage_guild:
        return True
    await send_callback(inter, ephemeral=True, edit_original_response=False,
                        embed=await embeds.simple(inter, lang, Locales.GuildPigAdmin.no_rights_title,
                                                  Locales.GuildPigAdmin.no_rights_desc,
                                                  prefix='warn', color=config.warn_color))
    return False


async def rename(inter):
    """Renames the pig from the panel. Asked for in a modal, since a name is free text and
    a select cannot carry one."""
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    if not await admin_only(inter, lang):
        return

    result = await modals.get_text(
        inter,
        translate(Locales.GuildPigAdmin.rename_modal_title, lang),
        translate(Locales.GuildPigAdmin.rename_modal_label, lang),
        default=await GuildPig.get_name(inter.guild.id),
        max_length=hryak.config.guild_pig_name_max_length)
    if not result:
        return
    modal_interaction, name = result

    response = await hryak.requests.guild_requests.rename_guild_pig(inter.guild.id, name)
    if response['status'] != hryak.Status.SUCCESS:
        await send_callback(modal_interaction, ephemeral=True, edit_original_response=False,
                            embed=await embeds.simple(inter, lang,
                                                      Locales.GuildPigAdmin.rename_bad_title,
                                                      Locales.GuildPigAdmin.rename_bad_desc,
                                                      prefix='warn', color=config.warn_color))
        return
    await send_callback(modal_interaction, ephemeral=True, edit_original_response=False,
                        embed=await embeds.simple(inter, lang, Locales.GuildPigAdmin.rename_scd_title,
                                                  Locales.GuildPigAdmin.rename_scd_desc,
                                                  {'pig': response['name']},
                                                  prefix='scd', color=config.success_color))
    await notify(inter.client, inter.guild.id, generate_embed(
        title=translate(Locales.GuildPigAdmin.notify_rename_title,
                        await Guild.get_language(inter.guild.id)),
        description=translate(Locales.GuildPigAdmin.notify_rename_desc,
                              await Guild.get_language(inter.guild.id),
                              {'user': inter.user.display_name, 'pig': response['name']}),
        prefix=Func.generate_prefix('✏️'),
        color=config.main_color,
        timestamp=False))
    await update_message(inter.client, inter.guild.id)


async def language(inter):
    """Sets the server's language from the panel.

    A language is a choice from a fixed list, so it is asked with a second select rather
    than a modal. The panel and the pig's message are both written in the server's language,
    so both are redrawn afterwards.
    """
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    if not await admin_only(inter, lang):
        return

    custom_id = f'in;guild_pig_language;{random.randrange(100000)}'
    await send_callback(inter, ephemeral=True, edit_original_response=False,
                        embed=await embeds.simple(inter, lang, Locales.GuildPigAdmin.language_title,
                                                  Locales.GuildPigAdmin.language_desc,
                                                  prefix='🌍'),
                        components=[components.choose_language(custom_id, lang)])
    try:
        chosen = await inter.client.wait_for(
            'interaction',
            check=lambda i: i.data.get('custom_id') == custom_id and i.user.id == inter.user.id,
            timeout=300)
    except asyncio.TimeoutError:
        return
    new_lang = chosen.data['values'][0]

    await Guild.set_language(inter.guild.id, new_lang)
    await send_callback(chosen, ephemeral=True, edit_original_response=True,
                        embed=generate_embed(
                            title=translate(Locales.SetServerLanguage.scd_title, new_lang),
                            description=translate(Locales.SetServerLanguage.scd_desc, new_lang),
                            prefix=Func.generate_prefix('scd'),
                            inter=inter))
    # both of hryak's own messages are written in the server's language
    await update_message(inter.client, inter.guild.id)
    await update_admin_message(inter.client, inter.guild.id)


async def withdraw(inter):
    """Moves money out of the pig and into the caller's own pocket.

    The panel lives in a channel only staff can see, but that is a permission the server can
    change, so the right to do this is checked here too rather than trusted to the walls.
    The amount is asked for in a modal, the same way donating does - a modal opened from a
    component is scoped to the message it came from, so an ephemeral is never edited onto
    the shared panel.
    """
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    currency = 'coins'
    if not await admin_only(inter, lang):
        return

    available = await Item.get_amount(currency, inventory=await GuildPig.get_inventory(inter.guild.id))
    if available < 1:
        await send_callback(inter, ephemeral=True, edit_original_response=False,
                            embed=await embeds.simple(inter, lang, Locales.GuildPigAdmin.empty_title,
                                                      Locales.GuildPigAdmin.empty_desc,
                                                      prefix='warn', color=config.warn_color))
        return

    result = await modals.get_item_amount(
        inter,
        translate(Locales.GuildPigAdmin.withdraw_modal_title, lang),
        translate(Locales.GuildPigAdmin.withdraw_modal_label, lang),
        max_amount=available)
    if not result:
        return
    modal_interaction, amount = result
    if amount < 1:
        return

    async def reply(embed, first: bool = False):
        await send_callback(modal_interaction, embed=embed, ephemeral=True,
                            edit_original_response=not first)

    confirmation = await DisUtils.confirm_message(
        modal_interaction, lang, ephemeral=True, edit_original_response=False,
        description=translate(Locales.GuildPigAdmin.withdraw_confirm_desc, lang,
                              {'money': amount, 'currency_emoji': await Item.get_emoji(currency),
                               'guild': inter.guild.name}))
    if not confirmation:
        await reply(await embeds.simple(inter, lang, Locales.GuildPigAdmin.withdraw_cancelled_title,
                                        Locales.GuildPigAdmin.withdraw_cancelled_desc, prefix='🏦'))
        return

    response = await hryak.requests.guild_requests.withdraw_server_money(
        inter.user.id, inter.guild.id, amount, currency)
    if response['status'] == hryak.Status.NO_MONEY:
        # somebody spent it while the modal was open
        await reply(error_callbacks.default_error_embed(
            inter,
            translate(Locales.ErrorCallbacks.not_enough_money_title, lang),
            translate(Locales.GuildPigAdmin.withdraw_gone_desc, lang,
                      {'available': response['available'],
                       'currency_emoji': await Item.get_emoji(currency)})))
        return
    await reply(await embeds.simple(inter, lang, Locales.GuildPigAdmin.withdraw_scd_title,
                                    Locales.GuildPigAdmin.withdraw_scd_desc,
                                    {'money': response['amount'],
                                     'currency_emoji': await Item.get_emoji(currency),
                                     'left': response['available']},
                                    prefix='scd', color=config.success_color))
    await money_moved(inter.client, inter.guild.id, inter.user, response['amount'], currency,
                      withdrawn=True)
    await update_message(inter.client, inter.guild.id)
    await update_admin_message(inter.client, inter.guild.id)


async def buy(inter, item_id, category: str = None, page: int = 1, bypass: bool = False):
    """Starting a purchase the whole server votes on, so it asks first.

    Everything here edits the ephemeral the shop already lives in, which is why the pig's
    own message is never touched.
    """
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    if not await Shop.is_item_in_shop(item_id, context='server'):
        await error_callbacks.item_is_not_in_shop(inter)
        return

    async def reply(title, description, options=None, prefix='🛍️', color=None):
        await send_callback(inter, ephemeral=True,
                            embed=await embeds.simple(inter, lang, title, description, options, prefix, color))

    # asked before anyone is warned about a vote: somebody who can buy outright is never
    # shown a poll they are not going to open
    response = await hryak.requests.guild_requests.propose_server_purchase(
        inter.user.id, inter.guild.id, item_id, bypass=bypass)
    status = response['status']
    if status == hryak.Status.IN_PROCESS:
        await reply(Locales.GuildPig.poll_in_process_title, Locales.GuildPig.poll_in_process_desc,
                    prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.NOT_A_CONTRIBUTOR:
        await reply(Locales.GuildPig.not_contributor_title, Locales.GuildPig.not_contributor_desc,
                    prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.NOT_READY:
        await reply(Locales.GuildPig.proposal_cooldown_title, Locales.GuildPig.proposal_cooldown_desc,
                    {'try_again': response['try_again']}, prefix='warn', color=config.warn_color)
        return
    if status != hryak.Status.SUCCESS:
        await error_callbacks.item_is_not_in_shop(inter)
        return

    item_name = await Item.get_name(item_id, lang)
    currency_emoji = await Item.get_emoji(response['currency'])
    if response['bypass']:  # manage server buys outright, no vote
        bought = await hryak.requests.guild_requests.buy_server_item(
            inter.guild.id, item_id, response['price'], response['currency'])
        if bought['status'] == hryak.Status.NO_MONEY:
            await error_callbacks.no_money(inter)
            return
        await reply(Locales.GuildPig.buy_bypassed_title, Locales.GuildPig.buy_bypassed_desc,
                    {'item': item_name, 'price': response['price'], 'currency_emoji': currency_emoji},
                    prefix='scd', color=config.success_color)
        await acted_alone(inter.client, inter.guild.id, inter.user, item_id, 'buy',
                          price=response['price'], currency=response['currency'])
        await update_message(inter.client, inter.guild.id)
        await update_admin_message(inter.client, inter.guild.id)
        return

    # from here on it really is going to a vote, so now it is worth asking
    confirmation = await DisUtils.confirm_message(
        inter, lang, ephemeral=True, edit_original_response=True,
        description=translate(Locales.GuildPig.buy_confirm_desc, lang,
                              {'item': item_name, 'price': response['price'],
                               'currency_emoji': currency_emoji,
                               'hours': hryak.config.guild_pig_poll_durations['shop'] // 3600}))
    if not confirmation:
        await send_callback(inter, embed=await embeds.buy_cancelled(inter, lang), ephemeral=True)
        return

    guild_lang = await Guild.get_language(inter.guild.id)
    posted = await post_poll(inter, 'shop', guild_lang,
                             # everyone reads this one, so it is in the server's language
                             # rather than in the language of whoever started it
                             translate(Locales.GuildPig.poll_question, guild_lang,
                                       {'item': await Item.get_name(item_id, guild_lang),
                                        'price': response['price'], 'currency': currency_emoji}),
                             {'item_id': item_id, 'price': response['price'],
                              'currency': response['currency']})
    if posted is None:
        await error_callbacks.item_is_not_in_shop(inter)
        return
    channel, opened = posted
    await reply(Locales.GuildPig.poll_started_title, Locales.GuildPig.poll_started_desc,
                {'item': item_name, 'channel': channel.mention, 'expires': opened['expires']},
                prefix='scd')


async def post_poll(inter, kind: str, guild_lang, question: str, data: dict):
    """Puts a vote to the server and records it, whatever it is about.

    Hands back (channel, opened) so the caller can say where it went, or None when the guild
    has no poll channel left to post in. Everything the resolver will need travels in data.
    """
    channel_id = await GuildPig.get_channel(inter.guild.id, key='poll_channel')
    channel = inter.client.get_channel(int(channel_id)) if channel_id is not None else None
    if channel is None:
        return None
    poll = discord.Poll(question=question,
                        # discord will not take less than an hour; when our own vote is
                        # shorter we simply end discord's poll early when it closes
                        duration=datetime.timedelta(
                            seconds=max(3600,
                                        hryak.config.guild_pig_poll_durations[kind])))
    poll.add_answer(text=translate(Locales.GuildPig.poll_yes, guild_lang), emoji='✅')
    poll.add_answer(text=translate(Locales.GuildPig.poll_no, guild_lang), emoji='❌')
    message = await channel.send(poll=poll)
    opened = await hryak.requests.guild_requests.open_server_poll(
        inter.user.id, inter.guild.id, kind, message.id, data)
    # the new vote is recorded by now, so sweeping cannot take it with it
    await clear_poll_channel(inter.client, inter.guild.id)
    return channel, opened


async def acted_alone(client, guild_id, user, item_id, action: str, price=None, currency=None):
    """Announces something staff did outright, without putting it to the server.

    A vote announces itself when it closes; this is the other route to the same result, and
    the server has just as much reason to hear about it.
    """
    lang = await Guild.get_language(guild_id)
    title, desc, emoji = {
        'buy': (Locales.GuildPig.notify_bought_title, Locales.GuildPig.notify_bought_desc, '🛍️'),
        'wear': (Locales.GuildPig.notify_dressed_title, Locales.GuildPig.notify_worn_desc, '👕'),
        'remove': (Locales.GuildPig.notify_dressed_title, Locales.GuildPig.notify_removed_desc, '👕'),
    }[action]
    return await notify(client, guild_id, generate_embed(
        title=translate(title, lang),
        description=translate(desc, lang,
                              {'user': user.display_name,
                               'item': await Item.get_name(item_id, lang),
                               'price': price,
                               'currency_emoji': await Item.get_emoji(currency) if currency else ''}),
        prefix=Func.generate_prefix(emoji),
        color=config.success_color,
        timestamp=False))


async def shop(inter, pre_command_check: bool = True, ephemeral: bool = False,
               edit_original_response: bool = None, init_category: str = None, init_page: int = 1):
    """The servers' shop, drawn by the same builder as the personal one.

    Only two things differ: the stock comes from the server snapshot, and the balance in
    the footer is the server's rather than the buyer's.
    """
    if pre_command_check:
        await DisUtils.pre_command_check(inter, ephemeral=ephemeral)
    else:
        await User.register_user_if_not_exists(inter.user.id)
    if edit_original_response is None:
        edit_original_response = not ephemeral
    lang = await User.get_language(inter.user.id)
    data = await Shop.get_data(context='server') or {}
    pages = {'weekly_shop': (Locales.GuildPig.shop_weekly, Locales.GuildPig.shop_weekly_desc),
             # 'permanent_shop': (Locales.GuildPig.shop_permanent, Locales.GuildPig.shop_permanent_desc)
             }
    # labels are what the user sees; the raw keys are what travels in custom_ids
    category_labels = {page: translate(title, lang) for page, (title, _) in pages.items()}
    items_by_cats = {category_labels[page]: data.get(page) or [] for page in pages}
    category_keys = {category_labels[page]: page for page in pages}
    inventory = await GuildPig.get_inventory(inter.guild.id)
    shop_embeds = await Embeds.generate_items_list_embeds(
        inter, items_by_cats, lang, sort=False,
        list_type='shop',
        prefix_emoji='\U0001f6cd\ufe0f',
        description={category_labels[page]: translate(desc, lang) for page, (_, desc) in pages.items()},
        empty_desc=translate(Locales.GuildPig.shop_empty, lang),
        select_item_component_id='item_select;server_shop',
        cat_as_title=True,
        category_keys=category_keys,
        footer_override=f"{translate(Locales.Global.balance, lang)}: "
                        f"{await Item.get_amount('coins', inventory=inventory)} "
                        f"{await Item.get_emoji('coins')}")
    await DisUtils.pagination(inter, lang, embeds=shop_embeds,
                              arrows=False, categories=True,
                              ephemeral=ephemeral, edit_original_response=edit_original_response,
                              init_category=init_category, init_page=init_page)


async def inventory(inter, pre_command_check: bool = True, ephemeral: bool = False,
                    edit_original_response: bool = None, init_category: str = None, init_page: int = 1):
    """Everything the pig owns, drawn by the same builder as a person's own things.

    The two lists the personal game splits across /wardrobe and /inventory are categories of
    one list here - the pig has few enough things that a second entry point would be empty
    most of the time. They are built apart because each is rendered its own way.
    """
    if pre_command_check:
        await DisUtils.pre_command_check(inter, ephemeral=ephemeral)
    else:
        await User.register_user_if_not_exists(inter.user.id)
    if edit_original_response is None:
        edit_original_response = not ephemeral
    lang = await User.get_language(inter.user.id)
    pig_inventory = await GuildPig.get_inventory(inter.guild.id)
    pages = {'wardrobe': (Locales.GuildPig.inventory_wardrobe, Locales.GuildPig.inventory_wardrobe_desc),
             'inventory': (Locales.GuildPig.inventory_things, Locales.GuildPig.inventory_things_desc)}
    # labels are what the user sees; the raw keys are what travels in custom_ids
    category_labels = {page: translate(title, lang) for page, (title, _) in pages.items()}
    inventory_embeds = {}
    for page, (_, desc) in pages.items():
        items = await Tech.get_all_items((('inventory_type', page),), inventory=pig_inventory)
        inventory_embeds.update(await Embeds.generate_items_list_embeds(
            inter, {category_labels[page]: items}, lang,
            list_type=page,
            inventory=pig_inventory,
            prefix_emoji='🎒',
            description=translate(desc, lang),
            empty_desc=translate(Locales.GuildPig.inventory_empty, lang),
            select_item_component_id='item_select;server_inventory',
            cat_as_title=True,
            category_keys={category_labels[page]: page}))
    await DisUtils.pagination(inter, lang, embeds=inventory_embeds,
                              arrows=False, categories=True,
                              ephemeral=ephemeral, edit_original_response=edit_original_response,
                              init_category=category_labels.get(init_category, init_category),
                              init_page=init_page)


async def inventory_item_selected(inter, item_id, category: str = None, page: int = 1):
    """The pig's own item menu - the same shape as a person's, with the buttons that act on
    it put to a vote instead of taking effect."""
    lang = await User.get_language(inter.user.id)
    pig_inventory = await GuildPig.get_inventory(inter.guild.id)
    if await Item.get_amount(item_id, inventory=pig_inventory) < 1:
        # the list was drawn before a vote took it away
        await error_callbacks.not_enough_items(inter, item_id)
        return
    await send_callback(inter,
                        embed=await Embeds.item_selected_embed(
                            inter, lang, item_id=item_id,
                            _type='wardrobe' if await Item.get_type(item_id) == 'skin' else 'inventory',
                            inventory=pig_inventory, context='server'),
                        components=await components.inventory_item_selected(
                            inter.guild.id, item_id, lang, category=category, page=page))


async def wear(inter, item_id, category: str = None, page: int = 1, remove: bool = False,
               bypass: bool = False):
    """Dressing the pig is put to the server the same way buying for it is - taking a skin
    off included, since it is just as much everyone's pig."""
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    item_name = await Item.get_name(item_id, lang)

    async def reply(title, description, options=None, prefix='👕', color=None):
        await send_callback(inter, ephemeral=True,
                            embed=await embeds.simple(inter, lang, title, description, options, prefix, color))

    # asked before anyone is warned about a vote: somebody who can dress the pig outright is
    # never shown a poll they are not going to open
    response = await hryak.requests.guild_requests.propose_server_wear(
        inter.user.id, inter.guild.id, item_id, remove=remove, bypass=bypass)
    status = response['status']
    if status == hryak.Status.IN_PROCESS:
        await reply(Locales.GuildPig.wear_poll_in_process_title, Locales.GuildPig.wear_poll_in_process_desc,
                    prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.NOT_A_CONTRIBUTOR:
        await reply(Locales.GuildPig.not_contributor_title, Locales.GuildPig.not_contributor_desc,
                    prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.NOT_READY:
        await reply(Locales.GuildPig.proposal_cooldown_title, Locales.GuildPig.proposal_cooldown_desc,
                    {'try_again': response['try_again']}, prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.NOT_COMPATIBLE_SKINS:
        await reply(Locales.GuildPig.wear_not_compatible_title, Locales.GuildPig.wear_not_compatible_desc,
                    {'item': item_name,
                     'skins': ', '.join([f'**{await Item.get_name(skin, lang)}**'
                                         for skin in response['skins']])},
                    prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.ALREADY_USED:
        await reply(Locales.GuildPig.wear_already_title, Locales.GuildPig.wear_already_desc,
                    {'item': item_name}, prefix='warn', color=config.warn_color)
        return
    if status == hryak.Status.NOT_ENOUGH_ITEMS:
        await error_callbacks.not_enough_items(inter, item_id)
        return
    if status != hryak.Status.SUCCESS:
        await error_callbacks.item_is_not_in_shop(inter)
        return

    if response['bypass']:  # manage server dresses the pig outright, no vote
        await hryak.requests.guild_requests.wear_server_skin(inter.guild.id, item_id, remove=remove)
        await reply(Locales.GuildPig.wear_bypassed_title,
                    Locales.GuildPig.remove_bypassed_desc if remove else Locales.GuildPig.wear_bypassed_desc,
                    {'item': item_name}, prefix='scd', color=config.success_color)
        await acted_alone(inter.client, inter.guild.id, inter.user, item_id,
                          'remove' if remove else 'wear')
        await update_message(inter.client, inter.guild.id)
        return

    # from here on it really is going to a vote, so now it is worth asking
    confirmation = await DisUtils.confirm_message(
        inter, lang, ephemeral=True, edit_original_response=True,
        description=translate(Locales.GuildPig.remove_confirm_desc if remove
                              else Locales.GuildPig.wear_confirm_desc, lang,
                              {'item': item_name,
                               'hours': hryak.config.guild_pig_poll_durations['wear'] // 3600}))
    if not confirmation:
        await reply(Locales.GuildPig.wear_cancelled_title, Locales.GuildPig.wear_cancelled_desc)
        return

    guild_lang = await Guild.get_language(inter.guild.id)
    posted = await post_poll(inter, 'wear', guild_lang,
                             translate(Locales.GuildPig.remove_question if remove
                                       else Locales.GuildPig.wear_question, guild_lang,
                                       {'item': await Item.get_name(item_id, guild_lang)}),
                             {'item_id': item_id, 'remove': remove})
    if posted is None:
        await error_callbacks.item_is_not_in_shop(inter)
        return
    channel, opened = posted
    await reply(Locales.GuildPig.poll_started_title, Locales.GuildPig.poll_started_desc,
                {'item': item_name, 'channel': channel.mention, 'expires': opened['expires']},
                prefix='scd')


async def top(inter, pre_command_check: bool = True, ephemeral: bool = False):
    """From the command it replies normally; from the pig's menu it answers ephemerally,
    so the shared message is left alone."""
    if pre_command_check:
        await DisUtils.pre_command_check(inter)
    else:
        await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    boards = (
        ('weight', Locales.GuildPig.top_title, Locales.GuildPig.top_desc, '🐖',
         await hryak.requests.top_requests.top_weight_guilds(inter.guild.id, lang)),
        ('money', Locales.GuildPig.top_money_title, Locales.GuildPig.top_money_desc, '🪙',
         await hryak.requests.top_requests.top_money_guilds(inter.guild.id, lang)),
    )
    await DisUtils.pagination(
        inter, lang,
        embeds={translate(title, lang): {
            'embed': await embeds.top(inter, lang, response, title, desc, emoji)}
            for _, title, desc, emoji, response in boards},
        arrows=False, categories=True,
        ephemeral=ephemeral, edit_original_response=not ephemeral)


# discord posts a "poll has closed" system message of its own once a poll ends. it is
# type 46, which discord.py 2.4 does not know about yet, so it is matched by raw value
POLL_RESULT_MESSAGE_TYPE = 46


async def remove_poll_result_message(channel, poll_message_id, attempts: int = 3, delay: float = 1):
    """Clears discord's own "the poll has closed" note, since we post our own outcome.

    It only shows up once discord processes the end of the poll, which is not instant, so
    this looks a few times before giving up.
    """
    for _ in range(attempts):
        await asyncio.sleep(delay)
        try:
            async for message in channel.history(limit=10):
                if message.type.value != POLL_RESULT_MESSAGE_TYPE:
                    continue
                reference = message.reference
                if reference is not None and reference.message_id != poll_message_id:
                    continue
                await message.delete()
                return True
        except discord.errors.HTTPException:
            return False
    return False


async def finalise_polls(client, delay: float = .5):
    """Closes every vote whose time is up.

    Discord counts the votes for us, so this only reads them back, applies the quorum and
    acts. A guild whose poll message or channel has gone is cleared rather than retried
    forever.
    """
    closed = 0
    for guild_id in await GuildPig.get_all_guilds_with_polls():
        lang = await Guild.get_language(guild_id)
        # each kind has its own slot, so a server may be voting on a purchase and on what
        # the pig wears at the same time without one holding the other up
        for kind in hryak.config.guild_pig_poll_durations:
            poll = await GuildPig.get_poll(guild_id, kind)
            if poll is None or poll['expires'] > hryak.Func.generate_current_timestamp():
                continue
            channel = client.get_channel(int(await GuildPig.get_channel(guild_id, key='poll_channel') or 0))
            yes = no = 0
            message = None
            if channel is not None:
                try:
                    message = await channel.fetch_message(int(poll['message_id']))
                except discord.errors.HTTPException:
                    message = None
            if message is not None and message.poll is not None:
                counts = [answer.vote_count for answer in message.poll.answers]
                yes, no = (counts + [0, 0])[:2]

            response = await hryak.requests.guild_requests.resolve_server_poll(guild_id, kind, yes, no)
            if response['status'] == hryak.Status.NOT_EXIST:
                continue
            # how it went is an announcement, not a vote, so it goes where announcements go
            await notify(client, guild_id, await embeds.poll_outcome(
                lang, response,
                await Item.get_name(poll['item_id'], lang),
                # only a purchase has a price to report
                await Item.get_emoji(poll['currency']) if poll.get('currency') else None))
            if message is not None and message.poll is not None and not message.poll.is_finalised():
                try:  # ours is over, so stop discord showing it as still running
                    await message.poll.end()
                except discord.errors.HTTPException:
                    pass
                await remove_poll_result_message(channel, message.id)
            if response['status'] == hryak.Status.SUCCESS:
                await update_message(client, guild_id)
            await clear_poll_channel(client, guild_id)
            closed += 1
            await asyncio.sleep(delay)
    return closed


async def pay_weekly_rewards(client, delay: float = .5):
    """Lets every pig that has been fed poop, once a week.

    Only guilds with feeds on the books are walked, and each decides for itself whether its
    week has turned, so this is safe to call as often as the loop likes. A guild whose
    payout is announced nowhere is still paid - the notification is the last step, never a
    condition of it.
    """
    paid = 0
    for guild_id in await GuildPig.get_all_setup_guild_ids_for_payout():
        response = await hryak.requests.guild_requests.pay_weekly_rewards_if_needed(guild_id)
        if response is None:
            continue
        if response['status'] == hryak.Status.SUCCESS and response['total_poop'] > 0:
            await notify(client, guild_id, await embeds.weekly_rewards(
                guild_id, await Guild.get_language(guild_id), response))
            paid += 1
        # the pig's message is not redrawn here on purpose. a payout moves poop into
        # people's inventories and changes nothing the message shows - not the weight, the
        # balance or the last feed - so redrawing would only reupload the picture and mark
        # the message edited, once per guild per cycle, for nothing
        await asyncio.sleep(delay)
    return paid


async def clear_poll_channel(client, guild_id, limit: int = 200):
    """Leaves the poll channel holding nothing but the votes still running.

    Everything else that used to land there - outcomes, discord's own poll-closed notes,
    anything a member managed to post - is swept out, so the channel reads as a list of what
    the server is deciding right now and nothing else. Only hryak posts there, so there is
    never much to remove; limit is a guard for the first sweep after a backlog.
    """
    channel_id = await GuildPig.get_channel(guild_id, key='poll_channel')
    if channel_id is None:
        return 0
    channel = client.get_channel(int(channel_id))
    if channel is None:
        return 0
    keep = set()
    for kind in hryak.config.guild_pig_poll_durations:
        poll = await GuildPig.get_poll(guild_id, kind)
        if poll is not None and poll.get('message_id'):
            keep.add(int(poll['message_id']))
    try:
        # purge bulk-deletes what it can and falls back to one-by-one past discord's
        # two-week cutoff, so an old channel still empties
        removed = await channel.purge(limit=limit, check=lambda m: m.id not in keep)
    except discord.errors.HTTPException:
        return 0
    return len(removed)


async def pig_message_payload(guild_id, lang):
    """The pig's message as (embed, file).

    The pig is drawn on the fly, so its picture is a file on disk rather than a url and has
    to travel with the message as an attachment. send_callback does this for everything that
    goes through it; the pig's message is posted and edited directly, so it does it here.
    """
    embed = await embeds.pig_message(guild_id, lang)
    path = embed.image.url
    if path and not path.startswith(('http://', 'https://', 'attachment://')):
        name = os.path.basename(path)
        embed.set_image(url=f'attachment://{name}')
        return embed, discord.File(path, filename=name)
    return embed, None


async def update_message(client, guild_id):
    """Redraws the pig's message in place. Returns False if there is nothing to redraw."""
    lang = await Guild.get_language(guild_id)
    channel_id = await GuildPig.get_channel(guild_id)
    message_id = await GuildPig.get_message(guild_id)
    if channel_id is None or message_id is None:
        return False
    channel = client.get_channel(int(channel_id))
    if channel is None:
        return False
    try:
        message = await channel.fetch_message(int(message_id))
        embed, file = await pig_message_payload(guild_id, lang)
        # the old picture has to be named in attachments or discord keeps it alongside the
        # new one, and the embed would then point at a file that is no longer the first
        await message.edit(embed=embed, view=components.pig_message(lang),
                           attachments=[file] if file is not None else [])
    except discord.errors.HTTPException:
        return False
    return True


async def update_admin_message(client, guild_id):
    """Redraws the admin panel in place. Returns False if there is nothing to redraw -
    a guild set up before the panel existed simply has none yet."""
    lang = await Guild.get_language(guild_id)
    channel_id = await GuildPig.get_channel(guild_id, key='admin_channel')
    message_id = await GuildPig.get_message(guild_id, key='admin_message')
    if channel_id is None or message_id is None:
        return False
    channel = client.get_channel(int(channel_id))
    if channel is None:
        return False
    try:
        message = await channel.fetch_message(int(message_id))
        await message.edit(embed=await embeds.admin_message(guild_id, lang),
                           view=components.admin_message(lang))
    except discord.errors.HTTPException:
        return False
    return True


async def update_all_messages(client, delay: float = .5):
    """Redraws every server pig's message, so a guild is never left showing stale numbers.

    Only guilds that actually set a pig up are walked, and there is a pause between them -
    edits share the same rate limiter as everything else the bot sends.
    """
    updated = 0
    for guild_id in await GuildPig.get_all_setup_guilds():
        if await update_message(client, guild_id):
            updated += 1
        await update_admin_message(client, guild_id)
        await asyncio.sleep(delay)
    return updated


async def prepare_channel(inter, channel, name, category=None):
    """Hands back (channel, created_by_bot). Sending is locked for everyone except hryak,
    which still needs to post and to open polls in there. A channel hryak makes itself goes
    into its own category; one the owner picked is left where they put it."""
    created_by_bot = False
    if channel is None:
        channel = await inter.guild.create_text_channel(name=name, category=category)
        created_by_bot = True
    await channel.set_permissions(inter.guild.default_role, send_messages=False)
    # denying @everyone takes hryak's own right to post with it, unless a role says
    # otherwise - so give the channel back to hryak explicitly. manage_messages is what
    # lets the poll channel be swept back down to just the votes still running: a bulk
    # delete needs it even for hryak's own messages
    await channel.set_permissions(inter.guild.me, view_channel=True, send_messages=True,
                                  embed_links=True, send_polls=True,
                                  manage_messages=True, read_message_history=True)
    return channel, created_by_bot


async def prepare_admin_channel(inter, channel, name, category=None):
    """Hands back (channel, created_by_bot) for the staff-only channel the panel lives in.

    Shuts everyone out and lets back in anyone who could have run the setup command in the
    first place - that is what makes it an admin channel rather than merely a hidden one.
    On a channel hryak makes itself the permissions go in at creation, so it is never
    briefly readable and it costs one api call instead of one per role; on a channel the
    owner picked they are applied after, since the channel already exists.
    """
    overwrites = {
        inter.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        inter.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                    embed_links=True),
    }
    for role in inter.guild.roles:
        if role.permissions.administrator or role.permissions.manage_guild:
            # staff read the panel and press its buttons, but the channel stays hryak's
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=False)
    if channel is None:
        return await inter.guild.create_text_channel(name=name, category=category,
                                                     overwrites=overwrites), True
    for target, overwrite in overwrites.items():
        await channel.set_permissions(target, overwrite=overwrite)
    return channel, False


async def remove_old_category(inter, new_category):
    """Drops the category hryak made last time, once nothing is left in it."""
    old_category_id = await GuildPig.get_channel(inter.guild.id, key='category')
    if old_category_id is None:
        return
    old_category = inter.guild.get_channel(int(old_category_id))
    if old_category is None or (new_category is not None and old_category.id == new_category.id):
        return
    if old_category.channels:  # somebody put their own channels in there
        return
    if await GuildPig.is_channel_created_by_bot(inter.guild.id, key='category'):
        try:
            await old_category.delete()
        except discord.errors.HTTPException:
            pass


async def remove_old_home(inter, new_channel, key: str = 'channel', delete_message: bool = True,
                          message_key: str = 'message'):
    """Clears out wherever the pig used to live.

    The old message always goes, even when staying in the same channel, so a server never
    ends up with two pig messages. The channel itself only goes if hryak made it - a
    channel the owner picked is theirs, not ours to delete.
    """
    old_channel_id = await GuildPig.get_channel(inter.guild.id, key=key)
    if old_channel_id is None:
        return
    old_channel = inter.guild.get_channel(int(old_channel_id))
    if old_channel is None:
        return

    old_message_id = await GuildPig.get_message(inter.guild.id, key=message_key)
    if delete_message and old_message_id is not None:
        try:
            message = await old_channel.fetch_message(int(old_message_id))
            await message.delete()
        except discord.errors.HTTPException:
            pass

    if old_channel.id != new_channel.id and await GuildPig.is_channel_created_by_bot(inter.guild.id, key=key):
        try:
            await old_channel.delete()
        except discord.errors.HTTPException:
            pass


async def setup(inter, channel: discord.TextChannel = None, poll_channel: discord.TextChannel = None,
                notification_channel: discord.TextChannel = None,
                admin_channel: discord.TextChannel = None):
    await DisUtils.pre_command_check(inter, language_check=False)
    lang = await User.get_language(inter.user.id)
    await Guild.register_guild_if_not_exists(inter.guild.id, Func.guess_guild_language(inter.guild, inter.user))

    # a category is only worth making when hryak has channels of its own to put in it, and
    # the right to make channels only matters when something still has to be made
    homes = (channel, poll_channel, notification_channel, admin_channel)
    making_channels = any(home is None for home in homes)
    if making_channels and not inter.guild.me.guild_permissions.manage_channels:
        await send_callback(inter, embed=await embeds.no_permissions(inter, lang))
        return

    created_channels = []
    category = None
    try:
        if making_channels:
            category = await inter.guild.create_category(name='🐷・HRYAK')
            created_channels.append(category)
        channel, created = await prepare_channel(inter, channel, '🐷・hryak', category)
        if created:
            created_channels.append(channel)
        poll_channel, created = await prepare_channel(inter, poll_channel, '🗳️・hryak-polls', category)
        if created:
            created_channels.append(poll_channel)
        notification_channel, created = await prepare_channel(inter, notification_channel,
                                                              '🔔・hryak-notifications', category)
        if created:
            created_channels.append(notification_channel)
        admin_channel, created = await prepare_admin_channel(inter, admin_channel,
                                                             '🛠️・hryak-admin', category)
        if created:
            created_channels.append(admin_channel)
        guild_lang = await Guild.get_language(inter.guild.id)
        pig_embed, pig_file = await pig_message_payload(inter.guild.id, guild_lang)
        message = await channel.send(embed=pig_embed, file=pig_file,
                                     view=components.pig_message(guild_lang))
        admin_message = await admin_channel.send(embed=await embeds.admin_message(inter.guild.id, guild_lang),
                                                 view=components.admin_message(guild_lang))
    except (discord.errors.Forbidden, discord.errors.HTTPException):
        for created_channel in created_channels:
            try:
                await created_channel.delete()
            except discord.errors.HTTPException:
                pass
        await send_callback(inter, embed=await embeds.no_permissions(inter, lang, channel))
        return

    # only once every home works, so a failed move never costs the server the old ones
    await remove_old_home(inter, channel)
    await remove_old_home(inter, poll_channel, key='poll_channel', delete_message=False)
    await remove_old_home(inter, notification_channel, key='notification_channel', delete_message=False)
    await remove_old_home(inter, admin_channel, key='admin_channel', message_key='admin_message')
    await remove_old_category(inter, category)
    await GuildPig.set_channel(inter.guild.id, channel.id, created_by_bot=channel in created_channels)
    await GuildPig.set_channel(inter.guild.id, poll_channel.id, created_by_bot=poll_channel in created_channels,
                               key='poll_channel')
    await GuildPig.set_channel(inter.guild.id, notification_channel.id,
                               created_by_bot=notification_channel in created_channels,
                               key='notification_channel')
    await GuildPig.set_channel(inter.guild.id, admin_channel.id,
                               created_by_bot=admin_channel in created_channels, key='admin_channel')
    await GuildPig.set_channel(inter.guild.id, category.id if category is not None else None,
                               created_by_bot=category is not None, key='category')
    await GuildPig.set_message(inter.guild.id, message.id)
    await GuildPig.set_message(inter.guild.id, admin_message.id, key='admin_message')
    await send_callback(inter, embed=await embeds.setup(inter, lang, channel, poll_channel,
                                                        notification_channel, admin_channel))
