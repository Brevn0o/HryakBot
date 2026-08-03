from ..core.items.item_components import item_components
from ..utils import *
from .. import modules
from ..core import *


from ..utils.discord_utils import send_callback, generate_embed


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        aiocache.Cache(Cache.MEMORY)
        if not config.TEST:
            Func.clear_folder(config.TEMP_FOLDER_PATH)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is ready: {self.client.user}')
        if not os.path.exists(config.TEMP_FOLDER_PATH):
            os.makedirs(config.TEMP_FOLDER_PATH)
        print('> Temp folder is created')
        await item_components.build_item_components()
        print('> Item components are built')
        await Setup.create_guild_table()
        await Setup.create_user_table()
        await Setup.create_shop_table()
        await Setup.create_promo_code_table()
        print('> Tables are created')
        await Guild.register([(guild.id, Func.guess_guild_language(guild)) for guild in self.client.guilds])
        print('> Guilds are registered')
        await Pig.fix_pig_structure_for_all_users()
        print('> Pig structures are fixed')
        await Stats.fix_stats_structure_for_all_users()
        print('> Stats structures are fixed')
        await History.fix_history_structure_for_all_users()
        print('> History structures are fixed')
        await User.fix_settings_structure_for_all_users()
        print('> User settings structures are fixed')
        for guild_id in [*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS]:
            try:
                await self.client.tree.sync(guild=discord.Object(id=guild_id))
            except discord.errors.Forbidden:
                pass
        print('> Admin guilds are synced')
        await self.client.tree.sync()
        print('> Tree is synced')
        print(f'> Server pig messages are updated: '
              f'{await modules.guild_pig.callbacks.update_all_messages(self.client)}')

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        await User.register_user_if_not_exists(interaction.user.id)
        if interaction.type == discord.InteractionType.application_command:
            command_name, options = Func.get_command_name_and_options(interaction)
            is_dm = True if interaction.guild is None else False
            await hryak.Func.add_log('command_used',
                         user_name=str(interaction.user),
                         user_id=interaction.user.id,
                         guild_name=str(interaction.guild) if not is_dm else None,
                         guild_id=interaction.guild.id if not is_dm else None,
                         channel_name=str(interaction.channel) if not is_dm else 'DM',
                         channel_id=interaction.channel.id,
                         command=command_name,
                         options=options)
        if interaction.type == discord.InteractionType.component:
            custom_id_params = interaction.data.get('custom_id').split(';') if interaction.data.get(
                'custom_id') is not None else []
            interaction_values = interaction.data.get('values')
            if custom_id_params and custom_id_params[0] == 'in':
                return
            allowed_users = []
            lang = await User.get_language(interaction.user.id)
            if custom_id_params and custom_id_params[0] == 'trade':
                trade_id = None
                if custom_id_params[1] == 'add':
                    trade_id = interaction_values[0].split(';')[1]
                elif custom_id_params[1] in ['agree', 'cancel', 'clear', 'add_item', 'tax_split_1', 'tax_split_2',
                                             'tax_split_equal']:
                    trade_id = custom_id_params[2]
                user1_id = await Trade.get_user(interaction.client, trade_id, 0, fetch=False)
                user2_id = await Trade.get_user(interaction.client, trade_id, 1, fetch=False)
                allowed_users.append(int(user1_id))
                allowed_users.append(int(user2_id))
            if interaction.message is not None and interaction.message.interaction is not None:
                if not DisUtils.check_if_right_user(interaction, except_users=allowed_users):
                    await error_callbacks.wrong_component_clicked(interaction)
                    return
            if custom_id_params:
                if custom_id_params[0] == 'trade':
                    if custom_id_params[1] == 'add':
                        interaction_values_params = interaction_values[0].split(';')
                        action_object = interaction_values_params[0]
                        trade_id = interaction_values_params[1]
                        user1 = await Trade.get_user(interaction.client, trade_id, 0)
                        user2 = await Trade.get_user(interaction.client, trade_id, 1)
                        if action_object in ['coins', 'hollars']:
                            modal_interaction, amount = await modals.get_item_amount(interaction,
                                                                                     translate(
                                                                                         Locales.Trade.add_item_modal_title,
                                                                                         lang),
                                                                                     translate(
                                                                                         Locales.Trade.add_item_with_tax_modal_label,
                                                                                         lang, {
                                                                                             'tax': await hryak.GameFunc.get_user_tax_percent(
                                                                                                 interaction.user.id,
                                                                                                 action_object),
                                                                                             'item_name': await Item.get_name(
                                                                                                 action_object, lang)}),
                                                                                     max_amount=await Item.get_amount(
                                                                                         action_object,
                                                                                         interaction.user.id) - await Trade.get_item_amount(
                                                                                         trade_id, interaction.user.id,
                                                                                         action_object),
                                                                                     delete_response=True
                                                                                     )
                            if amount is False:
                                return
                            await Trade.add_item(trade_id, modal_interaction.user.id, action_object, amount)
                            await modules.trade.callbacks.trade(modal_interaction,
                                                                user1,
                                                                user2,
                                                                trade_id=trade_id,
                                                                pre_command_check=False)
                        if action_object == 'inventory':
                            await modules.inventory.callbacks.inventory(interaction, pre_command_check=False,
                                                                        select_item_component_id=f'trade;add_item;{trade_id}',
                                                                        ephemeral=True, edit_original_response=False,
                                                                        tradable_items_only=True)
                        if action_object == 'wardrobe':
                            await modules.inventory.callbacks.wardrobe(interaction, pre_command_check=False,
                                                                       select_item_component_id=f'trade;add_item;{trade_id}',
                                                                       ephemeral=True, edit_original_response=False,
                                                                       tradable_items_only=True)
                    elif custom_id_params[1] in ['agree', 'cancel', 'clear', 'add_item', 'tax_split_1', 'tax_split_2',
                                                 'tax_split_equal']:
                        trade_id = custom_id_params[2]
                        user1_id = await Trade.get_user(interaction.client, trade_id, 0, fetch=False)
                        user2_id = await Trade.get_user(interaction.client, trade_id, 1, fetch=False)
                        if custom_id_params[1] == 'agree':
                            await interaction.response.defer()
                            await Trade.set_agree(trade_id, interaction.user.id,
                                            True if not await Trade.is_agree(trade_id, interaction.user.id) else False)
                            await modules.trade.callbacks.trade(interaction,
                                                                await Trade.get_user(interaction.client, trade_id, 0),
                                                                await Trade.get_user(interaction.client, trade_id, 1),
                                                                trade_id=trade_id,
                                                                pre_command_check=False)
                        elif custom_id_params[1] == 'cancel':
                            await error_callbacks.default_error_callback(interaction,
                                                                         translate(Locales.Trade.cancel_title, lang),
                                                                         translate(Locales.Trade.cancel_desc,
                                                                                   lang).format(
                                                                             user=interaction.user.display_name),
                                                                         thumbnail_url=await hryak.Func.get_image_path_from_link(
                                                                             config.image_links['trade']))
                        elif custom_id_params[1] == 'clear':
                            await interaction.response.defer()
                            await Trade.set_agree(trade_id, user1_id, False)
                            await Trade.set_agree(trade_id, user2_id, False)
                            await Trade.clear_items(trade_id, interaction.user.id)
                            await modules.trade.callbacks.trade(interaction,
                                                                await Trade.get_user(interaction.client, trade_id, 0),
                                                                await Trade.get_user(interaction.client, trade_id, 1),
                                                                trade_id=trade_id,
                                                                pre_command_check=False)
                        elif custom_id_params[1] == 'add_item':
                            action_object = interaction_values[0].split(';')[0]
                            modal_interaction, amount = await modals.get_item_amount(interaction,
                                                                                     translate(
                                                                                         Locales.Trade.add_item_modal_title,
                                                                                         lang),
                                                                                     translate(
                                                                                         Locales.Trade.add_item_modal_label,
                                                                                         lang, {'item': await Item.get_name(
                                                                                             action_object, lang)}),
                                                                                     max_amount=await Item.get_amount(
                                                                                         action_object,
                                                                                         interaction.user.id) - await Trade.get_item_amount(
                                                                                         trade_id, interaction.user.id,
                                                                                         action_object),
                                                                                     delete_response=True
                                                                                     )
                            if amount is False:
                                return
                            await interaction.delete_original_response()
                            await Trade.add_item(trade_id, modal_interaction.user.id, action_object, amount)
                            await Trade.set_agree(trade_id, user1_id, False)
                            await Trade.set_agree(trade_id, user2_id, False)
                            await modules.trade.callbacks.trade(interaction,
                                                                await Trade.get_user(modal_interaction.client, trade_id,
                                                                                     0),
                                                                await Trade.get_user(modal_interaction.client, trade_id,
                                                                                     1),
                                                                trade_id=trade_id,
                                                                pre_command_check=False)

                        elif custom_id_params[1] in ['tax_split_1', 'tax_split_2', 'tax_split_equal']:
                            await interaction.response.defer()
                            await Trade.set_tax_splitting_vote(trade_id, interaction.user.id, custom_id_params[1])
                            await modules.trade.callbacks.trade(interaction,
                                                                await Trade.get_user(interaction.client, trade_id, 0),
                                                                await Trade.get_user(interaction.client, trade_id, 1),
                                                                trade_id=trade_id,
                                                                pre_command_check=False)
                if custom_id_params[0] == 'guild_pig':
                    if custom_id_params[1] == 'feed':
                        await modules.guild_pig.callbacks.feed(interaction)
                    elif custom_id_params[1] == 'help':
                        await modules.guild_pig.callbacks.help_(interaction)
                    elif custom_id_params[1] == 'action':
                        if interaction_values[0] == 'top':
                            await modules.guild_pig.callbacks.top(interaction, pre_command_check=False,
                                                                  ephemeral=True)
                    return
                if custom_id_params[0] in ['like', 'dislike']:
                    if custom_id_params[0] == 'like':
                        await User.append_rate(custom_id_params[1], interaction.user.id, 1)
                    elif custom_id_params[0] == 'dislike':
                        await User.append_rate(custom_id_params[1], interaction.user.id, -1)
                    await modules.other.callbacks.profile(interaction,
                                                          await User.get_discord_user(interaction.client, custom_id_params[1]),
                                                          pre_command_check=False)
                elif custom_id_params[0] == 'view_profile':
                    await modules.other.callbacks.profile(interaction,
                                                          await User.get_discord_user(self.client, interaction_values[0]),
                                                          edit_original_response=False, ephemeral=True,
                                                          pre_command_check=False)
                if custom_id_params[0] == 'item_select':
                    await interaction.response.defer()
                    if custom_id_params[1] == 'inventory':
                        await modules.inventory.callbacks.inventory_item_selected(interaction, interaction_values[0],
                                                                                  category=custom_id_params[2],
                                                                                  page=int(custom_id_params[3]))
                    elif custom_id_params[1] == 'wardrobe':
                        await modules.inventory.callbacks.wardrobe_item_selected(interaction, interaction_values[0],
                                                                                 category=custom_id_params[2],
                                                                                 page=int(custom_id_params[3]))
                    elif custom_id_params[1] == 'shop':
                        await modules.shop.callbacks.shop_item_selected(interaction, interaction_values[0],
                                                                        category=custom_id_params[2],
                                                                        page=int(custom_id_params[3]))
                if custom_id_params[0] == 'back_to_inventory':
                    if custom_id_params[1] == 'inventory':
                        await modules.inventory.callbacks.inventory(interaction, init_category=custom_id_params[2],
                                                                    init_page=int(custom_id_params[3]))
                    elif custom_id_params[1] == 'wardrobe':
                        await modules.inventory.callbacks.wardrobe(interaction, init_category=custom_id_params[2],
                                                                   init_page=int(custom_id_params[3]))
                    elif custom_id_params[1] == 'shop':
                        await modules.shop.callbacks.shop(interaction, init_category=custom_id_params[2],
                                                          init_page=int(custom_id_params[3]))
                if custom_id_params[0] == 'move_to':
                    if custom_id_params[1] == 'shop':
                        await modules.shop.callbacks.shop(interaction, init_category=interaction_values[0],
                                                          init_page=0)
                if custom_id_params[0] == 'donate':
                    await modules.shop.callbacks.donation_page_selected(interaction, interaction_values[0])
                elif custom_id_params[0] == 'preview_skin':
                    await modules.other.callbacks.skin_preview(interaction, custom_id_params[1])
                elif custom_id_params[0] == 'buy':
                    await modules.shop.callbacks.shop_item_buy(interaction, custom_id_params[1])
                elif custom_id_params[0] == 'wear_skin':
                    await modules.inventory.callbacks.wardrobe_item_wear(interaction, custom_id_params[1],
                                                                         category=custom_id_params[2],
                                                                         page=int(custom_id_params[3]))
                elif custom_id_params[0] == 'remove_skin':
                    await modules.inventory.callbacks.wardrobe_item_remove(interaction, custom_id_params[1],
                                                                           category=custom_id_params[2],
                                                                           page=int(custom_id_params[3]))
                elif len(custom_id_params) > 1 and custom_id_params[1] in item_components.item_components and custom_id_params[0] in \
                        item_components.item_components[custom_id_params[1]]:
                    async def update_inventory(edit_followup: bool = False):
                        if await Item.get_amount(custom_id_params[1], interaction.user.id) == 0:
                            if await Item.get_inventory_type(custom_id_params[1]) == 'wardrobe':
                                await modules.inventory.callbacks.wardrobe(interaction, edit_followup=edit_followup,
                                                                           init_category=custom_id_params[2],
                                                                           init_page=int(custom_id_params[3]))
                            elif await Item.get_inventory_type(custom_id_params[1]) == 'inventory':
                                await modules.inventory.callbacks.inventory(interaction, edit_followup=edit_followup,
                                                                            init_category=custom_id_params[2],
                                                                            init_page=int(custom_id_params[3]))
                        else:
                            await modules.inventory.callbacks.inventory_item_selected(interaction, custom_id_params[1],
                                                                                      edit_followup=edit_followup)

                    if await Item.get_amount(custom_id_params[1], interaction.user.id) <= 0:
                        await error_callbacks.no_item(interaction, custom_id_params[1], edit_original_response=False,
                                                      ephemeral=True,
                                                      thumbnail_url=await Item.get_image_path(custom_id_params[1], config.TEMP_FOLDER_PATH))
                        await update_inventory()
                        return
                    result = await item_components.item_components[custom_id_params[1]][custom_id_params[0]]['func'](interaction,
                                                                                                     custom_id_params[
                                                                                                         1],
                                                                                                     update_inventory)
                    if result is None:
                        result = {}
                    if 'callback' in item_components.item_components[custom_id_params[1]][custom_id_params[0]]:
                        embed = generate_embed(
                            title=translate(
                                item_components.item_components[custom_id_params[1]][custom_id_params[0]]['callback']['title'],
                                lang),
                            description=translate(
                                item_components.item_components[custom_id_params[1]][custom_id_params[0]]['callback']['description'],
                                lang,
                                format_options=result),
                            prefix=Func.generate_prefix(
                                item_components.item_components[custom_id_params[1]][custom_id_params[0]]['callback']['prefix']),
                            inter=interaction,
                        )
                        await send_callback(interaction, embed=embed,
                                            ephemeral=True, edit_original_response=False)
                        await update_inventory(edit_followup=True)
                elif custom_id_params[0] == 'hide':
                    await interaction.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == config.BOT_HALYAVA_CHANNEL:
            if payload.emoji.name == '✅' and payload.member.id in config.HALYAVERS:
                reward_item_id, amount = random.choice([('coins', [80, 120]),
                                                        ('common_case', [1, 1]),
                                                        ('barbecue', [3, 5]),
                                                        ('poop', [80, 120])])
                amount[1] += 1
                amount = random.randrange(*amount)
                if datetime.datetime.now().day in [1, 2, 3]:
                    amount *= 2
                message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
                await User.add_item(message.author.id, reward_item_id, amount)
                await message.reply(
                    f'{await Item.get_emoji(reward_item_id)}・*Выдана награда: **{await Item.get_name(reward_item_id, 'ru')}** x{amount}*')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id in config.BOT_GUILDS:
            if member.guild.id == config.BOT_GUILDS[config.EN_BOT_GUILD_ID]:
                if await User.get_language(member.id) in ['ru']:
                    await member.kick(reason='Russian')
            if 'not_verified_role' in config.BOT_GUILDS[member.guild.id]:
                await User.register_user_if_not_exists(member.id)
                if (await Pig.get_weight(member.id) < 1.5 and await User.get_age(member.id) < 3600) or \
                        (hryak.Func.generate_current_timestamp() - member.created_at.timestamp() < 30 * 24 * 3600):
                    await member.add_roles(
                        member.guild.get_role(config.BOT_GUILDS[member.guild.id]['not_verified_role']))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await Guild.register_guild_if_not_exists(guild.id, Func.guess_guild_language(guild))
        await guild.chunk()
        await hryak.Func.add_log('guild_join',
                     owner_id=guild.owner_id,
                     guild_name=str(guild),
                     guild_id=guild.id,
                     members=guild.member_count)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await hryak.Func.add_log('guild_remove',
                     owner_id=guild.owner_id,
                     guild_name=str(guild),
                     guild_id=guild.id,
                     members=guild.member_count)


async def setup(client):
    await client.add_cog(Events(client))
