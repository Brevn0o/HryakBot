from ..core import *
from ..utils import *
from .. import modules


class PigCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(description=locale_str("feed-desc"))
    @discord.app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id,))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def feed(self, inter):
        await modules.pig.callbacks.feed(inter)

    @discord.app_commands.command(description=locale_str("butcher-desc"))
    @discord.app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id,))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def butcher(self, inter):
        await modules.pig.callbacks.butcher(inter)

    @discord.app_commands.command(description=locale_str("rename-desc"))
    @discord.app_commands.rename(name=locale_str("rename-name-name"))
    @discord.app_commands.describe(name=locale_str("rename-name-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def rename(self, inter, name: discord.app_commands.Range[str, 1, 50]):
        await modules.pig.callbacks.rename(inter, name)

    @discord.app_commands.command(description=locale_str("view-desc"))
    @discord.app_commands.rename(user=locale_str("view-user-name"))
    @discord.app_commands.describe(user=locale_str("view-user-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def view(self, inter, user: discord.User = None):
        await modules.other.callbacks.view(inter, user)


async def setup(client):
    await client.add_cog(PigCommands(client))
