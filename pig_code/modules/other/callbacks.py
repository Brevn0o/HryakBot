import asyncio

from ...utils import *
from . import embeds
from ...utils.discord_utils import send_callback, generate_embed
from ...core import *



async def profile(inter, user: discord.User = None, pre_command_check: bool = True,
                  edit_original_response: bool = True, ephemeral: bool = False, _components: list = None,
                  info: list = None):
    if pre_command_check:
        await DisUtils.pre_command_check(inter, ephemeral=ephemeral)
    lang = await User.get_language(inter.user.id)
    if info is None:
        info = ['user', 'pig']
    if user is None:
        user = inter.user
    await User.register_user_if_not_exists(user.id)
    if _components is None:
        _components = []
        _components += [discord.ui.Button(
            emoji='👍',
            custom_id=f'like;{user.id}',
            style=discord.ButtonStyle.blurple,
            disabled=True if await User.get_rate_number(user.id, inter.user.id) == 1 else False),
            discord.ui.Button(
                emoji='👎',
                custom_id=f'dislike;{user.id}',
                style=discord.ButtonStyle.blurple,
                disabled=True if await User.get_rate_number(user.id, inter.user.id) == -1 else False
            )
        ]

    await send_callback(inter, embed=await Embeds.profile_embed(inter, lang, user, info,
                                                               await DisUtils.generate_user_pig(user.id)),
                        ephemeral=ephemeral,
                        edit_original_response=edit_original_response, components=_components)


async def view(inter, user: discord.User = None):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    if user is None:
        user = inter.user
    await User.register_user_if_not_exists(user.id)
    await send_callback(inter, embed=generate_embed(timestamp=False,
                                                    image_url=await DisUtils.generate_user_pig(user.id)))


async def promocode(inter, code):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.use_promocode(inter.user.id, code)
    if response.get('status') == hryak.Status.NOT_EXIST:
        await send_callback(inter, embed=await embeds.promocode_not_exist(inter, lang))
        return
    elif response.get('status') == hryak.Status.USED_TOO_MANY_TIMES:
        await send_callback(inter, embed=await embeds.promocode_used_too_many_times(inter, lang))
        return
    elif response.get('status') == hryak.Status.EXPIRED:
        await send_callback(inter, embed=await embeds.promocode_expired(inter, lang))
        return
    elif response.get('status') == hryak.Status.ALREADY_USED:
        await send_callback(inter, embed=await embeds.user_used_promocode(inter, lang))
        return
    elif response.get('status') == hryak.Status.SUCCESS:
        await send_callback(inter, embed=await embeds.promo_code_used(inter, lang, await PromoCode.get_rewards(code)))


async def send_money(inter, user, amount, currency, message=None):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.send_money(inter.user.id, user.id, amount, currency, confirmed=False)
    if response['status'] == hryak.Status.NO_MONEY:
        await error_callbacks.no_money(inter)
        return
    confirmation = await DisUtils.confirm_message(inter, lang,
                                               description=translate(Locales.SendMoney.confirm_desc, lang,
                                                                     {'money': amount, 'user': user.display_name,
                                                                      'tax': response.get('tax'),
                                                                      'currency_emoji': await Item.get_emoji(currency),
                                                                      'money_with_tax': response.get('amount_with_tax'),}))
    if not confirmation:
        await send_callback(inter, embed=await embeds.cancel_sending_money(inter, lang))
        return
    response = await hryak.requests.post_requests.send_money(inter.user.id, user.id, amount, currency, confirmed=True)
    if response['status'] == hryak.Status.NO_MONEY:
        await error_callbacks.no_money(inter)
        return
    title = f'{translate(Locales.SendMoney.event_title, lang)}'
    description = translate(Locales.SendMoney.event_desc, lang,
                            format_options={'user': inter.user.display_name, 'money': amount,
                                            'currency_emoji': await Item.get_emoji(currency)})
    if message is not None:
        description += f'\n\n> {translate(Locales.Global.message, lang)}: *{message}*'
    await DisUtils.send_notification(user, inter, title, description,
                                  prefix_emoji='💸', send_to_dm=True, create_command_notification=True,
                                  notification_id='money_transfer')
    await send_callback(inter, embed=await embeds.transfer_money(inter, lang, user, amount, currency))


async def report(inter: discord.Interaction, text, attachment):
    await DisUtils.pre_command_check(inter)
    discohook_embed = discord_webhook.DiscordEmbed(title=f'{inter.user.global_name}',
                                                   color=config.main_color,
                                                   description=f'> {text}\n\n'
                                                               f'- Nickname: {inter.user.name}\n'
                                                               f'- User ID: {inter.user.id}')
    if attachment is not None:
        discohook_embed.set_image(url=attachment.url)
    discohook_embed.set_thumbnail(url=inter.user.avatar.url)
    for w in config.REPORT_WEBHOOKS:
        webhook = discord_webhook.DiscordWebhook(url=w,
                                                 username='Bug report')

        webhook.add_embed(discohook_embed)
        webhook.execute()
    lang = await User.get_language(inter.user.id)
    await send_callback(inter, embed=await embeds.report(inter, lang))


async def say(inter, text):
    await DisUtils.pre_command_check(inter, ephemeral=True)
    if not await Guild.is_say_allowed(inter.guild.id):
        lang = await User.get_language(inter.user.id)
        await error_callbacks.default_error_callback(inter, translate(Locales.Say.not_allowed_title, lang),
                                                     translate(Locales.Say.not_allowed_desc, lang))
        return
    if not inter.channel.permissions_for(inter.user).mention_everyone:
        text = text.replace('@everyone', '`@everyоne`').replace('@here', '`@hеre`')
    text = text.replace(r'\\', '\n')

    await inter.channel.send(text)
    message = await send_callback(inter, text)
    await message.delete()


async def set_language(inter, lang):
    await DisUtils.pre_command_check(inter, language_check=False)
    await User.set_language(inter.user.id, lang)
    await Stats.set_language_changed(inter.user.id, True)
    await send_callback(inter, embed=generate_embed(title=translate(Locales.SetLanguage.scd_title, lang),
                                                    description=translate(Locales.SetLanguage.scd_desc, lang),
                                                    prefix=Func.generate_prefix('scd'),
                                                    inter=inter))


async def settings_say(inter, allow: bool):
    await DisUtils.pre_command_check(inter, language_check=False)
    lang = await User.get_language(inter.user.id)
    await Guild.allow_say(inter.guild.id, allow)
    await send_callback(inter, content=translate(Locales.SettingsSay.scd_content, lang, {'value': str(allow).lower()}))

async def settings_top(inter, participate: bool):
    await DisUtils.pre_command_check(inter, language_check=False)
    lang = await User.get_language(inter.user.id)
    await User.set_top_participation(inter.user.id, participate)
    await send_callback(inter, content=translate(Locales.SettingsTop.scd_content, lang, {'value': str(participate).lower()}))

async def skin_preview(inter, item_id, message: discord.Message = None):
    lang = await User.get_language(inter.user.id)
    item_id = await Item.clean_id(item_id)
    not_compatible_skins = await hryak.GameFunc.get_not_compatible_active_skins(inter.user.id, item_id)
    if not_compatible_skins:
        await error_callbacks.not_compatible_skin(inter, item_id, not_compatible_skins, message)
        return
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_preview(inter, item_id, lang),
                        edit_original_response=False,
                        ephemeral=True
                        )
