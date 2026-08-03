from hryak import Status
from ...utils import *
from . import embeds, components
from ...utils.discord_utils import send_callback
from ...core import *


async def feed(inter):
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.post_requests.feed_guild_pig(inter.user.id, inter.guild.id)
    if response['status'] == hryak.statuses.Status.NOT_READY:
        await send_callback(inter, embed=await embeds.not_ready(inter, lang, response),
                            ephemeral=True, edit_original_response=False)
        return
    if response['status'] != hryak.statuses.Status.SUCCESS:
        return
    await send_callback(inter, embed=await embeds.fed(inter, lang, inter.guild.id, response),
                        ephemeral=True, edit_original_response=False)
    await update_message(inter.client, inter.guild.id)


async def help_(inter):
    await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    await send_callback(inter, embed=await embeds.help_(inter, lang),
                        ephemeral=True, edit_original_response=False)


async def top(inter, pre_command_check: bool = True, ephemeral: bool = False):
    """From the command it replies normally; from the pig's menu it answers ephemerally,
    so the shared message is left alone."""
    if pre_command_check:
        await DisUtils.pre_command_check(inter)
    else:
        await User.register_user_if_not_exists(inter.user.id)
    lang = await User.get_language(inter.user.id)
    response = await hryak.requests.top_requests.top_weight_guilds(inter.guild.id, lang)
    await send_callback(inter, embed=await embeds.top(inter, lang, response),
                        ephemeral=ephemeral, edit_original_response=not ephemeral)


async def update_message(client, guild_id):
    """Redraws the pig's message in place. Returns False if there is nothing to redraw."""
    lang = await Guild.get_language(guild_id)
    channel_id = await GuildPig.get_channel(guild_id)
    message_id = await GuildPig.get_message(guild_id)
    if channel_id is None or message_id is None:
        return False
    channel = client.get_channel(int(channel_id))
    if channel is None:
        return False
    try:
        message = await channel.fetch_message(int(message_id))
        await message.edit(embed=await embeds.pig_message(guild_id, lang),
                           view=components.pig_message(lang))
    except discord.errors.HTTPException:
        return False
    return True


async def update_all_messages(client, delay: float = .5):
    """Redraws every server pig's message, so a guild is never left showing stale numbers.

    Only guilds that actually set a pig up are walked, and there is a pause between them -
    edits share the same rate limiter as everything else the bot sends.
    """
    updated = 0
    for guild_id in await GuildPig.get_all_setup_guilds():
        if await update_message(client, guild_id):
            updated += 1
        await asyncio.sleep(delay)
    return updated


async def remove_old_home(inter, new_channel):
    old_channel_id = await GuildPig.get_channel(inter.guild.id)
    if old_channel_id is None:
        return
    old_channel = inter.guild.get_channel(int(old_channel_id))
    if old_channel is None:
        return

    old_message_id = await GuildPig.get_message(inter.guild.id)
    if old_message_id is not None:
        try:
            message = await old_channel.fetch_message(int(old_message_id))
            await message.delete()
        except discord.errors.HTTPException:
            pass

    if old_channel.id != new_channel.id and await GuildPig.is_channel_created_by_bot(inter.guild.id):
        try:
            await old_channel.delete()
        except discord.errors.HTTPException:
            pass


async def setup(inter, channel: discord.TextChannel = None):
    await DisUtils.pre_command_check(inter, language_check=False)
    lang = await User.get_language(inter.user.id)
    await Guild.register_guild_if_not_exists(inter.guild.id, Func.guess_guild_language(inter.guild, inter.user))

    if channel is None and not inter.guild.me.guild_permissions.manage_channels:
        await send_callback(inter, embed=await embeds.no_permissions(inter, lang))
        return

    created_channel = None
    try:
        if channel is None:
            channel = created_channel = await inter.guild.create_text_channel(
                name=f'🐷・hryak')
        await channel.set_permissions(inter.guild.default_role, send_messages=False)
        await channel.set_permissions(inter.guild.me, view_channel=True, send_messages=True, embed_links=True)
        guild_lang = await Guild.get_language(inter.guild.id)
        message = await channel.send(embed=await embeds.pig_message(inter.guild.id, guild_lang),
                                     view=components.pig_message(guild_lang))
    except (discord.errors.Forbidden, discord.errors.HTTPException):
        if created_channel is not None:
            try:
                await created_channel.delete()
            except discord.errors.HTTPException:
                pass
        await send_callback(inter, embed=await embeds.no_permissions(inter, lang, channel))
        return

    await remove_old_home(inter, channel)
    await GuildPig.set_channel(inter.guild.id, channel.id, created_by_bot=created_channel is not None)
    await GuildPig.set_message(inter.guild.id, message.id)
    await send_callback(inter, embed=await embeds.setup(inter, lang, channel))
