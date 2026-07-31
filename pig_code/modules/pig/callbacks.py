from ...utils import *
from . import embeds
from ...utils.discord_utils import send_callback
from ...core import *


async def feed(inter):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.feed(inter.user.id)
    if response.get('status') == hryak.Status.NOT_READY:
        await error_callbacks.default_error_callback(inter,
                                                     title=translate(Locales.ErrorCallbacks.pig_feed_cooldown_title,
                                                                     lang),
                                                     description=translate(
                                                         Locales.ErrorCallbacks.pig_feed_cooldown_desc, lang,
                                                         {'pig': await Pig.get_name(inter.user.id),
                                                          'timestamp': response.get('try_again')}),
                                                     color=config.main_color, prefix_emoji='🍖')
        return
    await send_callback(inter, embed=await embeds.feed(inter, lang, response.get('weight_added'),
                                                       response.get('pooped_amount'), response.get('vomit')))


async def butcher(inter):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.butcher(inter.user.id)
    if response.get('status') == hryak.Status.NOT_READY:
        await error_callbacks.default_error_callback(inter,
                                                     title=translate(Locales.ErrorCallbacks.pig_butcher_cooldown_title,
                                                                     lang),
                                                     description=translate(
                                                         Locales.ErrorCallbacks.pig_butcher_cooldown_desc, lang,
                                                         {'pig': await Pig.get_name(inter.user.id),
                                                          'timestamp': response.get('try_again')}),
                                                     color=config.main_color, prefix_emoji='🥓')
        return
    if response.get('status') == hryak.Status.NO_ITEM_KNIFE:
        await error_callbacks.no_item(inter, 'knife', description=translate(Locales.Butcher.no_knife_desc,
                                                                            await User.get_language(inter.user.id)),
                                      thumbnail_url=await Item.get_image_path('knife', config.TEMP_FOLDER_PATH))
        return
    await send_callback(inter, embed=await embeds.butcher(inter, lang, response.get('lard_added'),
                                                          response.get('weight_lost')))


async def rename(inter, name):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    await hryak.requests.post_requests.rename(inter.user.id, name)
    await send_callback(inter, embed=await embeds.rename(inter, lang))
