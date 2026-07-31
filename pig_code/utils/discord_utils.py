import ssl

import aiohttp.client_exceptions
import discord.errors
import discord.interactions
import discord.ui

from .functions import Func
from ..core import *

async def send_callback(inter,
                        content: str = '',
                        embed: discord.Embed = None,
                        ephemeral: bool = False,
                        send_to_dm: discord.User = None,
                        edit_original_response: bool = True,
                        edit_followup: bool = False,
                        ctx_message: bool = False,
                        components: list = None,
                        attachments: list = None,
                        retries: int = 3):
    view = discord.ui.View()
    components = components or []
    if isinstance(inter,
                  discord.interactions.Interaction) and inter.is_user_integration() and not inter.is_guild_integration():
        content = translate(Locales.user_install_content, await User.get_language(inter.user.id)) + '\n' + content
    for component in components:
        view.add_item(component)
    if attachments is None:
        attachments = []
    caller_attachments = list(attachments)
    file_paths = []  # files we opened ourselves; a File can only be read once, so retries reopen them
    if embed is not None:
        if embed.thumbnail.url is not None and not embed.thumbnail.url.startswith(
                ('http://', 'https://', 'attachment://')):
            original_embed_thumbnail_path = embed.thumbnail.url
            file_paths.append(embed.thumbnail.url)
            attachments.append(discord.File(embed.thumbnail.url, filename=os.path.basename(embed.thumbnail.url)))
            embed.set_thumbnail(url=f'attachment://{os.path.basename(embed.thumbnail.url)}')
        if embed.image.url is not None and not embed.image.url.startswith(('http://', 'https://', 'attachment://')):
            original_embed_image_path = embed.thumbnail.url
            file_paths.append(embed.image.url)
            attachments.append(discord.File(embed.image.url, filename=os.path.basename(embed.image.url)))
            embed.set_image(url=f'attachment://{os.path.basename(embed.image.url)}')
    for attempt in range(retries):
        m = None
        if attempt:
            attachments = caller_attachments + [discord.File(p, filename=os.path.basename(p)) for p in file_paths]
        if not send_to_dm:
            try:
                if ctx_message:
                    try:
                        await inter.response.defer(ephemeral=ephemeral)
                    except Exception as e:
                        pass
                    if type(inter) == discord.TextChannel:
                        channel = inter
                    else:
                        channel = inter.channel
                    m = await channel.send_message(content, embed=embed, view=view, attachments=attachments)
                elif edit_followup:
                    await inter.followup.edit_message(inter.message.id, content=content, embed=embed,
                                                      view=view,
                                                      attachments=attachments)
                elif type(inter) in [discord.Message, discord.InteractionMessage]:
                    if edit_original_response:
                        m = await inter.edit(content=content, embed=embed, view=view, attachments=attachments)
                else:
                    try:
                        if edit_original_response:
                            await inter.response.defer(ephemeral=ephemeral)
                    except discord.errors.InteractionResponded as e:
                        pass
                    try:
                        if edit_original_response:
                            try:
                                m = await inter.edit_original_response(content=content, embed=embed,
                                                                       view=view,
                                                                       attachments=attachments)
                            except (ssl.SSLError, aiohttp.client_exceptions.ClientError):
                                raise  # let the retry handler below deal with it
                            except Exception as e:
                                print(e)
                        else:
                            extra_kwargs = {}
                            if embed is not None:
                                extra_kwargs['embed'] = embed
                            m = await inter.response.send_message(content, ephemeral=ephemeral,
                                                                  view=view, files=attachments,
                                                                  **extra_kwargs)
                    except discord.HTTPException as e:
                        print(e)
                        m = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                              view=view, files=attachments)

            except (aiohttp.client_exceptions.ClientError, ssl.SSLError) as e:
                print(f'[send_callback] transient connection error, attempt {attempt + 1}/{retries}: {e}')
                await asyncio.sleep(1)
                continue
            except ValueError as e:
                print(e)
                if embed.thumbnail.url is not None and embed.thumbnail.url.startswith('attachment://'):
                    if embed.thumbnail.url is not None:
                        for n, file in enumerate(attachments):
                            if file.filename == embed.thumbnail.url.split('://')[1]:
                                attachments.pop(n)
                                attachments.append(discord.File(original_embed_thumbnail_path,
                                                                filename=os.path.basename(
                                                                    original_embed_thumbnail_path)))
                        embed.set_thumbnail(url=f'attachment://{os.path.basename(original_embed_thumbnail_path)}')
                if embed.image.url is not None and embed.image.url.startswith('attachment://'):
                    if embed.image.url is not None:
                        for n, file in enumerate(attachments):
                            if file.filename == embed.image.url.split('://')[1]:
                                attachments.pop(n)
                                attachments.append(discord.File(original_embed_image_path,
                                                                filename=os.path.basename(
                                                                    original_embed_image_path)))
                        embed.set_thumbnail(url=f'attachment://{os.path.basename(original_embed_image_path)}')
                await asyncio.sleep(.5)
                continue
            except Exception as e:
                raise e
        else:
            try:
                m = await send_to_dm.send(content, embed=embed, view=view, files=attachments)
            except Exception as e:
                print(e)
        return m


