import os
import logging
from aiohttp import web
from discord.ext import commands
import topgg
from ..core import *
from ..utils import *
from .. import modules
from ..utils.discord_utils import send_webhook

PORT = 8000
WEBHOOK_PATH = "/dbl"


def clean_auth(value) -> str:
    """Env vars arrive raw - a pasted trailing newline or wrapping quotes would
    otherwise fail top.gg's exact-match auth check and return 401."""
    return (value or '').strip().strip('"').strip("'")


@web.middleware
async def log_webhook_request(request, handler):
    """Logs what actually arrives, so a 401 can be told apart from never being called.
    Only the tail of the secret is logged - never the whole thing."""
    sent = request.headers.get('Authorization', '')
    expected = clean_auth(config.TOPGG_WEBHOOK_AUTH)
    response = await handler(request)
    print(f'[topgg] {request.method} {request.path} -> {response.status} | '
          f'sent len={len(sent)} ends={sent[-4:] or "-"} | '
          f'expected len={len(expected)} ends={expected[-4:] or "-"} | '
          f'match={sent == expected}')
    return response


class VoteWebhookCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.webhook_manager = topgg.WebhookManager()
        endpoint = (
            topgg.WebhookEndpoint()
            .type(topgg.WebhookType.BOT)
            .route(WEBHOOK_PATH)
            .auth(clean_auth(config.TOPGG_WEBHOOK_AUTH))
            .callback(self.on_dbl_vote)
        )
        self.webhook_manager.endpoint(endpoint)
        self.webhook_manager.app.middlewares.append(log_webhook_request)

    async def cog_load(self):
        expected = clean_auth(config.TOPGG_WEBHOOK_AUTH)
        print(f'[topgg] listening on :{PORT}{WEBHOOK_PATH} | '
              f'secret len={len(expected)} ends={expected[-4:] or "NOT SET"}')
        await self.webhook_manager.start(PORT)

    async def cog_unload(self):
        await self.webhook_manager.close()

    async def on_dbl_vote(self, data: "topgg.BotVoteData"):
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
        await send_webhook(config.REPORT_WEBHOOKS[0], content=f"vote detected")
        print(f"{user_id}: {data}")
        await send_webhook(config.REPORT_WEBHOOKS[0], content=f"{user_id}: {data}")


async def setup(client: commands.Bot):
    await client.add_cog(VoteWebhookCog(client))