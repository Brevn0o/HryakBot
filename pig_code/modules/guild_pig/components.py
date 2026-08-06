from ...utils import *
from ...core import *


def pig_message(lang) -> discord.ui.View:
    """The buttons that live on the pig's message.

    No ids are baked into the custom_id - the message only ever sits in the guild it
    belongs to, so the handler reads the guild off the interaction. timeout=None because
    this message outlives restarts; the interactions are dispatched from on_interaction,
    which does not need the view to still be held in memory.
    """
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(custom_id='guild_pig;feed',
                                    style=discord.ButtonStyle.green,
                                    label=translate(Locales.GuildPig.feed_btn, lang),
                                    emoji='🌾'))
    view.add_item(discord.ui.Button(custom_id='guild_pig;help',
                                    style=discord.ButtonStyle.gray,
                                    label=translate(Locales.GuildPig.help_btn, lang)))
    view.add_item(actions(lang))
    return view


def admin_message(lang) -> discord.ui.View:
    """Everything staff can do to the pig from the panel.

    Same reasoning as the pig's message - no ids in the custom_id, timeout=None because it
    outlives restarts and is dispatched from on_interaction.
    """
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Select(
        custom_id='guild_pig;admin',
        placeholder=translate(Locales.GuildPigAdmin.actions_placeholder, lang),
        options=[
            discord.SelectOption(value='rename',
                                 label=translate(Locales.GuildPigAdmin.rename_btn, lang),
                                 description=Func.cut_text(
                                     translate(Locales.GuildPigAdmin.rename_btn_desc, lang), 100),
                                 emoji='✏️'),
            discord.SelectOption(value='language',
                                 label=translate(Locales.GuildPigAdmin.language_btn, lang),
                                 description=Func.cut_text(
                                     translate(Locales.GuildPigAdmin.language_btn_desc, lang), 100),
                                 emoji='🌍'),
            discord.SelectOption(value='withdraw',
                                 label=translate(Locales.GuildPigAdmin.withdraw_btn, lang),
                                 description=Func.cut_text(
                                     translate(Locales.GuildPigAdmin.withdraw_btn_desc, lang), 100),
                                 emoji='🏦'),
        ]))
    return view


def choose_language(custom_id, lang) -> discord.ui.Select:
    """The languages hryak speaks, for picking the server's.

    custom_id starts with 'in;' so on_interaction leaves it alone - the caller is sitting on
    a wait_for, the same way the pagination and part-picking selects work.
    """
    return discord.ui.Select(
        custom_id=custom_id,
        placeholder=translate(Locales.GuildPigAdmin.language_placeholder, lang),
        options=[discord.SelectOption(value=code, label=bot_locale.full_names[code])
                 for code in bot_locale.valid_discord_locales])


async def inventory_item_selected(guild_id, item_id, lang, category: str = None, page: int = 1) -> list:
    """The buttons on one of the pig's things.

    Same as a person's wardrobe, except pressing one opens a vote rather than doing it -
    hence the separate custom_ids. Non-skins have nothing to press yet; they still get the
    way back.
    """
    components = []
    if await Item.get_type(item_id) == 'skin':
        if await GuildPig.is_skin_worn(guild_id, item_id):
            components.append(discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label=translate(Locales.Global.remove_cloth, lang),
                custom_id=f'server_remove_skin;{item_id};{category};{page}',
            ))
        else:
            components.append(discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label=translate(Locales.Global.wear, lang),
                custom_id=f'server_wear_skin;{item_id};{category};{page}',
            ))
        components.append(discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label=translate(Locales.Global.preview, lang),
            custom_id=f'preview_skin;{item_id};{category};{page};server',
        ))
    components.append(discord.ui.Button(
        style=discord.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory;server_inventory;{category};{page}',
    ))
    return components


def actions(lang) -> discord.ui.Select:
    """Everything the pig can do beyond being fed. Each option answers ephemerally, so
    the shared message is never edited by someone poking at the menu."""
    return discord.ui.Select(custom_id='guild_pig;action',
                             placeholder=translate(Locales.GuildPig.actions_placeholder, lang),
                             options=[
                                 discord.SelectOption(value='donate',
                                                      label=translate(Locales.GuildPig.donate_btn, lang),
                                                      emoji='🪙'),
                                 discord.SelectOption(value='inventory',
                                                      label=translate(Locales.GuildPig.inventory_btn, lang),
                                                      emoji='🎒'),
                                 discord.SelectOption(value='shop',
                                                      label=translate(Locales.GuildPig.shop_btn, lang),
                                                      emoji='🛍️'),
                                 discord.SelectOption(value='top',
                                                      label=translate(Locales.GuildPig.top_btn, lang),
                                                      emoji='🐖'),
                             ])
