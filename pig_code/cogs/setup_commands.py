from ..core import *
from ..utils import *
from .. import modules


class SetupCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(description=locale_str("language-desc"))
    @discord.app_commands.rename(language=locale_str("language-language-name"))
    @discord.app_commands.describe(language=locale_str("language-language-desc"))
    @discord.app_commands.choices(language=[discord.app_commands.Choice(name=bot_locale.full_names[i], value=i) for i in
                                            bot_locale.valid_discord_locales])
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def language(self, inter, language: str):
        await modules.other.callbacks.set_language(inter, language)

    settings = discord.app_commands.Group(name="settings", description='-')

    @settings.command(description=locale_str("settings-say-desc"))
    @discord.app_commands.rename(allow=locale_str("settings-say-allow-name"))
    @discord.app_commands.describe(allow=locale_str("settings-say-allow-desc"))
    @discord.app_commands.choices(allow=[
        discord.app_commands.Choice(name=locale_str('choice-true'), value='true'),
        discord.app_commands.Choice(name=locale_str('choice-false'), value='false')
    ])
    @discord.app_commands.checks.has_permissions(administrator=True)
    @discord.app_commands.guild_install()
    @commands.guild_only()
    async def say(self, inter, allow: str):
        await modules.other.callbacks.settings_say(inter, Func.str_to_bool(allow))

    @settings.command(description=locale_str("settings-top-desc"))
    @discord.app_commands.rename(participate=locale_str("settings-top-participate-name"))
    @discord.app_commands.describe(participate=locale_str("settings-top-participate-desc"))
    @discord.app_commands.choices(participate=[
        discord.app_commands.Choice(name=locale_str('choice-true'), value='true'),
        discord.app_commands.Choice(name=locale_str('choice-false'), value='false')
    ])
    @discord.app_commands.guild_install()
    @discord.app_commands.guild_install()
    async def top(self, inter, participate: str):
        await modules.other.callbacks.settings_top(inter, Func.str_to_bool(participate))

    server = discord.app_commands.Group(name="server", description='-')

    @server.command(name="top", description=locale_str("server-top-desc"))
    @discord.app_commands.guild_install()
    @commands.guild_only()
    async def server_top(self, inter):
        await modules.guild_pig.callbacks.top(inter)

    @discord.app_commands.command(name="setup", description=locale_str("setup-desc"))
    @discord.app_commands.rename(channel=locale_str("setup-channel-name"))
    @discord.app_commands.describe(channel=locale_str("setup-channel-desc"))
    @discord.app_commands.rename(poll_channel=locale_str("setup-polls-name"))
    @discord.app_commands.describe(poll_channel=locale_str("setup-polls-desc"))
    @discord.app_commands.rename(notification_channel=locale_str("setup-notifications-name"))
    @discord.app_commands.describe(notification_channel=locale_str("setup-notifications-desc"))
    @discord.app_commands.rename(admin_channel=locale_str("setup-admin-name"))
    @discord.app_commands.describe(admin_channel=locale_str("setup-admin-desc"))
    @discord.app_commands.checks.has_permissions(manage_guild=True)
    @discord.app_commands.guild_install()
    @commands.guild_only()
    async def pig_setup(self, inter, channel: discord.TextChannel = None,
                        poll_channel: discord.TextChannel = None,
                        notification_channel: discord.TextChannel = None,
                        admin_channel: discord.TextChannel = None):
        await modules.guild_pig.callbacks.setup(inter, channel, poll_channel,
                                                notification_channel, admin_channel)


async def setup(client):
    await client.add_cog(SetupCommands(client))
