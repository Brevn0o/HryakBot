import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def breed(inter, partner):
    await BotUtils.pre_command_check(inter)
    BotUtils.raise_if_language_not_supported(inter.author.id)
    User.register_user_if_not_exists(partner.id)
    Pig.create_pig_if_no_pig(partner.id)
    BotUtils.check_pig_breed_cooldown(inter.author)
    BotUtils.check_pig_breed_cooldown(partner)
    lang = User.get_language(inter.author.id)
    min_weight_to_breed = 50
    if partner == inter.author:
        raise BreedWithYourself
    if partner.bot is True:
        raise BotAsPartnerBreed
    if Pig.get_weight(inter.author.id) < min_weight_to_breed:
        await BotUtils.send_callback(inter, embed=embeds.pig_is_too_small_for_breed(inter, lang, inter.author, min_weight_to_breed))
        return
    if Pig.get_weight(partner.id) < min_weight_to_breed:
        await BotUtils.send_callback(inter, embed=embeds.pig_is_too_small_for_breed(inter, lang, partner, min_weight_to_breed))
        return
    message = await BotUtils.send_callback(inter,
                                           embed=embeds.personal_breed_invite(inter, lang, partner),
                                           components=components.invite_components(lang))
    def check(interaction):
        if message is not None:
            right_message = message.id == interaction.message.id
            return right_message and partner.id == interaction.author.id

    try:
        interaction = await inter.client.wait_for('button_click', check=check, timeout=120)
    except asyncio.exceptions.TimeoutError:
        await BotUtils.send_callback(message, embed=embeds.breed_canceled(inter, lang, partner, 'no_response'))
        return
    if interaction.component.custom_id == 'in:accept':
        await interaction.response.defer(ephemeral=True)
        mini_pig_chances = {'fail': 50,
                            # 'pet_hryak_default': (Pig.get_weight(inter.author.id) + Pig.get_weight(partner.id)) / 1.5
                            }
        mini_pig = Func.random_choice_with_probability(mini_pig_chances)
        Pig.set_last_breed(inter.author.id, Func.get_current_timestamp())
        Pig.set_last_breed(partner.id, Func.get_current_timestamp())
        if mini_pig == 'fail':
            await BotUtils.send_callback(inter, embed=embeds.pig_breed_fail(inter, lang, partner))
        else:
            Pig.make_pregnant(partner.id, partner.id, mini_pig)
            await BotUtils.send_callback(inter, embed=embeds.pig_breed_ok(inter, lang, partner, mini_pig))
    elif interaction.component.custom_id == 'in:reject':
        await BotUtils.send_callback(interaction, embed=embeds.breed_canceled(inter, lang, partner, 'partner_reject'))

async def pregnancy(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.pregnancy(inter, lang))