from .....utils import *
from .....utils.discord_utils import send_callback, generate_embed
from .....core import *


async def eat(inter, item_id, update):
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.eat_poop(inter.user.id, item_id)
    if response.get('status') == hryak.Status.NOT_ENOUGH_ITEMS:
        await error_callbacks.not_enough_items(inter, item_id)
        return
    scenario = response.get('scenario')
    if scenario == 'poisoned':
        await send_callback(inter, embed=eaten_and_poisoned(inter, lang),
                            components=[discord.ui.Button(
                                label=translate(Locales.Global.pay, lang),
                                custom_id='in;pay',
                                emoji='🪙',
                                style=discord.ButtonStyle.primary
                            ), discord.ui.Button(
                                label=translate(Locales.Global.run_away, lang),
                                custom_id='in;run_away',
                                emoji='🏃‍♂️',
                            )],
                            ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)
        interaction = await inter.client.wait_for('interaction')
        if interaction.data.get('custom_id') == 'in;run_away':
            await interaction.response.defer()
            await inter.edit_original_response(embed=ran_away_from_doctor(inter, lang), view=None)
        elif interaction.data.get('custom_id') == 'in;pay':
            await interaction.response.defer()
            payment = await hryak.requests.post_requests.pay_doctor(interaction.user.id)
            if payment.get('status') == hryak.Status.SUCCESS:
                await inter.edit_original_response(embed=payed_the_doctor(inter, lang), view=None)
            else:
                await inter.edit_original_response(embed=not_enough_money_for_doctor(inter, lang), view=None)
    elif scenario == 'dizzy':
        await send_callback(inter, embed=generate_embed(
            title=translate(Locales.ItemUsed.ate_poop_and_dizzy_title, lang),
            description=f"{translate(Locales.ItemUsed.ate_poop_and_dizzy_desc, lang)}",
            prefix=Func.generate_prefix('🍽️'),
            inter=inter,
        ), ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)
    elif scenario == 'question':
        await send_callback(inter, embed=generate_embed(
            title=translate(Locales.ItemUsed.ate_poop_and_dizzy_title, lang),
            description=f"{translate(Locales.ItemUsed.ate_poop_and_question_desc, lang)}",
            prefix=Func.generate_prefix('🍽️'),
            inter=inter,
        ), ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)
    elif scenario == 'dad':
        await send_callback(inter, embed=generate_embed(
            title=translate(Locales.ItemUsed.ate_poop_and_dad_title, lang),
            description=f"{translate(Locales.ItemUsed.ate_poop_and_dad_desc, lang)}",
            prefix=Func.generate_prefix('🍽️'),
            inter=inter,
        ), ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)


def eaten_and_poisoned(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.ItemUsed.ate_poop_and_poisoned_title, lang),
        description=f"{translate(Locales.ItemUsed.ate_poop_and_poisoned_desc, lang)}",
        prefix=Func.generate_prefix('🍽️'),
        inter=inter,
    )
    return embed


def ran_away_from_doctor(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.PoopEaten.ran_away_and_not_payed_title, lang),
        description=f"{translate(Locales.PoopEaten.ran_away_and_not_payed_desc, lang)}",
        prefix=Func.generate_prefix('🏃‍♂️'),
        inter=inter,
    )
    return embed


def payed_the_doctor(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.PoopEaten.payed_to_doctor_title, lang),
        description=f"{translate(Locales.PoopEaten.payed_to_doctor_desc, lang)}",
        prefix=Func.generate_prefix('🪙'),
        inter=inter,
    )
    return embed


def not_enough_money_for_doctor(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.PoopEaten.not_enough_money_for_doctor_title, lang),
        description=f"{translate(Locales.PoopEaten.not_enough_money_for_doctor_desc, lang)}",
        prefix=Func.generate_prefix('🪙'), inter=inter,
        color=config.error_color
    )
    return embed