def generate_embed(title: str = None,
                   description: str = None,
                   color=config.main_color,
                   prefix: str = None,
                   image_url: str = None,
                   thumbnail_url: str = None,
                   footer: str = None,
                   footer_url: str = None,
                   fields: list = None,
                   timestamp: bool = True,
                   inter=None) -> discord.Embed:
    if fields is None:
        fields = []
    if timestamp is True:
        timestamp = datetime.datetime.now()
    elif not timestamp:
        timestamp = None
    elif timestamp is not None:
        timestamp = datetime.datetime.fromtimestamp(timestamp)
    title = '' if title is None else title
    prefix = '' if prefix is None else prefix
    embed = discord.Embed(
        title=f'{prefix}{title}',
        description=description,
        color=color,
        timestamp=timestamp
    )
    if image_url is not None:
        embed.set_image(url=image_url)
    if thumbnail_url is not None:
        embed.set_thumbnail(url=thumbnail_url)
    if footer_url is None and inter is not None:
        footer_url = Func.generate_footer_url('user_avatar', inter.user)
    if footer is not None:
        embed.set_footer(text=footer, icon_url=footer_url)
    elif inter is not None:
        embed.set_footer(text=Func.generate_footer(inter), icon_url=footer_url)
    for field in fields:
        embed.add_field(name=field['name'] if 'name' in field else None,
                        value=field['value'] if 'value' in field else None,
                        inline=field['inline'] if 'inline' in field else None)
    return embed


async def send_webhook(url: str, embed=None, content: str = None, username=None, avatar_url=None,
                       file_name: str = 'webhook.txt', file_content=None, retries: int = 3):
    webhook = discord_webhook.DiscordWebhook(content=content, url=url, username=username, avatar_url=avatar_url)
    if file_content is not None:
        webhook.add_file(filename=file_name, file=file_content)
    if embed is not None:
        webhook.add_embed(embed)
    for i in range(retries):
        try:
            webhook_ex = webhook.execute()
            if webhook_ex.status_code == 200:
                break
            elif webhook_ex.status_code == 429:
                await asyncio.sleep(webhook_ex.json()['retry_after'] / 1000 + .2)
            else:
                break
        except requests.exceptions.SSLError as e:
            print('! Webhook send error', e)
            await asyncio.sleep(1)
            continue

