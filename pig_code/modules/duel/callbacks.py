from ...utils import *
from . import embeds
from . import components
from ...utils.discord_utils import send_callback, generate_embed
from ...core import *


async def duel(inter, opponent, bet):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    await User.register_user_if_not_exists(opponent.id)
    if opponent == inter.user:
        await error_callbacks.default_error_callback(inter, translate(
            Locales.ErrorCallbacks.cant_play_with_yourself_duel_title, lang),
                                                     translate(Locales.ErrorCallbacks.cant_play_with_yourself_duel_desc,
                                                               lang))
        return
    if opponent.bot is True:
        await error_callbacks.default_error_callback(inter,
                                                     translate(Locales.ErrorCallbacks.bot_as_opponent_duel_title, lang),
                                                     translate(Locales.ErrorCallbacks.bot_as_opponent_duel_desc, lang))
        return
    message = await send_callback(inter,
                                  embed=generate_embed(
                                      title=translate(Locales.Duel.invite_title, lang),
                                      description=translate(Locales.Duel.personal_invite_desc, lang).format(
                                          opponent=opponent.display_name,
                                          user=inter.user.display_name, bet=bet),
                                      prefix=Func.generate_prefix('⚔️'),
                                      inter=inter,
                                  ),
                                  components=components.invite_components(lang))
    await DisUtils.send_notification(opponent, inter,
                                     translate(Locales.Duel.invite_title, await User.get_language(opponent.id)),
                                     translate(Locales.Duel.personal_invite_dm_desc, await User.get_language(opponent.id),
                                               format_options={'user': inter.user.display_name, 'bet': bet}),
                                     prefix_emoji='⚔️',
                                     url_label=translate(Locales.Global.message, await User.get_language(opponent.id)),
                                     url=message.jump_url if message is not None else None, send_to_dm=True,
                                     create_command_notification=False,
                                     guild=inter.guild)

    def check(interaction):
        if message is not None and interaction.message is not None:
            right_message = message.id == interaction.message.id
            return right_message and opponent.id == interaction.user.id

    try:
        interaction = await inter.client.wait_for('interaction', check=check, timeout=1800)
    except asyncio.exceptions.TimeoutError:
        await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                     translate(Locales.Duel.no_response_desc, lang,
                                                               format_options={'user': opponent.display_name}))
        return
    if interaction.data.get('custom_id') == 'in;accept':
        await interaction.response.defer(ephemeral=True)
        response = await hryak.requests.duel_requests.duel(inter.user.id, opponent.id, bet)
        if response.get('status') == hryak.Status.NO_MONEY:
            broke_user = await User.get_discord_user(inter.client, response.get('user_id'))
            await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                         translate(Locales.Duel.no_money_for_bet_desc, lang,
                                                                   format_options={'user': broke_user.display_name}))
            return
        for i in range(10):
            await send_callback(interaction, embed=await embeds.fight_is_starting(inter, lang, inter.user.id, opponent.id, 10 - i,
                                                                            list(response.get('chances').values())))
            await asyncio.sleep(1)
        await send_callback(interaction, embed=await embeds.fight_is_going(inter, lang, inter.user.id, opponent.id,
                                                                     random.choice(hryak.config.fight_gifs)))
        await asyncio.sleep(11)
        await send_callback(interaction, embed=await embeds.user_won(inter, lang, response.get('winner_id'), response.get('money_earned'),
                                                               random.choice(hryak.config.win_gifs)))
    elif interaction.data.get('custom_id') == 'in;reject':
        await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                     translate(Locales.Duel.opponent_reject_desc, lang,
                                                               format_options={'user': opponent.display_name}))
