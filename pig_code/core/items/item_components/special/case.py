from ... import *
from .....utils import *


async def case_used(inter, item_id, update):
    lang = User.get_language(inter.author.id)
    items_dropped = Item.generate_case_drop(item_id)
    if None in items_dropped:
        items_dropped.pop(None)
    User.add_item(inter.author.id, item_id, -1)
    for item, amount in items_dropped.items():
        User.add_item(inter.author.id, item, amount)
    await send_callback(inter, embed=generate_embed(
        title=translate(Locales.ItemUsed.case_title, lang),
        description=f"```{BotUtils.get_items_in_str_list(items_dropped, lang)}```",
        prefix=Func.generate_prefix('🎁'),
        # color=utils_config.rarity_colors[str(BotUtils.get_rarest_item(items_received))],
        inter=inter,
    ), ephemeral=True, edit_original_message=False)
    await update()