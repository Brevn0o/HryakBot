from ...utils import *
from . import embeds
from . import components


async def wardrobe(inter, message=None, select_item_component_id: str = 'item_select;wardrobe', pre_command_check=True,
                   ephemeral=False, edit_original_message=True, tradable_items_only: bool = False,
                    init_category: str = None, init_page: int = 1):
    if pre_command_check:
        await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    _items = Tech.get_all_items((('inventory_type', 'wardrobe'),), user_id=inter.author.id)
    items_by_cats = {}
    embed_thumbnail_file = await BotUtils.generate_user_pig(inter.author.id)
    empty_desc = Locales.Wardrobe.wardrobe_empty_desc[lang]
    item_types = set()
    for item in _items:
        item_types.add(Item.get_skin_type(item))
    item_types = sorted(item_types)
    for i, item_type in enumerate(['all'] + item_types):
        items_by_cats[Locales.SkinTypes[item_type][lang] if item_type != 'all' else Locales.Global.everything[lang]] = \
            Tech.get_all_items(tuple({'skin_type': item_type}.items())) if item_type != 'all' else _items
    await BotUtils.pagination(inter if message is None else message, lang,
                              embeds=await BotUtils.generate_items_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                               list_type='wardrobe',
                                                                               select_item_component_id=select_item_component_id,
                                                                               title=Locales.Wardrobe.wardrobe_title[
                                                                                   lang],
                                                                               tradable_items_only=tradable_items_only),
                              embed_thumbnail_file=embed_thumbnail_file, ephemeral=ephemeral,
                              edit_original_message=edit_original_message, init_category=init_category, init_page=init_page)


async def inventory(inter, message=None, select_item_component_id: str = 'item_select;inventory',
                    pre_command_check=True, ephemeral=False, edit_original_message=True, tradable_items_only: bool = False,
                    init_category: str = None, init_page: int = 1):
    if pre_command_check:
        await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    _items = Tech.get_all_items((('inventory_type', 'inventory'),), user_id=inter.author.id)
    empty_desc = Locales.Inventory.inventory_empty_desc[lang]
    items_by_cats = {Locales.Inventory.inventory_title[lang]: _items}
    await BotUtils.pagination(inter if message is None else message, lang,
                              embeds=await BotUtils.generate_items_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                               select_item_component_id=select_item_component_id,
                                                                               title=Locales.Inventory.inventory_title[
                                                                                   lang],
                                                                               tradable_items_only=tradable_items_only),
                              embed_thumbnail_file=await Func.get_image_path_from_link(utils_config.image_links['inventory']), ephemeral=ephemeral,
                              edit_original_message=edit_original_message, init_category=init_category, init_page=init_page)


async def wardrobe_item_selected(inter, item_id, message: disnake.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.author.id)
    await send_callback(inter if message is None else message,
                        embed=await BotUtils.generate_item_selected_embed(inter, lang, item_id=item_id, _type='wardrobe'),
                        components=components.inventory_item_selected(inter.author.id, item_id, lang, _type='wardrobe',
                                                                      category=category, page=page))


async def inventory_item_selected(inter, item_id, message: disnake.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.author.id)
    await send_callback(inter if message is None else message,
                        embed=await BotUtils.generate_item_selected_embed(inter, lang, item_id=item_id, _type='inventory'),
                        components=components.inventory_item_selected(inter.author.id, item_id, lang, _type='inventory',
                                                                      category=category, page=page))


async def wardrobe_item_wear(inter, item_id, message: disnake.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.author.id)
    not_compatible_skins = BotUtils.get_not_compatible_skins(inter.author.id, item_id)
    if not_compatible_skins:
        await error_callbacks.not_compatible_skin(inter, item_id, not_compatible_skins, message)
        return
    Pig.set_skin(inter.author.id, item_id)
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_wear(inter, item_id, lang),
                        edit_original_message=False,
                        ephemeral=True
                        )
    await wardrobe_item_selected(inter, item_id, inter.message, category=category, page=page)


async def wardrobe_item_remove(inter, item_id, message: disnake.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.author.id)
    Pig.remove_skin(inter.author.id, Item.get_skin_type(item_id))
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_remove(inter, item_id, lang),
                        edit_original_message=False,
                        ephemeral=True
                        )
    await wardrobe_item_selected(inter, item_id, inter.message, category=category, page=page)
