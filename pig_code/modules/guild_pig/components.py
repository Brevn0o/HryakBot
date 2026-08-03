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


def actions(lang) -> discord.ui.Select:
    """Everything the pig can do beyond being fed. Each option answers ephemerally, so
    the shared message is never edited by someone poking at the menu."""
    return discord.ui.Select(custom_id='guild_pig;action',
                             placeholder=translate(Locales.GuildPig.actions_placeholder, lang),
                             options=[
                                 discord.SelectOption(value='top',
                                                      label=translate(Locales.GuildPig.top_title, lang),
                                                      emoji='🐖'),
                             ])