class DisUtils:

    @staticmethod
    async def generate_user_pig(user_id: int, eye_emotion: str = None, preview_items: dict = None):
        user_skin = await Pig.get_skin(user_id, 'all')
        for k, v in user_skin.items():
            if await Item.get_amount(v, user_id) <= 0:
                user_skin[k] = None
        if preview_items is not None:
            for item_id in preview_items.values():
                user_skin = await Pig.set_skin_to_options(user_skin, item_id)
        final_pig = await hryak.GameFunc.build_pig(tuple(user_skin.items()),
                                          tuple((await Pig.get_genetic(user_id, 'all')).items()),
                                          eye_emotion=eye_emotion)
        return final_pig

    @staticmethod
    def check_if_right_user(interaction, except_users: list = None):
        if except_users is None:
            except_users = []
        if interaction.user.id in except_users:
            return True
        return interaction.message.interaction.user.id == interaction.user.id

    @staticmethod
    async def send_notification(user: discord.User, inter=None, title: str = None, description: str = None,
                                prefix_emoji: str = None, url_label: str = None, url: str = None,
                                send_to_dm: bool = True,
                                create_command_notification: bool = False, notification_id: str = None,
                                guild=None):
        """
        :type user: object
            User who will receive notification
        :param title:
            Title of notification
        :param description:
            Description of notification
        :param prefix_emoji:
            The prefix before title
        :param url_label:
            The button label containing url
        :param url:
            The URL that will be placed in the button below the message
        :param send_to_dm:
            If true it will try to send notification to user's dm
        :param create_command_notification:
            If true it will show notification next time when user will use the bot command
            (will not work if sending notification to dm was successful)
        :param notification_id:
            Needed for create_command_notification. If not specified, a random ID will be generated.
        :param guild:
            The notification will not be sent if both users are not in the specified guild
        """
        lang = await User.get_language(user.id)
        embed = generate_embed(
            title=title,
            description=description,
            prefix=Func.generate_prefix(prefix_emoji),
            footer_url=Func.generate_footer_url('user_avatar', user),
            footer=Func.generate_footer(user=user)
        )
        components = []
        if url is not None:
            components.append(
                discord.ui.Button(style=discord.ButtonStyle.url,
                                  label=translate(url_label, lang),
                                  url=url)
            )
        dm_message = None
        if send_to_dm:
            if guild is None or (
                    guild.get_member(inter.user.id) is not None and guild.get_member(user.id) is not None):
                dm_message = await send_callback(None, embed=embed, components=components, send_to_dm=user)
        if create_command_notification:
            if dm_message is None:
                 await Events.add(user.id, title=title,
                           description=description, expires_in=100 * 3600,
                           event_id=notification_id)
        return

    @staticmethod
    async def pagination(inter,
                         lang: str,
                         embeds,
                         message: discord.Message = None,
                         timeout: int = 180,
                         embed_thumbnail_url: str = None,
                         ctx_message: bool = False,
                         everyone_can_click: bool = False,
                         return_if_starts_with: list = None,
                         arrows: bool = True,
                         categories: bool = False,
                         ephemeral=False,
                         edit_original_response=True,
                         edit_followup: bool = False,
                         init_category=None,
                         init_page=1):
        if return_if_starts_with is None:
            return_if_starts_with = ['back_to_inventory', 'item_select']
        complete_embeds = {}
        current_page = init_page
        current_cat = None

        def set_thumbnail_if_not_none():
            if embed_thumbnail_url is not None:
                get_current_embed()['embed'].set_thumbnail(url=embed_thumbnail_url)

        def is_categorised_pages():
            try:
                return type(embeds) == dict and type(list(embeds.values())[0]) == dict and \
                    'embeds' in list(embeds.values())[0] and 'embed' in list(embeds.values())[0]['embeds'][0]
            except:
                return False

        def get_current_embed():
            if not is_categorised_pages():
                return embeds[list(embeds)[current_page - 1]]
            else:
                return embeds[current_cat]['embeds'][current_page - 1]

        def category_components():
            options = [discord.SelectOption(label=j, value=str(i), emoji='➡️' if current_cat == i else None) for i, j in
                       enumerate(embeds)]
            if is_categorised_pages():
                options = [discord.SelectOption(label=i, value=str(i), emoji='➡️' if current_cat == i else None) for i
                           in embeds]
            return discord.ui.Select(custom_id='in;select_category',
                                     placeholder=translate(Locales.Pagination.select_category, lang),
                                     options=options,
                                     row=3)

        def arrows_components():
            return [discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label=translate(Locales.Pagination.previous, lang),
                emoji='◀',
                custom_id='in;previous',
                row=4
            ),
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    label=translate(Locales.Pagination.next, lang),
                    emoji='▶',
                    custom_id='in;next',
                    row=4
                )
            ]

        if is_categorised_pages():
            current_cat = list(embeds)[0]
            if init_category is not None and init_category in embeds:
                current_cat = init_category
            if len(embeds) > 1:
                for cat in embeds.copy():
                    for embed in embeds[cat]['embeds']:
                        embed['components'].append(category_components())
                        if len(embeds[cat]['embeds']) > 1:
                            embed['components'] += arrows_components()
                for i in embeds:
                    if len(embeds[i]['embeds']) > 1:
                        for j, embed in enumerate(embeds[i]['embeds']):
                            embed['embed'].set_footer(
                                text=f'📚 {translate(Locales.Pagination.page, lang)}: {j + 1}')
            elif len(embeds[list(embeds)[0]]['embeds']) > 1:
                for i, embed in enumerate(embeds[list(embeds)[0]]['embeds']):
                    embed['components'] += arrows_components()
                    embed['embed'].set_footer(text=f'📚 {translate(Locales.Pagination.page, lang)}: {i + 1}')


        else:
            for i, embed in enumerate(embeds):
                if type(embed) == discord.Embed:
                    complete_embeds[str(i)] = {'embed': embed,
                                               'components': []}
                elif type(embed) == str:
                    if type(embeds[embed]) == discord.Embed:
                        complete_embeds[embed] = {'embed': embeds[embed],
                                                  'components': []}
                    elif type(embeds[embed]) == dict:
                        complete_embeds[embed] = embeds[embed]
                elif type(embed) == dict:
                    complete_embeds[str(i)] = embed
            for i, embed in enumerate(complete_embeds.values()):
                if 'components' not in embed:
                    embed['components'] = []
                if len(embeds) > 1:
                    if categories:
                        embed['components'].append(category_components())
                    if arrows:
                        embed['components'] += arrows_components()
            embeds = complete_embeds.copy()
            for i, element in enumerate(embeds.values()):
                if arrows and len(embeds) > 1:
                    element['embed'].set_footer(
                        text=f'📚 {translate(Locales.Pagination.page, lang)}: {i + 1}',
                        icon_url=Func.generate_footer_url('user_avatar', inter.user))
        if is_categorised_pages():
            if len(embeds[current_cat]['embeds']) < current_page:
                current_page = 1
        else:
            if len(embeds) < current_page:
                current_page = 1
        set_thumbnail_if_not_none()
        message = await send_callback(inter if message is None else message, embed=get_current_embed()['embed'],
                                      components=get_current_embed()['components'],
                                      ctx_message=ctx_message, ephemeral=ephemeral,
                                      edit_original_response=edit_original_response, edit_followup=edit_followup)
        if message is None:
            try:
                message = await inter.original_response()
            except:
                pass

        def check(interaction):
            if message is not None and interaction.message is not None and type(
                    interaction) == discord.interactions.Interaction:
                right_message = message.id == interaction.message.id
                return right_message

        while True:
            try:
                interaction = await inter.client.wait_for('interaction',
                                                          check=check,
                                                          timeout=timeout)
                if not everyone_can_click and inter.user.id != interaction.user.id:
                    try:
                        await send_callback(interaction,
                                            embed=generate_embed(
                                                prefix=Func.generate_prefix('❌'),
                                                color=config.error_color,
                                                title=Locales.Pagination.wrong_user_title[
                                                    await User.get_language(interaction.user.id)],
                                                description=Locales.Pagination.wrong_user_desc[
                                                    await User.get_language(interaction.user.id)],
                                                inter=inter),
                                            edit_original_response=False,
                                            ephemeral=True)
                    except:
                        pass
                    continue
            except asyncio.exceptions.TimeoutError as e:
                try:
                    set_thumbnail_if_not_none()
                    await message.edit(view=None)
                except:
                    pass
                return
            if type(interaction) != discord.interactions.Interaction:
                continue
            if interaction.data.get('custom_id') in ['in;next', 'in;previous', 'hide', 'in;select_category']:
                try:
                    if not ephemeral:
                        await interaction.response.defer(ephemeral=True)
                except discord.errors.HTTPException:
                    return
            if interaction.data.get('custom_id') == 'in;next':
                embeds_num = len(embeds)
                if is_categorised_pages():
                    embeds_num = len(embeds[current_cat]['embeds'])
                current_page = Func.get_changed_page_number(embeds_num, current_page, 1)
            elif interaction.data.get('custom_id') == 'in;previous':
                embeds_num = len(embeds)
                if is_categorised_pages():
                    embeds_num = len(embeds[current_cat]['embeds'])
                current_page = Func.get_changed_page_number(embeds_num, current_page, -1)
            elif interaction.data.get('custom_id') == 'in;select_category':
                if not is_categorised_pages():
                    current_page = int(interaction.data.get('values')[0]) + 1
                else:
                    current_cat = interaction.data.get('values')[0]
                    current_page = 1
            elif interaction.data.get('custom_id') == 'hide':
                return
            elif Func.startswith_list(interaction.data.get('custom_id'), return_if_starts_with):
                return
            else:
                continue
            embed = get_current_embed()['embed']
            components = get_current_embed()['components']
            for i in range(len(components)):
                try:
                    if components[i].custom_id == 'in;select_category':
                        components[i] = category_components()
                except TypeError as e:
                    continue
            set_thumbnail_if_not_none()
            await send_callback(interaction if not ctx_message else message,
                                embed=embed,
                                components=components
                                )

    @staticmethod
    async def get_items_in_str_list(items_to_convert: dict, lang, add_prefixes: bool = True):
        list_res = []
        for item_id in items_to_convert:
            if type(items_to_convert[item_id]) == dict:
                if items_to_convert[item_id]["amount"] > 0:
                    list_res.append(
                        f'{Func.generate_prefix(await Item.get_emoji(item_id)) if add_prefixes else ""}{await Item.get_name(item_id, lang)} x{items_to_convert[item_id]["amount"]}')
            else:
                if items_to_convert[item_id] > 0:
                    list_res.append(
                        f'{Func.generate_prefix(await Item.get_emoji(item_id)) if add_prefixes else ""}{await Item.get_name(item_id, lang)} x{items_to_convert[item_id]}')
        return '\n'.join(list_res)

    @staticmethod
    async def confirm_message(inter, lang, description: str = '', image_url=None, ctx_message=False,
                              ephemeral: bool = False):
        message = await send_callback(inter, embed=generate_embed(
            title=translate(Locales.Global.are_you_sure, lang),
            description=description,
            prefix=Func.generate_prefix('❓'),
            image_url=image_url,
            inter=inter,
        ), ctx_message=ctx_message,
                                      ephemeral=ephemeral,
                                      components=[
                                          discord.ui.Button(
                                              label=translate(Locales.Global.yes, lang),
                                              custom_id='in;yes',
                                              # emoji='✅',
                                              style=discord.ButtonStyle.green
                                          ),
                                          discord.ui.Button(
                                              label=translate(Locales.Global.no, lang),
                                              custom_id='in;no',
                                              # emoji='❌',
                                              style=discord.ButtonStyle.red
                                          )
                                      ])

        def check(interaction):
            if message is not None and interaction.message is not None:
                right_message = message.id == interaction.message.id
                return right_message and DisUtils.check_if_right_user(interaction)

        interaction = await inter.client.wait_for('interaction', check=check)
        try:
            await interaction.response.defer(ephemeral=True)
        except discord.errors.HTTPException:
            return
        if interaction.data.get('custom_id') == 'in;yes':
            return True
        elif interaction.data.get('custom_id') == 'in;no':
            return False


    @staticmethod
    async def pre_command_check(inter, ephemeral=False, defer=True, language_check: bool = True,
                                owner_only: bool = False, allowed_users: list = None):
        if defer:
            try:
                await inter.response.defer(ephemeral=ephemeral)
            except:
                pass
        await User.register_user_if_not_exists(inter.user.id)
        if inter.is_guild_integration() and inter.guild is not None and not inter.guild.chunked:
            try:
                await asyncio.wait_for(inter.guild.chunk(), timeout=5)
            except asyncio.TimeoutError:
                print("> Chunking took too long and was stopped")
        if inter.guild is not None:
            await Guild.register_guild_if_not_exists(inter.guild.id)
        if not await Stats.get_language_changed(inter.user.id) and language_check:
            lang = str(inter.locale)
            if lang in ['ru', 'uk']:
                lang = 'ru'
            else:
                lang = 'en'
            await User.set_language(inter.user.id, lang)
            await Stats.set_language_changed(inter.user.id, True)
            await Pig.rename(inter.user.id, hryak.Func.generate_random_pig_name(await User.get_language(inter.user.id)))
        if await User.is_blocked(inter.user.id):
            raise UserInBlackList(inter.user)
        if owner_only and not await inter.client.is_owner(inter.user):
            raise NotBotOwner(inter.user)
        if allowed_users is not None and inter.user.id not in allowed_users:
            raise NotBotOwner(inter.user)
        for event_id, event_data in (await Events.get_events(inter.user.id)).copy().items():
            await Events.remove(inter.user.id, event_id)
            wait_for_btn = .7
            if event_data['expires_in'] is None or event_data['expires_in'] + event_data[
                'created'] > hryak.Func.generate_current_timestamp():
                await DisUtils.event_callback(inter, event_data, wait_for_btn)


    @staticmethod
    async def event_callback(inter, event, wait_for_btn: float = .7):
        lang = await User.get_language(inter.user.id)
        title = event['title'] if type(event['title']) != dict else translate(event['title'], lang)
        description = event['description'] if type(event['description']) != dict else translate(event['description'],
                                                                                                lang)
        embed = generate_embed(title=title,
                               description=description,
                               timestamp=event['created'],
                               inter=inter)
        components = [
            discord.ui.Button(
                custom_id='in;ok',
                style=discord.ButtonStyle.green,
                # emoji='✅',
                label=translate(Locales.Global.got_it_btn, lang),
                disabled=True
            )]
        message = await send_callback(inter, embed=embed, components=components)
        await asyncio.sleep(wait_for_btn)
        components[0].disabled = False
        message = await send_callback(message, embed=embed, components=components)
        while True:
            def check(interaction):
                if message is not None and interaction.message is not None and type(
                        interaction) == discord.interactions.Interaction:
                    right_message = message.id == interaction.message.id
                    return right_message

            interaction = await inter.client.wait_for('interaction',
                                                      check=check)
            if not DisUtils.check_if_right_user(interaction):
                continue
            if interaction.data.get('custom_id') == 'in;ok':
                await interaction.response.defer()
                break
            break

