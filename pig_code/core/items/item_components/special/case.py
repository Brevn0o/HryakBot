from .....utils import *
from .....utils.discord_utils import send_callback, generate_embed
from .....core import *


async def case_used(inter, item_id, update):
    lang = await User.get_language(inter.user.id)
    items_dropped = await Item.generate_case_drop(item_id)
    if None in items_dropped:
        items_dropped.pop(None)
    await User.remove_item(inter.user.id, item_id, 1)
    for item, amount in items_dropped.items():
        await User.add_item(inter.user.id, item, amount)
    await send_callback(inter, embed=generate_embed(
        title=translate(Locales.ItemUsed.case_title, lang),
        description=f"```{await DisUtils.get_items_in_str_list(items_dropped, lang)}```",
        prefix=Func.generate_prefix('🎁'),
        # color=utils_config.rarity_colors[str(BotUtils.get_rarest_item(items_received))],
        inter=inter,
    ), ephemeral=True, edit_original_response=False)
    await update(edit_followup=True)
