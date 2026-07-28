from ...core import *
from ...utils import *
from . import embeds
from . import components


async def top(inter, _global: bool = False):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)

    if not _global and not inter.guild.chunked:
        await error_callbacks.bot_is_restarting(inter)
        return

    guild = None if _global else inter.guild
    weight_top_response = await hryak.requests.top_requests.top_weight_users(inter.user.id, lang, guild=guild)
    coins_top_response = await hryak.requests.top_requests.top_amount_of_items_users(inter.user.id, 'coins', guild=guild)
    hollars_top_response = await hryak.requests.top_requests.top_amount_of_items_users(inter.user.id, 'hollars', guild=guild)
    streak_top_response = await hryak.requests.top_requests.top_streak_users(inter.user.id, guild=guild)
    await DisUtils.pagination(inter, lang,
                           embeds={
                               translate(Locales.Top.weight_top_title, lang): {
                                   'embed': await embeds.generate_top_embed(inter, lang,
                                                                            translate(Locales.Top.weight_top_title,
                                                                                      lang),
                                                                            translate(
                                                                                Locales.Top.weight_top_desc,
                                                                                lang),
                                                                            weight_top_response.get('users'),
                                                                            prefix_emoji='🐖',
                                                                            user_position=weight_top_response.get(
                                                                                'user_position'),
                                                                            thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                config.image_links['top'])),
                                   'components': [await components.choose_user(inter, lang, [i[0] for i in
                                                                                             weight_top_response.get(
                                                                                                 'users')])]},
                               translate(Locales.Top.coins_top_title, lang): {
                                   'embed': await embeds.generate_top_embed(inter, lang,
                                                                            translate(Locales.Top.coins_top_title,
                                                                                      lang),
                                                                            translate(
                                                                                Locales.Top.coins_top_desc,
                                                                                lang),
                                                                            coins_top_response.get('users'),
                                                                            prefix_emoji='💰',
                                                                            user_position=coins_top_response.get(
                                                                                'user_position'),
                                                                            thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                config.image_links['top'])),
                                   'components': [await components.choose_user(inter, lang, [i[0] for i in
                                                                                             coins_top_response.get(
                                                                                                 'users')])]},
                               translate(Locales.Top.hollars_top_title, lang): {
                                   'embed': await embeds.generate_top_embed(inter, lang,
                                                                            translate(Locales.Top.hollars_top_title,
                                                                                      lang),
                                                                            translate(
                                                                                Locales.Top.hollars_top_desc,
                                                                                lang),
                                                                            hollars_top_response.get('users'),
                                                                            prefix_emoji='💸',
                                                                            user_position=hollars_top_response.get(
                                                                                'user_position'),
                                                                            thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                config.image_links['top'])),
                                   'components': [await components.choose_user(inter, lang, [i[0] for i in
                                                                                             hollars_top_response.get(
                                                                                                 'users')])]},
                               translate(Locales.Top.streak_top_title, lang): {
                                   'embed': await embeds.generate_top_embed(inter, lang,
                                                                            translate(Locales.Top.streak_top_title,
                                                                                      lang),
                                                                            translate(
                                                                                Locales.Top.streak_top_desc,
                                                                                lang),
                                                                            streak_top_response.get('users'),
                                                                            prefix_emoji='🔥',
                                                                            user_position=streak_top_response.get(
                                                                                'user_position'),
                                                                            thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                config.image_links['top'])),
                                   'components': [await components.choose_user(inter, lang, [i[0] for i in
                                                                                             streak_top_response.get(
                                                                                                 'users')])]},
                           },
                           arrows=False,
                           categories=True)
