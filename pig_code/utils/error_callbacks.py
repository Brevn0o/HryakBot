from pig_code.utils.discord_utils import send_callback, generate_embed, send_webhook
from pig_code.utils.functions import Func
from pig_code.utils.functions import translate
from pig_code.core import *


def default_error_embed(inter, title, description, prefix_emoji: str = '❌',
                        color: str = config.error_color, thumbnail_url=None) -> discord.Embed:
    embed = generate_embed(
        title=title,
        description=description,
        prefix=Func.generate_prefix(prefix_emoji),
        inter=inter,
        color=color,
        thumbnail_url=thumbnail_url
    )
    return embed


async def default_error_callback(inter, title, description, prefix_emoji: str = '❌',
                                 color: str = config.error_color, thumbnail_url=None,
                                 edit_original_response: bool = True,
                                 ephemeral: bool = False):
    await send_callback(inter,
                        embed=default_error_embed(inter, title, description, prefix_emoji, color, thumbnail_url),
                        edit_original_response=edit_original_response,
                        ephemeral=ephemeral)


async def error(error, inter):
    try:
        lang = await User.get_language(inter.user.id)
    except Exception:
        # the DB may be exactly what broke — never let the error handler die on it
        lang = hryak.config.user_settings['language']
    text_error = str(type(error)).split('.')[-1].split('\'')[0]
    if type(error) == discord.app_commands.errors.NoPrivateMessage:
        await default_error_callback(inter, translate(Locales.ErrorCallbacks.not_allowed_to_use_command_title, lang),
                                     translate(Locales.ErrorCallbacks.not_owner_desc, lang))
    elif type(error) == discord.app_commands.errors.BotMissingPermissions:
        perms = Func.translate_permissions(error.missing_permissions, lang)
        description = translate(Locales.ErrorCallbacks.bot_missing_perms_desc, lang)
        for n, i in enumerate(perms):
            description += f'\n> {n + 1}. {i}'
        await default_error_callback(inter, translate(Locales.ErrorCallbacks.bot_missing_perms_title, lang),
                                     description,
                                     prefix_emoji='👧', color=config.warn_color, ephemeral=True)
    elif type(error) == discord.app_commands.errors.MissingPermissions:
        perms = Func.translate_permissions(error.missing_permissions, lang)
        description = translate(Locales.ErrorCallbacks.user_missing_perms_desc, lang)
        for n, i in enumerate(perms):
            description += f'\n> {n + 1}. {i}'
        await default_error_callback(inter, translate(Locales.ErrorCallbacks.user_missing_perms_title, lang),
                                     description,
                                     prefix_emoji='👧', color=config.warn_color, ephemeral=True)
    elif type(error) == discord.app_commands.errors.CommandOnCooldown:
        await default_error_callback(inter, translate(Locales.ErrorCallbacks.cooldown_title, lang),
                                     translate(Locales.ErrorCallbacks.cooldown_desc, lang,
                                               {'timestamp': round(hryak.Func.generate_current_timestamp() + error.retry_after)}),
                                     prefix_emoji='⚠️', color=config.warn_color, ephemeral=True)
    elif type(error.original) == discord.errors.Forbidden:
        await default_error_callback(inter, translate(Locales.ErrorCallbacks.forbidden_title, lang),
                                     translate(Locales.ErrorCallbacks.forbidden_desc, lang),
                                     prefix_emoji='👧', color=config.warn_color, ephemeral=True)
    elif type(error.original) == UserInBlackList:
        await black_list(inter)
        return
    elif type(error.original) == NotBotOwner:
        await default_error_callback(inter, translate(Locales.ErrorCallbacks.not_allowed_to_use_command_title, lang),
                                     translate(Locales.ErrorCallbacks.not_owner_desc, lang))
        return
    else:
        await send_callback(inter, embed=generate_embed(
            title=f"{translate(Locales.ErrorCallbacks.unknown_error_title, lang)}",
            color=config.error_color,
            description=translate(Locales.ErrorCallbacks.unknown_error_desc, lang),
            footer=Func.generate_footer(inter, second_part='Unknown error'),
            footer_url=Func.generate_footer_url('user_avatar', inter.user), prefix=Func.generate_prefix('👁️')))
        error_by = ''
        if inter is not None:
            try:
                error_by += f'**Guild:** `{inter.guild.name}`|`[{inter.guild.id}]`\n'
            except:
                pass
            try:
                error_by += f'**Channel:** `{inter.channel.name}`|`[{inter.channel.id}]`\n'
            except:
                pass
            error_by += f'**User:** {inter.user}|`[{inter.user.id}]`\n'
        description = f'{error_by}' \
                      f'```{error}```'
        discohook_embed = discord_webhook.DiscordEmbed(title='Debugger',
                                                       description=description,
                                                       color=config.error_color)
        await send_webhook(config.DEBUGGER_WEBHOOK, discohook_embed, username=str(inter.client.user),
                           avatar_url=inter.client.user.avatar.url,
                           content='<@&1106677021691613205>',
                           file_content=traceback.format_exc())
        print(error)
        raise error


async def cant_duel_with_yourself(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.cant_play_with_yourself_duel_title, lang),
                                 translate(Locales.ErrorCallbacks.cant_play_with_yourself_duel_desc, lang))


async def bot_as_opponent_duel(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.bot_as_opponent_duel_title, lang),
                                 translate(Locales.ErrorCallbacks.bot_as_opponent_duel_desc, lang))


