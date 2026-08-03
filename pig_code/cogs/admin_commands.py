from ..utils import *
from ..core import *

from hryak.db_api import PromoCode

from ..utils.discord_utils import send_callback, generate_embed


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(description='Check if the bot is ready')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def test(self, inter):
        await DisUtils.pre_command_check(inter, owner_only=True)

        order = hryak.functions.Lava.create_order(inter.user.id, 'hollars', 100, currency='RUB')
        link = ''
        await send_callback(inter, f'*Link: {order}*')

    @discord.app_commands.command(description='Check if the bot is ready')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def is_ready(self, inter):
        await DisUtils.pre_command_check(inter, owner_only=True)
        if self.client.is_ready():
            await send_callback(inter, f'*{self.client.user} is ready*')
        else:
            await send_callback(inter, f'*{self.client.user} is not ready*')

    @discord.app_commands.command(description='Sync the tree')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def sync_tree(self, inter):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await self.client.tree.sync()
        for guild_id in config.ADMIN_GUILDS + config.TEST_GUILDS + config.PUBLIC_TEST_GUILDS:
            try:
                await self.client.tree.sync(guild=discord.Object(guild_id))
            except:
                pass
        await send_callback(inter, f'*Tree is synced*')

    @discord.app_commands.command(description='Block user from using the bot')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def block(self, inter, user: discord.User, reason: str = None):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await User.register_user_if_not_exists(user.id)
        await User.set_block(user.id, True)
        await User.set_block_reason(user.id, reason)
        await send_callback(inter, f'*User **{user}** has been blocked*')

    @discord.app_commands.command(description='Unblock user from using the bot')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def unblock(self, inter, user: discord.User):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await User.register_user_if_not_exists(user.id)
        await User.set_block(user.id, False)
        await User.set_block_reason(user.id, '')
        await send_callback(inter, f'*User **{user}** has been unblocked*')

    @discord.app_commands.command(description='Get amount of possible skin variations')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def skin_variations(self, inter):
        await DisUtils.pre_command_check(inter, owner_only=True)
        variations = await hryak.GameFunc.get_number_of_possible_skin_variations()
        await send_callback(inter, f'*There are **{variations:,}** possible skin variations*')

    @discord.app_commands.command(description='Add item to user\'s inventory')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def add_item(self, inter, user: discord.User, item_id: str, amount: int = 1):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await User.register_user_if_not_exists(user.id)
        if not await Item.exists(item_id):
            await send_callback(inter, "*Item doesn't exist*")
        else:
            await User.add_item(user.id, item_id, amount)
            await send_callback(inter, f'*User **{user}** received **{item_id} x{amount}***')

    @add_item.autocomplete('item_id')
    async def autocomplete_item_id(self, interaction, current: str):
        return [discord.app_commands.Choice(name=i, value=i) for i in
                difflib.get_close_matches(current, await Tech.get_all_items(), n=25, cutoff=0.1)]

    @discord.app_commands.command(description='Add weight to user')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def add_weight(self, inter, user: discord.User, amount: int = 1):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await Pig.add_weight(user.id, amount)
        await send_callback(inter, f'*User **{user}** received **{amount} kg***')

    @discord.app_commands.command(description='Set Order Status')
    @discord.app_commands.choices(status=[
        discord.app_commands.Choice(name='success', value='success'),
        discord.app_commands.Choice(name='in_process', value='in_process'),
        discord.app_commands.Choice(name='failed', value='failed')
    ])
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS])
    async def set_order_status(self, inter, order_id: str,
                               status: str):
        await DisUtils.pre_command_check(inter)
        await Order.set_status(order_id, status)
        await send_callback(inter, f'*Order **{order_id}** status has been set to **{status}***')

    @discord.app_commands.command(description='Add all available skins to user')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def add_all_skins(self, inter,
                            user: discord.User):
        await DisUtils.pre_command_check(inter, owner_only=True)
        if user is None:
            user = inter.user
        await User.register_user_if_not_exists(user.id)
        for item in await Tech.get_all_items((('type', 'skin'),)):
            await User.set_item_amount(user.id, item, 1)
        await send_callback(inter, f'*User **{user}** received all available skins*')

    @discord.app_commands.command(description='Update shop')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def update_shop(self, inter):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await Shop.update()
        await send_callback(inter, f'*Shop updated*')

    @discord.app_commands.command(description='Transfer User Data')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def transfer_account(self, inter, from_user: discord.User, to_user: discord.User, overwrite: bool = False):
        await DisUtils.pre_command_check(inter, owner_only=True)
        print(await User.transfer_data(from_user.id, to_user.id, overwrite=overwrite))
        await send_callback(inter, f'*Data was transferred from **{from_user.name}** to **{to_user.name}***')

    @discord.app_commands.command(description='Create a promo code')
    @discord.app_commands.describe(
        prise='Items that user will receive | Has to be json | Ex: {"coins": 10, "rare_case": 2}')
    @discord.app_commands.describe(lifespan='For how long the promocode will be usable (in minutes)')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def create_promocode(self, inter, prise: str,
                               max_uses: int = 999999,
                               name: str = None,
                               lifespan: int = -1):
        await DisUtils.pre_command_check(inter, allowed_users=config.PROMOCODERS)
        try:
            prise = json.loads(prise)
            if type(prise) == list:
                raise
        except:
            await send_callback(inter,
                                embed=generate_embed(title=f'*Bad json*',
                                                     color=config.error_color))
            return
        for item in prise:
            if not await Item.exists(item):
                await send_callback(inter,
                                    embed=generate_embed(title=f'*Item **"{item}"** doesn\'t exist*',
                                                         color=config.error_color))
                return
        if await PromoCode.exists(name):
            await PromoCode.delete(name)
        promo_code_code = await PromoCode.create(max_uses, prise, lifespan=lifespan * 60,
                                           code=name)
        await send_callback(inter,
                            embed=generate_embed(title=f'*Promo code `{promo_code_code}` created*'))

    @discord.app_commands.command(description='Leave from a server')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def leave(self, inter, server: str):
        await DisUtils.pre_command_check(inter, owner_only=True)
        await self.client.get_guild(int(server)).leave()
        await send_callback(inter, f'*I left from *{server}***')

    @discord.app_commands.command(description='Returns a list of guilds')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def guilds(self, inter):
        await DisUtils.pre_command_check(inter, owner_only=True)
        d = {}
        for guild in self.client.guilds:
            d[guild] = len(set([i for i in guild.members if not i.bot]))
        d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
        embeds = []
        total_member_count = 0
        for guild in self.client.guilds:
            total_member_count += guild.member_count
        title = f'🌐・{len(self.client.guilds)} | {len(set([i for i in self.client.get_all_members() if not i.bot]))}/{len(self.client.users)}'
        embed = generate_embed(title, '')
        for n, i in enumerate(d):
            embed.description += f"> {n + 1}. {d[i]} | {i} [{i.id}]\n"
            if len(embed.description) >= 4000:
                embeds.append(embed)
                embed = generate_embed(title, '')
        embeds.append(embed)
        await DisUtils.pagination(inter, 'en', embeds=embeds)


async def setup(client):
    await client.add_cog(AdminCommands(client))
