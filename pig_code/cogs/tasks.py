import datetime
import random

from ..core import *
from ..utils import *
from .. import modules


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_shop_update.start()

    @tasks.loop(seconds=60)
    async def daily_shop_update(self):
        last_update_timestamp = Shop.get_last_update_timestamp()
        if last_update_timestamp is None:
            Shop.add_shop_state(Func.generate_shop_daily_items())
        elif Func.get_current_timestamp() - last_update_timestamp >= 86000:
            Shop.add_shop_state(Func.generate_shop_daily_items())


def setup(client):
    client.add_cog(Tasks(client))
