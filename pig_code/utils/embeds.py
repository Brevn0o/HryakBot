from . import DisUtils
from .discord_utils import generate_embed
from .functions import Func, translate
from .components import Components
from ..core import *

class Embeds:
    @staticmethod
    async def profile_embed(inter, lang, user: discord.User = None, info: list = None,
                            thumbnail_url=None) -> discord.Embed:
        if user is None:
            user = inter.user
        description = ''
        if 'user' in info:
            rating_status = ''
            rating_number = await User.get_rating_total_number(user.id)
            if rating_number > 0:
                rating_status = '💚'
            elif rating_number < 0:
                rating_status = '⚠️'
            description += translate(Locales.Profile.user_profile_desc, lang,
                                     format_options={'coins': await Item.get_amount('coins', user.id),
                                                     'hollars': await Item.get_amount('hollars', user.id),
                                                     'likes': rating_number,
                                                     'rating_status': rating_status,
                                                     'pos_amount': await User.get_amount_of_positive_ratings(user.id),
                                                     'neg_amount': await User.get_amount_of_negative_ratings(user.id)}) + '\n\n'
        if 'pig' in info:
            description += translate(Locales.Profile.pig_profile_desc, lang,
                                     format_options={'pig_name': await Pig.get_name(user.id),
                                                     'weight': await Pig.get_weight(user.id),
                                                     'age': await Pig.age(user.id, lang)}) + '\n\n'
        embed = generate_embed(
            title=translate(Locales.Profile.profile_title, lang, {'user': user.display_name}),
            description=description,
            prefix=Func.generate_prefix('🐽'),
            thumbnail_url=thumbnail_url,
            footer=Func.generate_footer(inter, second_part=f'{await Stats.get_streak(user.id)} 🔥'),
            inter=inter,
        )
        return embed

    @staticmethod
    async def item_selected_embed(inter, lang, item_id, _type: str,
                                  # whose things are being looked at - a guild pig keeps
                                  # its own, so there is no user to count them against
                                  inventory: dict = None,
                                  # and which pig to model it on: 'server' previews the item
                                  # on the community pig, since that is what would wear it
                                  context: str = None) -> discord.Embed:
        footer = Func.generate_footer(inter)
        footer_url = Func.generate_footer_url('user_avatar', inter.user)
        basic_info_desc = ''
        title = await Item.get_name(item_id, lang)
        item_description = await Item.get_description(item_id, lang)
        prefix = Func.generate_prefix(await Item.get_emoji(item_id))
        embed_color = hryak.config.rarity_colors[await Item.get_rarity(item_id)]
        thumbnail_url = None
        if await Item.get_type(item_id) == 'skin':
            # which pig the item is modelled on, skins and genetic together - a community
            # pig is a different shape and starts from a different blank
            base = hryak.config.default_guild_pig if context == 'server' else hryak.config.default_pig
            preview_options = await Pig.set_skin_to_options(base['skins'].copy(),
                                                            item_id.split('.')[0], context=context)
            thumbnail_url = await hryak.GameFunc.build_pig(tuple(preview_options.items()),
                                                           tuple(base['genetic'].items()),
                                                           context=context)
        elif await Item.get_image_path(item_id, config.TEMP_FOLDER_PATH) is not None:
            thumbnail_url = await Item.get_image_path(item_id, config.TEMP_FOLDER_PATH)
        if _type in ['inventory', 'wardrobe']:
            amount = await Item.get_amount(item_id, inventory=inventory) if inventory is not None \
                else await Item.get_amount(item_id, inter.user.id)
            basic_info_desc += f'{translate(Locales.Global.amount, lang)}: **{amount}**\n'
            basic_info_desc += f'{translate(Locales.Global.type, lang)}: **{await Item.get_skin_type(item_id, lang, context) if await Item.get_type(item_id) == "skin" else await Item.get_type(item_id, lang)}**\n'
            basic_info_desc += f'{translate(Locales.Global.rarity, lang)}: **{await Item.get_rarity(item_id, lang)}**'
            if await Item.is_salable(item_id):
                basic_info_desc += f'\n{translate(Locales.Global.cost_per_item, lang)}: **{await Item.get_sell_price(item_id)} {await Item.get_emoji(await Item.get_sell_price_currency(item_id))}**'
        elif _type == 'shop':
            if await Item.get_amount(item_id) > 1:
                basic_info_desc += f'{translate(Locales.Global.amount, lang)}: **{await Item.get_amount(item_id)}**\n'
            basic_info_desc += f'{translate(Locales.Global.price, lang)}: **{await Item.get_market_price(item_id, context)} {await Item.get_emoji(await Item.get_market_price_currency(item_id, context))}**\n'
            basic_info_desc += f'{translate(Locales.Global.type, lang)}: **{await Item.get_skin_type(item_id, lang, context) if await Item.get_type(item_id) == "skin" else await Item.get_type(item_id, lang)}**\n'
            basic_info_desc += f'{translate(Locales.Global.rarity, lang)}: **{await Item.get_rarity(item_id, lang)}**'
        embed = generate_embed(
            title=title,
            description=basic_info_desc,
            prefix=prefix,
            footer=footer,
            footer_url=footer_url,
            timestamp=True,
            color=embed_color,
            thumbnail_url=thumbnail_url,
            fields=[{'name': f"📋 ⟩ {translate(Locales.Global.description, lang)}",
                     'value': f"*{item_description}*"}]
        )
        return embed

    @staticmethod
    async def generate_items_list_embeds(inter, _items, lang, empty_desc='Empty', title=None,
                                         prefix_emoji: str = '📦', description='', fields_for_one_page: int = 7,
                                         # description and empty_desc may also be a {category: text}
                                         # mapping, when each category wants its own blurb
                                         list_type: str = 'inventory', tradable_items_only: bool = False,
                                         select_item_component_id: str = 'item_select;inventory', sort=True,
                                         cat_as_title=False, client=None, category_keys: dict = None,
                                         footer_override: str = None,
                                         # whose things are being listed - a guild pig keeps
                                         # its own, so there is no user to count them against
                                         inventory: dict = None,
                                         # and whose config describes them: an item can be
                                         # sold only to servers, in which case everything
                                         # about it lives in its server config
                                         context: str = None):
        complete_embeds = {}
        if sort:
            sorted_items = {}
            for cat in _items:
                if list_type == 'inventory':
                    types = await asyncio.gather(*(Item.get_type(x) for x in _items[cat]))
                    sorted_items[cat] = [x for _, x in sorted(zip(types, _items[cat]), key=lambda pair: pair[0])]
                elif list_type == 'wardrobe':
                    skin_types = await asyncio.gather(*(Item.get_skin_type(x) for x in _items[cat]))
                    sorted_items[cat] = [x for _, x in sorted(zip(skin_types, _items[cat]), key=lambda pair: pair[0])]
            if sorted_items:
                _items = sorted_items.copy()
            # elif list_type == 'shop':
            #     for cat in _items:
            #         sorted_items[cat] = sorted(_items[cat], key=lambda x: await Item.get_market_price(x))
            #     _items = sorted_items.copy()
        if client is None:
            client = inter.client
        for cat, v in _items.items():
            item_fields = []
            options = []
            complete_embeds[cat] = {'embeds': []}
            select_item_placeholder = translate(Locales.Inventory.select_item_placeholder, lang)
            footer_first_part = ''
            for item in v:
                item_label_without_prefix = 'Unknown'
                option_desc = None
                emoji = None
                field_value = '----'
                after_prefix = ''
                if list_type in ['inventory', 'wardrobe']:
                    if tradable_items_only and not await Item.is_tradable(item):
                        continue
                    if await Item.exists(item):
                        field_value = ''
                        amount = await Item.get_amount(item, inventory=inventory) if inventory is not None \
                            else await Item.get_amount(item, inter.user.id)
                        if amount == 0:
                            continue
                        if list_type == 'inventory':
                            field_value += f'{translate(Locales.Global.rarity, lang)}: {await Item.get_rarity(item, lang)}\n'
                            if await Item.is_salable(item):
                                field_value += f'{translate(Locales.Global.cost_per_item, lang)}: {await Item.get_sell_price(item)} {await Item.get_emoji(await Item.get_sell_price_currency(item))}'
                            else:
                                field_value += f'{translate(Locales.Global.type, lang)}: {await Item.get_type(item, lang)}'
                        elif list_type == 'wardrobe':
                            field_value += f'{translate(Locales.Global.type, lang)}: {await Item.get_skin_type(item, lang, context)}\n' \
                                           f'{translate(Locales.Global.rarity, lang)}: {await Item.get_rarity(item, lang)}'
                        field_value = f'```{field_value}```'
                        after_prefix = f" x{amount}"
                        item_label_without_prefix = f'{await Item.get_name(item, lang)}'
                        emoji = await Item.get_emoji(item)
                        option_desc = Func.cut_text(await Item.get_description(item, lang), 100)
                elif list_type == 'shop':
                    field_value = f'```{translate(Locales.Global.price, lang)}: {await Item.get_market_price(item, context)} {await Item.get_emoji(await Item.get_market_price_currency(item, context))}\n' \
                                  f'{translate(Locales.Global.rarity, lang)}: {await Item.get_rarity(item, lang)}```'
                    after_prefix = f" x{await Item.get_amount(item)}" if await Item.get_amount(item) > 1 else ""
                    item_label_without_prefix = f'{await Item.get_name(item, lang)}'
                    emoji = await Item.get_emoji(item)
                    option_desc = Func.cut_text(await Item.get_description(item, lang), 100)
                    # whose balance to show - the buyer's by default, but a server shop
                    # spends the server's money, so the caller can say
                    footer_first_part = footer_override if footer_override is not None else \
                        f'{translate(Locales.Global.balance, lang)}: {await Item.get_amount('coins', inter.user.id)} 🪙'
                item_fields.append(
                    {
                        'name': f'{Func.generate_prefix(emoji, backticks=False)}{item_label_without_prefix}',
                        'value': field_value,
                        'inline': False,
                        'after_prefix': after_prefix})
                options.append(
                    {'label': item_label_without_prefix,
                     'value': f'{item}',
                     'emoji': emoji,
                     'description': option_desc
                     }
                )
            item_fields = Func.field_inline_alternation(item_fields)
            for field in item_fields:
                if field['inline'] is True:
                    field['name'] = Func.cut_text(field['name'], 15)
                field['name'] = f'{field['name']}{field['after_prefix']}'
            cat_description = description.get(cat, '') if isinstance(description, dict) else description
            cat_empty_desc = empty_desc.get(cat, '') if isinstance(empty_desc, dict) else empty_desc
            page_embeds = Embeds.generate_embeds_list_from_fields(item_fields,
                                                                 description=cat_description if item_fields else cat_empty_desc,
                                                                 title=f'{Func.generate_prefix(prefix_emoji)}{title if not cat_as_title else cat}',
                                                                 fields_for_one=fields_for_one_page,
                                                                 footer=Func.generate_footer(inter,
                                                                                             first_part=footer_first_part),
                                                                 footer_url=Func.generate_footer_url('user_avatar',
                                                                                                     inter.user))
            # custom_ids carry the raw category key, not the translated label - it is shorter,
            # ascii-only, and does not change with the user's language
            page_components = Components.generate_select_components_for_pages(options, select_item_component_id,
                                                                         select_item_placeholder,
                                                                         category=(category_keys or {}).get(cat, cat),
                                                                         fields_for_one=fields_for_one_page)
            for i, embed in enumerate(page_embeds):
                complete_embeds[cat]['embeds'].append({'embed': embed, 'components': page_components[i]})
        return complete_embeds

    @staticmethod
    def generate_embeds_list_from_fields(fields: list, title: str = '', description: str = '',
                                         color=config.main_color, fields_for_one: int = 25,
                                         thumbnail_url: str = None, footer: str = None,
                                         footer_url: str = None, timestamp: bool = True):
        fields_for_one -= 1
        embeds = []
        create_embed = lambda: generate_embed(title=title, color=color, description=description,
                                              thumbnail_url=thumbnail_url, footer=footer, footer_url=footer_url,
                                              timestamp=timestamp)
        embed = create_embed()
        for i, field in enumerate(fields, 1):
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
            if i % (fields_for_one + 1) == 0:
                embeds.append(embed)
                embed = create_embed()
        if len(fields) == 0 or i % (fields_for_one + 1) != 0:
            embeds.append(embed)
        return embeds