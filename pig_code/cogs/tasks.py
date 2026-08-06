from ..core import *
from ..utils import *
from .. import modules


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_shop_update.start()
        self.server_shop_update.start()
        self.server_weekly_rewards.start()
        self.server_polls.start()
        self.process_streaks.start()
        self.process_orders.start()
        if not config.TEST:
            self.monitoring_data_update.start()

    @tasks.loop(seconds=60)
    async def register_guilds(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        await Guild.register([guild.id for guild in self.client.guilds])

    @tasks.loop(seconds=60)
    async def process_streaks(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        await hryak.GameFunc.reset_expired_streaks()

    @tasks.loop(seconds=60)
    async def daily_shop_update(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        await Shop.update_if_needed()

    @tasks.loop(seconds=60)
    async def server_polls(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        await modules.guild_pig.callbacks.finalise_polls(self.client)

    @tasks.loop(seconds=60)
    async def server_shop_update(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        await Shop.update_server_if_needed()

    @tasks.loop(seconds=60)
    async def server_weekly_rewards(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        await modules.guild_pig.callbacks.pay_weekly_rewards(self.client)

    @tasks.loop(seconds=300)
    async def give_items(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        for item_id in await Tech.get_all_items(exceptions=(('requirements', None),)):
            allowed_users = await Item.get_all_allowed_users_by_requirements(self.client, item_id)
            for user_id in allowed_users:
                await User.register_user_if_not_exists(user_id)
                await User.set_item_amount(user_id, item_id, 1)
                await asyncio.sleep(.1)
            for user_id in await Tech.get_all_users(where=f"JSON_EXTRACT(inventory, '$.{item_id}.amount') > 0",
                                              exclude_users=allowed_users):
                await User.set_item_amount(user_id, item_id, 0)
                await asyncio.sleep(.1)

    @tasks.loop(seconds=30)
    async def process_orders(self):
        for order_id in await Order.get_all_orders():
            user_id = await Order.get_user(order_id)
            lang = await User.get_language(user_id)
            order_status = await Order.get_status(order_id, fetch=True)
            if (hryak.functions.Func.generate_current_timestamp() - await Order.get_timestamp(order_id) > (60 * 60 * 24 * 3) or
                    order_status == 'failed'):
                await Order.delete(order_id)
            if order_status in ['completed', 'success', 'hold']:
                await DisUtils.send_notification(await User.get_discord_user(self.client, user_id),
                                                 title=translate(Locales.PremiumShop.item_give_notification_title, lang),
                                                 description=translate(Locales.PremiumShop.item_give_notification_desc,
                                                                       lang, {'items': await DisUtils.get_items_in_str_list(
                                                      await Order.get_items(order_id),
                                                      await User.get_language(user_id))}),
                                                 prefix_emoji='💎')
                for item_id, amount in (await Order.get_items(order_id)).items():
                    await User.add_item(user_id, item_id, amount)
                await Stats.add_successful_orders(user_id, 1)
                await Stats.add_dollars_donated(user_id, round(
                    await Order.get_amount(order_id) / hryak.config.currency_to_usd[await Order.get_currency(order_id)], 2))
                await Order.delete(order_id)
                await asyncio.sleep(1)
                continue

    @tasks.loop(seconds=3600)
    async def monitoring_data_update(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        servers = len(self.client.guilds)
        Func.send_data_to_sdc(self.client)
        Func.send_data_to_boticord(self.client)
        await Func.send_data_to_stats_channel(self.client, servers)


async def setup(client):
    await client.add_cog(Tasks(client))
