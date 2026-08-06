from ...core import *
from ...utils import *


async def shop_item_selected(item_id, lang, category: str = None, page: int = 1,
                             context: str = None) -> list:
    shop_key = 'shop' if context is None else f'{context}_shop'
    components = []
    components.append(discord.ui.Button(
        style=discord.ButtonStyle.green,
        label=translate(Locales.Global.buy, lang),
        # a server purchase is put to a vote, so it takes a different route
        custom_id=f'{"buy" if context is None else "server_buy"};{item_id};{category};{page}',
    ))
    if (await Item.get_type(item_id)).startswith('skin'):
        components.append(discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label=translate(Locales.Global.preview, lang),
            custom_id=f'preview_skin;{item_id};{category};{page}{";server" if context == "server" else ""}',
        ))
    components.append(discord.ui.Button(
        style=discord.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory;{shop_key};{category};{page}',
    ))
    return components
