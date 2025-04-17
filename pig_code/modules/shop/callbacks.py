import discord.ui

from ...utils import *
from . import components
from ...utils.discord_utils import send_callback, generate_embed
from ...core import *


async def shop(inter, message=None, init_category: str = None, init_page: int = 1):
    await DisUtils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    shops = {'consumables_shop': Shop.get_consumables_shop,
             'tools_shop': Shop.get_tools_shop,
             'daily_shop': Shop.get_daily_shop,
             'case_shop': Shop.get_case_shop,
             'premium_skins_shop': Shop.get_premium_skins_shop,
             'coins_shop': Shop.get_coins_shop,
             # 'donation_shop': None
             }
    if init_category is None:
        description = f'{translate(Locales.Shop.main_page_desc, lang)}\n\n'
        for shop_ in shops:
            description += f'{'\n' if shop_ == 'premium_skins_shop' else ''}> {Func.generate_prefix(config.shops_emojis[shop_])}{translate(Locales.Shop.titles[shop_], lang)}\n'
        await send_callback(inter, embed=generate_embed(translate(Locales.Shop.main_page_title, lang),
                                                        description,
                                                        prefix=Func.generate_prefix('🛍️'),
                                                        thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                            config.image_links['shop']),
                                                        footer_url=Func.generate_footer_url(user=inter.user),
                                                        footer=Func.generate_footer(inter)),
                            components=[discord.ui.Select(custom_id='move_to;shop',
                                                          placeholder=translate(Locales.Global.choose_category, lang),
                                                          options=[discord.SelectOption(
                                                              label=translate(Locales.Shop.titles[shop_], lang),
                                                              value=translate(Locales.Shop.titles[shop_], lang),
                                                              emoji=config.shops_emojis[shop_]) for shop_ in
                                                              shops])])
        return
    items_by_cats = {}
    for shop_ in shops:
        if shops[shop_] is None:
            continue
        items_by_cats[f'{translate(Locales.Shop.titles[shop_], lang)}'] = shops[shop_]()
    embeds = await Embeds.generate_items_list_embeds(inter, items_by_cats, lang, sort=False,
                                                    list_type='shop',
                                                    prefix_emoji='🛍️',
                                                    select_item_component_id='item_select;shop',
                                                    cat_as_title=True)
    # embeds[translate(Locales.Shop.titles['donation_shop'], lang)] = {
    #         'embeds': [{'embed': generate_embed(translate(Locales.Shop.donation_shop_title, lang),
    #                                             translate(Locales.Shop.donation_shop_desc, lang),
    #                                             prefix=Func.generate_prefix('🍩'),
    #                                             footer_url=Func.generate_footer_url(user=inter.user),
    #                                             color=config.premium_color,
    #                                             footer=Func.generate_footer(inter)),
    #                     'components': []}]}
    # if lang in ['ru']:
    #     embeds[translate(Locale.Shop.titles['donation_shop'], lang)] = {
    #         'embeds': [{'embed': generate_embed(translate(Locale.PremiumShop.main_page_title, lang),
    #                                             translate(Locale.PremiumShop.main_page_desc, lang),
    #                                             prefix=Func.generate_prefix('🍩'),
    #                                             footer_url=Func.generate_footer_url(user=inter.user),
    #                                             color=config.premium_color,
    #                                             footer=Func.generate_footer(inter)),
    #                     'components': [discord.ui.Select(
    #                         custom_id='donate',
    #                         placeholder=translate(Locale.PremiumShop.main_page_select_placeholder, lang),
    #                         options=[discord.SelectOption(
    #                             label=translate(Locale.PremiumShop.main_page_select_option_hollars, lang),
    #                             emoji='💵',
    #                             value='hollars'),
    #                             discord.SelectOption(
    #                                 label=translate(Locale.PremiumShop.main_page_select_option_coins, lang),
    #                                 emoji='🪙',
    #                                 value='coins')])]}]}
    # elif lang in ['en']:
    #     embeds[translate(Locale.Shop.titles['donation_shop'], lang)] = {
    #         'embeds': [{'embed': generate_embed(translate(Locale.Shop.donation_shop_title, lang),
    #                                             translate(Locale.Shop.donation_shop_desc, lang),
    #                                             prefix=Func.generate_prefix('🍩'),
    #                                             footer_url=Func.generate_footer_url(user=inter.user),
    #                                             color=config.premium_color,
    #                                             footer=Func.generate_footer(inter)),
    #                     'components': []}]}
    await DisUtils.pagination(inter, lang, message=message,
                           embeds=embeds,
                           return_if_starts_with=['back_to_inventory', 'wardrobe_category_choose'],
                           embed_thumbnail_url=await hryak.Func.get_image_path_from_link(
                               config.image_links['shop']), arrows=False, categories=True,
                           init_category=init_category, init_page=init_page)


