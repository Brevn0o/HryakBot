import os
import logging
from discord.ext import commands
import topgg
from ..core import *
from ..utils import *
from .. import modules
from ..utils.discord_utils import send_webhook

PORT = 8000
WEBHOOK_PATH = "/"


class VoteWebhookCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.webhook_manager = topgg.WebhookManager(client).dbl_webhook(
            WEBHOOK_PATH,
            config.TOPGG_WEBHOOK_AUTH,
        )

    async def cog_load(self):
        self.webhook_manager.run(PORT)

    async def cog_unload(self):
        await self.webhook_manager.close()

    @commands.Cog.listener()
    async def on_dbl_vote(self, data: dict):
        """
        Fired whenever top.gg POSTs a vote event to your webhook.
        `data` looks like:
        {
            "user": "user_id_str",
            "type": "upvote" or "test",
            "isWeekend": bool,
            "query": "...",
            "bot": "bot_id_str"
        }
        """
        user_id = int(data["user"])
        await self.handle_vote(user_id, data)

    async def handle_vote(self, user_id: int, data: dict):
        await send_webhook(config.REPORT_WEBHOOKS, content=f"vote detected")
        print(f"{user_id}: {data}")
        await send_webhook(config.REPORT_WEBHOOKS, content=f"{user_id}: {data}")


async def setup(bot: commands.Bot):
    await bot.add_cog(VoteWebhookCog(bot))