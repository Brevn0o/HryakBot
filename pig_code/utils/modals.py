import discord.ui

from pig_code.core import *
from pig_code.utils import error_callbacks
from pig_code.utils.functions import translate


async def get_item_amount(inter, title, label, max_amount: int = None, delete_response: bool = False,
                          min_amount: int = 1):
    """Asks for a number and hands back (interaction, amount).

    Returns None when there is no usable answer - not a number, below min_amount, or the
    modal was opened and never submitted. Callers should check the result before unpacking
    it; anything less than min_amount is refused rather than quietly let through, because a
    zero sails through every downstream check and ends up announced as "donated 0 coins".
    An amount over what the person has is clamped instead, since that is a slip rather than
    a mistake.
    """
    lang = await User.get_language(user_id=inter.user.id)
    custom_id = f'modal;get_item_amount{random.randrange(1000)}'
    modal = discord.ui.Modal(title=title, custom_id=custom_id)
    modal.add_item(discord.ui.TextInput(
        label=label,
        placeholder=translate(Locales.Global.you_have_amount, lang, {'max_amount': max_amount}),
        custom_id="amount",
        style=discord.TextStyle.short,
        max_length=7,
        required=True
    ))
    await inter.response.send_modal(modal)
    try:
        interaction = await inter.client.wait_for(
            "interaction",
            check=lambda i: i.data.get('custom_id') == custom_id and i.user.id == inter.user.id,
            timeout=300,
        )
    except asyncio.TimeoutError:
        return None
    amount = interaction.data['components'][0]['components'][0]['value'].strip()
    if not amount.isdigit():
        await error_callbacks.modal_input_is_not_number(interaction)
        return None
    amount = int(amount)
    if amount < min_amount:
        await error_callbacks.modal_amount_too_small(interaction, min_amount)
        return None
    if max_amount is not None and amount > max_amount:
        amount = max_amount
    if delete_response:
        await interaction.response.defer(ephemeral=True)
    return interaction, amount


async def get_text(inter, title, label, placeholder: str = None, max_length: int = 32,
                   default: str = None):
    """Asks for a line of text and hands back (interaction, text).

    Same shape as get_item_amount, without the number checking - what counts as a valid
    answer differs per caller, so it is left to them. Returns None if the modal is opened
    and never submitted, so callers can just check the result instead of each of them
    having to catch the timeout.
    """
    custom_id = f'modal;get_text{random.randrange(1000)}'
    modal = discord.ui.Modal(title=title, custom_id=custom_id)
    modal.add_item(discord.ui.TextInput(
        label=label,
        placeholder=placeholder,
        default=default,
        custom_id='text',
        style=discord.TextStyle.short,
        max_length=max_length,
        required=True
    ))
    await inter.response.send_modal(modal)
    try:
        interaction = await inter.client.wait_for(
            'interaction',
            check=lambda i: i.data.get('custom_id') == custom_id and i.user.id == inter.user.id,
            timeout=300,
        )
    except asyncio.TimeoutError:
        return None
    return interaction, interaction.data['components'][0]['components'][0]['value']


async def get_amount_of_hollars_to_donate(inter, delete_response: bool = False):
    lang = await User.get_language(user_id=inter.user.id)
    modal = discord.ui.Modal(title=translate(Locales.PremiumShop.get_amount_of_hollars_modal_title, lang),
                             custom_id='get_amount_of_hollars_to_donate')
    modal.add_item(discord.ui.TextInput(
        label=translate(Locales.PremiumShop.get_amount_of_hollars_modal_label, lang),
        placeholder=translate(Locales.PremiumShop.get_amount_of_hollars_modal_placeholder, lang),
        custom_id="amount",
        style=discord.TextStyle.short,
        max_length=7,
        required=True
    ))
    await inter.response.send_modal(modal)
    interaction = await inter.client.wait_for(
        "interaction",
        check=lambda i: i.data.get('custom_id') == "get_amount_of_hollars_to_donate" and i.user.id == inter.user.id,
        timeout=300,
    )
    amount = interaction.data['components'][0]['components'][0]['value']
    if not amount.isdigit():
        await error_callbacks.modal_input_is_not_number(inter)
        return False
    if delete_response:
        await interaction.response.defer(ephemeral=True)
        # await interaction.delete_original_response()
    return interaction, int(amount)
