from .embeds import trade_embed
from ...utils import *
from ...utils.discord_utils import send_callback, generate_embed
from ...core import *


async def trade(inter, user1, user2, trade_id: str = None, pre_command_check: bool = True):
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.trade_requests.trade(user1.id, user2.id, trade_id)
    if pre_command_check:
        await DisUtils.pre_command_check(inter)
        if user1.id == user2.id:
            await error_callbacks.default_error_callback(inter, translate(
                Locales.ErrorCallbacks.cant_trade_with_yourself_title, lang),
                                                         translate(Locales.ErrorCallbacks.cant_trade_with_yourself_desc,
                                                                   lang))
            return
        if user2.bot:
            await error_callbacks.default_error_callback(inter,
                                                         translate(Locales.ErrorCallbacks.bot_as_trade_user_title,
                                                                   lang),
                                                         translate(Locales.ErrorCallbacks.bot_as_trade_user_desc, lang))
            return
    if response.get('status') == hryak.Status.NO_TRADE_ID:
        m = await send_callback(inter, '🔃')
        trade_id = str(m.id)
        try:
            m = await inter.channel.fetch_message(m.id)
        except discord.HTTPException:
            pass
        await Trade.create(trade_id, user1.id, user2.id, m)
        response = await hryak.requests.trade_requests.trade(user1.id, user2.id, trade_id)
        await DisUtils.send_notification(user2, inter,
                                         translate(Locales.Trade.trade_invitation_title, await User.get_language(user2.id)),
                                         translate(Locales.Trade.trade_invitation_desc, await User.get_language(user2.id),
                                                   format_options={'user': user1.display_name}),
                                         prefix_emoji='💰',
                                         url_label=translate(Locales.Global.message, await User.get_language(user2.id)),
                                         url=m.jump_url, send_to_dm=True, create_command_notification=False,
                                         guild=inter.guild)
    if await Trade.get_message(trade_id) is None:
        await error_callbacks.cannot_use_command_in_this_channel(inter)
        return
    if response.get('trade_status') == hryak.TradeStatus.IN_PROCESS:
        try:
            await inter.response.defer()
        except discord.InteractionResponded:
            pass
        add_item_component = discord.ui.Select(placeholder=translate(Locales.Trade.add_item_placeholder, lang),
                                               custom_id='trade;add',
                                               options=[
                                                   discord.SelectOption(label=await Item.get_name('coins', lang),
                                                                        value=f'coins;{trade_id}',
                                                                        emoji=await Item.get_emoji('coins')),
                                                   discord.SelectOption(label=await Item.get_name('hollars', lang),
                                                                        value=f'hollars;{trade_id}',
                                                                        emoji=await Item.get_emoji('hollars')),
                                                   discord.SelectOption(
                                                       label=translate(Locales.Global.inventory, lang),
                                                       value=f'inventory;{trade_id}',
                                                       emoji='📦'),
                                                   discord.SelectOption(
                                                       label=translate(Locales.Global.wardrobe, lang),
                                                       value=f'wardrobe;{trade_id}',
                                                       emoji='🎭')
                                               ],
                                               row=0)
        agree_component = discord.ui.Button(style=discord.ButtonStyle.green,
                                            emoji='✅', label=f'{await Trade.get_agree_number(trade_id)}/2',
                                            custom_id=f'trade;agree;{trade_id}',
                                            row=1)
        cancel_component = discord.ui.Button(style=discord.ButtonStyle.red,
                                             emoji='✖️', custom_id=f'trade;cancel;{trade_id}',
                                             row=1)
        clear_component = discord.ui.Button(style=discord.ButtonStyle.blurple,
                                            label=translate(Locales.Global.clear, lang),
                                            custom_id=f'trade;clear;{trade_id}',
                                            row=1)
        await send_callback(await Trade.get_message(trade_id),
                            embed=await trade_embed(inter, trade_id, lang),
                            components=[add_item_component,
                                        agree_component, cancel_component, clear_component])
        return
    elif response.get('trade_status') == hryak.TradeStatus.TAX_PROCESSING:
        response = await hryak.requests.trade_requests.trade(user1.id, user2.id, trade_id)
        if response.get('trade_status') == hryak.TradeStatus.TAX_PROCESSING:
            description = f'{translate(Locales.Trade.tax_splitting_process_desc, lang)}\n'
            for currency, amount in response['total_tax'].items():
                description += f'\n> {await Item.get_emoji(currency)}・{await Item.get_name(currency, lang)} x{amount}'
            description += f'\n\n{translate(Locales.Trade.tax_splitting_process_who_pays_desc, lang)}'
            components = [
                discord.ui.Button(style=discord.ButtonStyle.blurple,
                                  label=f'{f"1/2 " if await Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_1') == 1 else ""}@{user1}',
                                  custom_id=f'trade;tax_split_1;{trade_id}',
                                  row=1),
                discord.ui.Button(style=discord.ButtonStyle.blurple,
                                  label=f'{f"1/2 " if await Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_2') == 1 else ""}@{user2}',
                                  custom_id=f'trade;tax_split_2;{trade_id}',
                                  row=1),
                discord.ui.Button(style=discord.ButtonStyle.blurple,
                                  label=f'{f"{await Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_equal')}/2 " if await Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_equal') > 0 else ""}{translate(Locales.Trade.split_equally, lang)}',
                                  custom_id=f'trade;tax_split_equal;{trade_id}',
                                  row=1)
            ]
            await send_callback(await Trade.get_message(trade_id),
                                embed=generate_embed(translate(Locales.Trade.tax_splitting_process_title, lang),
                                                     description=description,
                                                     prefix=Func.generate_prefix("💸"),
                                                     thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                         config.image_links['trade']),
                                                     footer_url=inter.client.user.avatar.url,
                                                     footer=inter.client.user.display_name
                                                     ),
                                components=components)
            return
    if response.get('trade_status') == hryak.TradeStatus.TAX_PROCESSING_SUCCESS:
        response = await hryak.requests.trade_requests.trade(user1.id, user2.id, trade_id)
    if response.get('trade_status') == hryak.TradeStatus.SUCCESS:
        await send_callback(await Trade.get_message(trade_id), embed=generate_embed(translate(Locales.Trade.scd_title, lang),
                                                                              description=translate(
                                                                                  Locales.Trade.scd_desc, lang,
                                                                                  {'user1': user1.display_name,
                                                                                   'user2': user2.display_name}),
                                                                              prefix=Func.generate_prefix("scd"),
                                                                              thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                                                  config.image_links['trade']),
                                                                              footer_url=inter.client.user.avatar.url,
                                                                              footer=inter.client.user.display_name
                                                                              ))