async def shop_item_buy(inter, item_id):
    lang = User.get_language(inter.user.id)
    if not Shop.is_item_in_shop(item_id):
        await error_callbacks.item_is_not_in_shop(inter)
        return
    if Shop.is_item_in_cooldown(inter.user.id, item_id):
        await error_callbacks.default_error_callback(inter,
                                                     translate(Locales.ErrorCallbacks.shop_buy_cooldown_title, lang),
                                                     translate(Locales.ErrorCallbacks.shop_buy_cooldown_desc, lang,
                                                               {'item': Item.get_name(item_id, lang),
                                                                'timestamp': Shop.get_timestamp_of_cooldown_pass(
                                                                    inter.user.id, item_id)}),
                                                     edit_original_response=False, ephemeral=True, )
        return
    if Item.get_amount(Item.get_market_price_currency(item_id), inter.user.id) < Item.get_market_price(item_id):
        await error_callbacks.not_enough_money(inter)
        return
    User.remove_item(inter.user.id, Item.get_market_price_currency(item_id), Item.get_market_price(item_id))
    User.add_item(inter.user.id, Item.clean_id(item_id), Item.get_amount(item_id))
    History.append_shop_history(inter.user.id, Item.clean_id(item_id), amount=Item.get_amount(item_id))
    await send_callback(inter, edit_original_response=False, ephemeral=True,
                        embed=generate_embed(
                            title=translate(Locales.ShopItemBought.title, lang,
                                            {'item': Item.get_name(item_id,
                                                                   lang).lower()}) + f' x{Item.get_amount(item_id)}',
                            description=translate(Locales.ShopItemBought.desc, lang),
                            prefix=Func.generate_prefix('scd'),
                            inter=inter,
                        ))


async def shop_item_selected(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.user.id)
    if not Shop.is_item_in_shop(item_id):
        await error_callbacks.item_is_not_in_shop(inter)
        return
    await send_callback(inter if message is None else message,
                        embed=await Embeds.item_selected_embed(inter, lang, item_id=item_id, _type='shop'),
                        components=components.shop_item_selected(item_id, lang, category=category, page=page))


async def donation_page_selected(inter, category):
    lang = User.get_language(inter.user.id)
    currency = 'RUB'
    if lang in ['en']:
        currency = 'USD'
    if category == 'hollars':
        m = await send_callback(inter,
                                embed=generate_embed(translate(Locales.PremiumShop.buy_hollars_page_title, lang),
                                                     translate(Locales.PremiumShop.buy_hollars_page_desc, lang,
                                                               {'amount':
                                                                    config.amount_of_hollars_per_unit_of_real_currency[
                                                                        hryak.config.language_currencies[lang]]}),
                                                     prefix=Func.generate_prefix('💵'),
                                                     footer_url=Func.generate_footer_url(user=inter.user),
                                                     footer=Func.generate_footer(inter),
                                                     color=config.premium_color,
                                                     thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                         config.image_links['shop'])),
                                components=[
                                    discord.ui.Button(
                                        label=translate(Locales.PremiumShop.buy_hollars_button_label, lang),
                                        custom_id='in;donate;hollars',
                                        style=discord.ButtonStyle.green),
                                    discord.ui.Button(
                                        style=discord.ButtonStyle.grey,
                                        label='↩️',
                                        custom_id=f'back_to_inventory;shop;{translate(Locales.Shop.titles["donation_shop"], lang)};1',
                                    )
                                ])
        interaction = await inter.client.wait_for(
            "interaction",
            check=lambda i: i.data.get(
                'custom_id') == "in;donate;hollars" and i.user.id == inter.user.id and i.message.id == m.id,
            timeout=300,
        )
        modal_interaction, amount = await modals.get_amount_of_hollars_to_donate(interaction, delete_response=True)
        if amount is False:
            return
        price = round(amount / config.amount_of_hollars_per_unit_of_real_currency[currency], 2)
        await choose_payment_method(inter, category, amount, price, currency)
    if category == 'coins':
        options = []
        for k, v in hryak.config.donate_coins_prices[lang].items():
            options.append(discord.SelectOption(
                label=translate(Locales.PremiumShop.select_coins_option_label, lang, {'amount': k}),
                description=translate(Locales.PremiumShop.select_coins_option_desc, lang, {'price': v,
                                                                                           'currency':
                                                                                               config.currency_symbols[
                                                                                                   currency]}),
                emoji='🪙',
                value=f'{k}'))
        m = await send_callback(inter,
                                embed=generate_embed(translate(Locales.PremiumShop.buy_coins_page_title, lang),
                                                     translate(Locales.PremiumShop.buy_coins_page_desc, lang),
                                                     prefix=Func.generate_prefix('🪙'),
                                                     footer_url=Func.generate_footer_url(user=inter.user),
                                                     footer=Func.generate_footer(inter),
                                                     color=config.premium_color,
                                                     thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                         config.image_links['shop']),
                                                     image_url=config.image_links[
                                                         'coins_ru_ruble_prices'] if currency == 'RUB' else None),
                                components=[discord.ui.Select(
                                    placeholder=translate(Locales.PremiumShop.select_coins_placeholder, lang),
                                    custom_id='in;donate;coins', options=options)])
        interaction = await inter.client.wait_for(
            "interaction",
            check=lambda i: i.data.get(
                'custom_id') == "in;donate;coins" and i.user.id == inter.user.id and i.message.id == m.id,
            timeout=300,
        )
        amount = int(interaction.data['values'][0])
        await interaction.response.defer()
        await choose_payment_method(inter, category, amount, hryak.config.donate_coins_prices[lang][amount], currency)