async def cant_breed_with_yourself(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.cant_breed_with_yourself_title, lang),
                                 translate(Locales.ErrorCallbacks.cant_breed_with_yourself_desc, lang))


async def bot_as_partner_breed(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.bot_as_partner_breed_title, lang),
                                 translate(Locales.ErrorCallbacks.bot_as_partner_breed_desc, lang))


async def item_is_not_in_shop(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.item_is_not_in_shop_title, lang),
                                 translate(Locales.ErrorCallbacks.item_is_not_in_shop_desc, lang))


async def not_enough_money(inter, minimum_money: float = None, edit_original_response: bool = False,
                           ephemeral: bool = True):
    lang = await User.get_language(inter.user.id)
    description = translate(Locales.ErrorCallbacks.not_enough_money_desc, lang)
    if minimum_money is not None:
        description += f'\n\n*{translate(Locales.Global.need, lang)}: **{minimum_money}** 🪙*'
    await default_error_callback(inter,
                                 translate(Locales.ErrorCallbacks.not_enough_money_title, lang),
                                 description, prefix_emoji='💸',
                                 ephemeral=ephemeral, edit_original_response=edit_original_response)


async def not_compatible_skin(inter, item_id, not_compatible_skins, message: discord.Message = None):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter if message is None else message,
                                 translate(Locales.ErrorCallbacks.skin_not_compatible_title, lang),
                                 translate(Locales.ErrorCallbacks.skin_not_compatible_desc, lang,
                                           {'skin1': await Item.get_name(item_id, lang),
                                            'skin2': await Item.get_name(not_compatible_skins[0], lang)}),
                                 ephemeral=True, edit_original_response=False)


async def no_money(inter):
    lang = await User.get_language(inter.user.id)
    await send_callback(inter, embed=default_error_embed(inter,
                                                         translate(Locales.ErrorCallbacks.not_enough_money_title, lang),
                                                         translate(Locales.ErrorCallbacks.not_enough_money_desc, lang)))


async def no_item(inter, item, description: str = None, ephemeral=False, edit_original_response=True,
                  thumbnail_url: str = None):
    lang = await User.get_language(inter.user.id)
    title = translate(Locales.ErrorCallbacks.no_item_title, lang, {'item': (await Item.get_name(item, lang)).lower()})
    if description is None:
        description = f"{translate(Locales.ErrorCallbacks.no_item_desc, lang)}"
    await default_error_callback(inter, title, description, ephemeral=ephemeral,
                                 edit_original_response=edit_original_response,
                                 thumbnail_url=thumbnail_url)


async def not_enough_items(inter, item_id, user=None, thumbnail_url: str = None):
    lang = await User.get_language(inter.user.id)
    if user is None:
        title = translate(Locales.ErrorCallbacks.not_enough_item_title, lang)
        description = f"{translate(Locales.ErrorCallbacks.not_enough_item_desc, lang, {'item_emoji': await Item.get_emoji(item_id), 'item': await Item.get_name(item_id, lang)})}"
    else:
        title = translate(Locales.ErrorCallbacks.user_not_enough_item_title, lang)
        description = f"{translate(Locales.ErrorCallbacks.user_not_enough_item_desc, lang, {'user': user.display_name, 'item_emoji': await Item.get_emoji(item_id), 'item': await Item.get_name(item_id, lang)})}"
    await default_error_callback(inter, title, description, ephemeral=True, edit_original_response=True,
                                 thumbnail_url=thumbnail_url)


async def wrong_component_clicked(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.wrong_component_clicked_title, lang),
                                 translate(Locales.ErrorCallbacks.wrong_component_clicked_desc, lang),
                                 ephemeral=True, edit_original_response=False)


async def modal_input_is_not_number(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.modal_input_is_not_number_title, lang),
                                 translate(Locales.ErrorCallbacks.modal_input_is_not_number_desc, lang),
                                 ephemeral=True, edit_original_response=False)


async def modal_amount_too_small(inter, min_amount: int = 1):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.amount_too_small_title, lang),
                                 translate(Locales.ErrorCallbacks.amount_too_small_desc, lang,
                                           {'min_amount': min_amount}),
                                 ephemeral=True, edit_original_response=False)


async def bot_is_restarting(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.bot_is_restarting_title, lang),
                                 translate(Locales.ErrorCallbacks.bot_is_restarting_desc, lang), prefix_emoji='🔃')


async def cannot_use_command_in_this_channel(inter):
    lang = await User.get_language(inter.user.id)
    await default_error_callback(inter,
                                 translate(Locales.ErrorCallbacks.cannot_use_command_in_this_channel_title, lang),
                                 translate(Locales.ErrorCallbacks.cannot_use_command_in_this_channel_desc, lang),
                                 prefix_emoji='❌')


async def black_list(inter):
    lang = await User.get_language(inter.user.id)
    description = translate(Locales.ErrorCallbacks.user_in_black_list_desc, lang)
    block_reason = await User.get_block_reason(inter.user.id)
    if block_reason not in ['', None, 'None']:
        description += f"\n\n```{translate(Locales.Global.reason, lang)}: {block_reason}```"
    await default_error_callback(inter, translate(Locales.ErrorCallbacks.user_in_black_list_title, lang),
                                 description, prefix_emoji='📃',
                                 ephemeral=True, edit_original_response=False)
