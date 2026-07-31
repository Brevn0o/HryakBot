from .....utils import *
from .....utils.discord_utils import send_callback, generate_embed
from .....core import *


async def case_used(inter, item_id, update):
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.open_case(inter.user.id, item_id)
    if response.get('status') == hryak.Status.NOT_ENOUGH_ITEMS:
        await error_callbacks.not_enough_items(inter, item_id,
                                               thumbnail_url=await Item.get_image_path(item_id,
                                                                                       config.TEMP_FOLDER_PATH))
        return
    await send_callback(inter, embed=generate_embed(
        title=translate(Locales.ItemUsed.case_title, lang),
        description=f"```{await DisUtils.get_items_in_str_list(response.get('items_dropped'), lang)}```",
        prefix=Func.generate_prefix('🎁'),
        # color=utils_config.rarity_colors[str(BotUtils.get_rarest_item(items_received))],
        inter=inter,
    ), ephemeral=True, edit_original_response=False)
    await update(edit_followup=True)