async def choose_payment_method(inter, category, amount, price, currency):
    lang = User.get_language(inter.user.id)
    options = []
    for i in config.payment_methods_for_languages[lang]:
        if i == 'donatello':
            options.append(discord.SelectOption(label='Donatello', value='donatello'))
    items = {}
    if category == 'hollars':
        items = {'hollars': amount}
    elif category == 'coins':
        items = {'coins': amount}
    description = f'{translate(Locales.PremiumShop.select_payment_method_desc, lang)}\n\n'
    for i in config.payment_methods_for_languages[lang]:
        description += f'**{i.capitalize()}**\n' \
                       f'{translate(Locales.PremiumShop.payment_methods_descs[i], lang)}\n'
    m = await send_callback(inter,
                            embed=generate_embed(translate(Locales.PremiumShop.select_payment_method_title, lang),
                                                 description,
                                                 prefix=Func.generate_prefix('🍩'),
                                                 footer_url=Func.generate_footer_url(user=inter.user),
                                                 footer=Func.generate_footer(inter),
                                                 color=config.premium_color,
                                                 thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                     config.image_links['shop'])
                                                 ),
                            components=[discord.ui.Select(custom_id='in;payment_method', options=options)])
    interaction = await inter.client.wait_for(
        "interaction",
        check=lambda i: i.data.get(
            'custom_id') == "in;payment_method" and i.user.id == inter.user.id and i.message.id == m.id,
        timeout=300,
    )
    order_id = await Order.generate_order_id(interaction.data['values'][0])
    if interaction.data['values'][0] == 'donatello':
        await Order.create(inter.user.id, order_id, items, price, currency, platform='donatello')
        price /= config.currency_to_usd[currency]
        currency = 'UAH'
        price *= config.currency_to_usd[currency]
        price = round(price, 2)
        await send_callback(interaction, embed=generate_embed(
            translate(Locales.PremiumShop.donatello_pay_title, lang),
            description=translate(Locales.PremiumShop.donatello_pay_desc, lang,
                                  {'amount': price, 'currency': config.currency_symbols[currency],
                                   'order_id': order_id}),
            prefix=Func.generate_prefix('🍩'),
            footer_url=Func.generate_footer_url(user=inter.user),
            footer=Func.generate_footer(inter),
            color=config.premium_color,
        ), edit_original_response=False, ephemeral=True)
    await send_callback(inter, embed=generate_embed(translate(Locales.PremiumShop.pay_below_title, lang),
                                                    translate(Locales.PremiumShop.pay_below_desc, lang),
                                                    prefix=Func.generate_prefix('⬇️'),
                                                    footer_url=Func.generate_footer_url(user=inter.user),
                                                    footer=Func.generate_footer(inter),
                                                    color=config.premium_color,
                                                    thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                        config.image_links['shop'])
                                                    ))