# @staticmethod
    # async def send_promocodes_guild_message(guild: discord.Guild):
    #     members_count = len([i for i in guild.members if not i.bot])
    #     promocodes = []
    #     if members_count >= 30:
    #         promocodes.append(await PromoCode.create(5, {'coins': 30}))
    #     elif members_count >= 100:
    #         promocodes.append(await PromoCode.create(3, {'rare_case': 2}))
    #         promocodes.append(await PromoCode.create(5, {'coins': 100}))
    #         promocodes.append(await PromoCode.create(members_count // 5, {'coins': 30}))
    #     elif members_count > 500:
    #         promocodes.append(await PromoCode.create(1, {'gold_body': 1}))
    #         promocodes.append(await PromoCode.create(5, {'rare_case': 2}))
    #         promocodes.append(await PromoCode.create(5, {'common_case': 3}))
    #         promocodes.append(await PromoCode.create(members_count // 50, {'coins': 100}))
    #         promocodes.append(await PromoCode.create(members_count // 10, {'coins': 50}))
    #     elif members_count > 1000:
    #         promocodes.append(await PromoCode.create(1, {'gold_body': 1}))
    #         promocodes.append(await PromoCode.create(1, {'gold_pupils': 1}))
    #         promocodes.append(await PromoCode.create(5, {'rare_case': 2}))
    #         promocodes.append(await PromoCode.create(5, {'common_case': 3}))
    #         promocodes.append(await PromoCode.create(members_count // 50, {'coins': 100}))
    #         promocodes.append(await PromoCode.create(members_count // 10, {'coins': 50}))
    #         promocodes.append(await PromoCode.create(3, {'hollars': 20}))
    #     promocodes_text = ''
    #     for promocode in promocodes:
    #         promocodes_text += f'- {promocode}\n' \
    #                            f' > Содержимое: **{DisUtils.get_items_in_str_list(await PromoCode.get_prise(promocode), "ru", add_prefixes=False)}**\n' \
    #                            f' > Макс. использований: **{await PromoCode.max_uses(promocode)}**\n'
    #     await DisUtils.send_notification(guild.owner, title='Привет', prefix_emoji='🍖',
    #                                      description=f'*Вижу у вас неплохой сервер. В честь этого мы дарим вам промокоды для розыгрыша между участниками. Думаю это поможет поднять актив на сервере*\n\n'
    #                                                  f'**Вот промокоды:**\n'
    #                                                  f'{promocodes_text}')

