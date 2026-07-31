from ...utils import *
from . import embeds
from . import components
from ...utils.discord_utils import send_callback
from ...core import *


async def wardrobe(inter, message=None, select_item_component_id: str = 'item_select;wardrobe',
                   pre_command_check=True, ephemeral=False, edit_original_response=True, edit_followup: bool = False,
                   tradable_items_only: bool = False,
                   init_category: str = None, init_page: int = 1):
    if pre_command_check:
        await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    embed_thumbnail_url = await DisUtils.generate_user_pig(inter.user.id)
    empty_desc = translate(Locales.Wardrobe.wardrobe_empty_desc, lang)
    _cats = await Tech.get_categorized_items(inter.user.id, 'wardrobe')
    # labels are what the user sees; the raw keys are what travels in custom_ids
    category_labels = {key: (translate(Locales.Global.everything, lang) if key == 'all'
                             else translate(hryak.locale.Locale.SkinTypes[key], lang)) for key in _cats}
    items_by_cats = {category_labels[key]: items for key, items in _cats.items()}
    category_keys = {label: key for key, label in category_labels.items()}
    init_category = category_labels.get(init_category, init_category)
    await DisUtils.pagination(inter, lang, message=message,
                           embeds=await Embeds.generate_items_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                         list_type='wardrobe',
                                                                         select_item_component_id=select_item_component_id,
                                                                         title=translate(
                                                                             Locales.Wardrobe.wardrobe_title,
                                                                             lang),
                                                                         tradable_items_only=tradable_items_only,
                                                                         sort=False,
                                                                         category_keys=category_keys),
                           embed_thumbnail_url=embed_thumbnail_url, ephemeral=ephemeral,
                           edit_original_response=edit_original_response, edit_followup=edit_followup,
                           init_category=init_category,
                           init_page=init_page)


async def inventory(inter, message=None, select_item_component_id: str = 'item_select;inventory',
                    pre_command_check=True, ephemeral=False, edit_original_response=True, edit_followup: bool = False,
                    tradable_items_only: bool = False,
                    init_category: str = None, init_page: int = 1):
    if pre_command_check:
        await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    empty_desc = translate(Locales.Inventory.inventory_empty_desc, lang)
    _cats = await Tech.get_categorized_items(inter.user.id, 'inventory')
    category_labels = {key: translate(Locales.Inventory.inventory_title, lang) for key in _cats}
    items_by_cats = {category_labels[key]: items for key, items in _cats.items()}
    category_keys = {label: key for key, label in category_labels.items()}
    init_category = category_labels.get(init_category, init_category)
    await DisUtils.pagination(inter, lang, message=message,
                           embeds=await Embeds.generate_items_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                         select_item_component_id=select_item_component_id,
                                                                         title=translate(
                                                                             Locales.Inventory.inventory_title,
                                                                             lang),
                                                                         tradable_items_only=tradable_items_only,
                                                                         sort=False,
                                                                         category_keys=category_keys),
                           embed_thumbnail_url=await hryak.Func.get_image_path_from_link(
                               config.image_links['inventory']), ephemeral=ephemeral,
                           edit_original_response=edit_original_response, edit_followup=edit_followup,
                           init_category=init_category,
                           init_page=init_page)


async def wardrobe_item_selected(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = await User.get_language(inter.user.id)
    await send_callback(inter if message is None else message,
                        embed=await Embeds.item_selected_embed(inter, lang, item_id=item_id,
                                                                       _type='wardrobe'),
                        components=await components.inventory_item_selected(inter.user.id, item_id, lang, _type='wardrobe',
                                                                      category=category, page=page))


async def inventory_item_selected(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1,
                                  edit_followup: bool = False):
    lang = await User.get_language(inter.user.id)
    await send_callback(inter if message is None else message, edit_followup=edit_followup,
                        embed=await Embeds.item_selected_embed(inter, lang, item_id=item_id,
                                                                       _type='inventory'),
                        components=await components.inventory_item_selected(inter.user.id, item_id, lang, _type='inventory',
                                                                      category=category, page=page))


async def wardrobe_item_wear(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.wear_skin(inter.user.id, item_id)
    choose_parts = False
    if response.get('status') == hryak.Status.PENDING_CHOOSE_PARTS:
        choose_parts = True
        custom_id = f'in;select_part;{random.randrange(100000)}'
        await send_callback(inter if message is None else message,
                            embed=await embeds.wardrobe_item_choose_layers_to_wear(inter, item_id, lang),
                            components=await components.choose_parts_to_wear(item_id, lang, custom_id),
                            edit_original_response=False,
                            ephemeral=True
                            )

        def check(interaction):
            return interaction.data.get('custom_id') == custom_id


        interaction = await inter.client.wait_for('interaction', check=check)
        response = await hryak.requests.post_requests.wear_skin(inter.user.id, item_id, parts=interaction.data.get('values'))
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_wear(inter, item_id, lang),
                        edit_original_response=True if choose_parts else False,
                        ephemeral=True
                        )
    await wardrobe_item_selected(inter, item_id, inter.message, category=category, page=page)


async def wardrobe_item_remove(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.skin_remove(inter.user.id, item_id)
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_remove(inter, item_id, lang),
                        edit_original_response=False,
                        ephemeral=True
                        )
    await wardrobe_item_selected(inter, item_id, inter.message, category=category, page=page)
