import time

from .connection import Connection
from .tech import Tech
from ...core import *
from ...core.config import users_schema


class Stats:

    @staticmethod
    def fix_stats_structure_for_all_users(nested_key_path: str = '', standard_values: dict = None):
        if standard_values is None:
            standard_values = utils_config.default_stats
        Connection.make_request(f"UPDATE {config.users_schema} SET stats = '{'{}'}' WHERE stats IS NULL")
        for k, v in standard_values.items():
            new_key_path = f"{nested_key_path}.{k}" if nested_key_path else k
            if type(v) in [dict]:
                Connection.make_request(f"""
                UPDATE {config.users_schema}
                SET stats = JSON_SET(stats, '$.{new_key_path}', CAST(%s AS JSON))
                WHERE JSON_EXTRACT(stats, '$.{new_key_path}') IS NULL;
                """, params=(json.dumps(v),))
                Stats.fix_stats_structure_for_all_users(new_key_path, standard_values[k])
            else:
                Connection.make_request(f"""
                UPDATE {config.users_schema}
                SET stats = JSON_SET(stats, '$.{new_key_path}', {'CAST(%s AS JSON)' if isinstance(v, list) else '%s'})
                WHERE JSON_EXTRACT(stats, '$.{new_key_path}') IS NULL;
                """, params=(json.dumps(v) if isinstance(v, list) else v,))

    # @staticmethod
    # async def fix_stats_structure_for_all_users():
    #     users = Tech.get_all_users()
    #     for user in users:
    #         Stats.fix_stats_structure(user)
    #         await asyncio.sleep(0.1)
    #
    # @staticmethod
    # def fix_stats_structure(user_id):
    #     stats = Stats.get_stats(user_id)
    #     if stats is None:
    #         stats = {}
    #     for key, value in utils_config.user_stats.items():
    #         if key not in stats:
    #             stats[key] = value
    #     Stats.set_stats(user_id, stats)

    @staticmethod
    def get_stats(user_id):
        result = Connection.make_request(
            f"SELECT stats FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_stats(user_id, new_stats):
        new_stats = json.dumps(new_stats, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET stats = %s WHERE id = {user_id}", params=(new_stats,)
        )

    @staticmethod
    def add_pig_fed(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['pig_fed'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    def get_pig_fed(user_id):
        stats = Stats.get_stats(user_id)
        return stats['pig_fed']

    @staticmethod
    def set_streak(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['streak'] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    def add_streak(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['streak'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    def get_streak(user_id):
        stats = Stats.get_stats(user_id)
        return stats['streak']

    @staticmethod
    def add_money_earned(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['money_earned'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    def get_money_earned(user_id):
        stats = Stats.get_stats(user_id)
        return stats['money_earned']

    @staticmethod
    def add_commands_used(user_id, command, amount: int = 1):
        stats = Stats.get_stats(user_id)
        if command in stats['commands_used']:
            stats['commands_used'][command] += amount
        else:
            stats['commands_used'][command] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_commands_stats(user_id):
        stats = Stats.get_stats(user_id)
        return stats['commands_used']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_command_used_times(user_id, command):
        stats = Stats.get_stats(user_id)
        if command in stats['commands_used']:
            return stats['commands_used'][command]
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_total_commands_used(user_id):
        stats = Stats.get_stats(user_id)
        total_commands_used = 0
        for i in stats['commands_used']:
            total_commands_used += stats['commands_used'][i]
        return total_commands_used

    @staticmethod
    def add_items_used(user_id, item, amount: int = 1):
        stats = Stats.get_stats(user_id)
        if item in stats['items_used']:
            stats['items_used'][item] += amount
        else:
            stats['items_used'][item] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_items_used(user_id, item):
        stats = Stats.get_stats(user_id)
        if item in stats['items_used']:
            return stats['items_used'][item]
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_total_items_used(user_id):
        stats = Stats.get_stats(user_id)
        total_items_used = 0
        for i in stats['items_used']:
            total_items_used += stats['items_used'][i]
        return total_items_used

    @staticmethod
    def add_items_sold(user_id, item, amount: int = 1):
        stats = Stats.get_stats(user_id)
        if item in stats['items_sold']:
            stats['items_sold'][item] += amount
        else:
            stats['items_sold'][item] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_items_sold_stats(user_id):
        stats = Stats.get_stats(user_id)
        return stats['items_sold']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_sold_amount(user_id, item):
        stats = Stats.get_stats(user_id)
        if item in stats['items_sold']:
            return stats['items_sold'][item]
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_total_items_sold(user_id):
        stats = Stats.get_stats(user_id)
        total_items_sold = 0
        for i in stats['items_sold']:
            total_items_sold += stats['items_sold'][i]
        return total_items_sold

    @staticmethod
    def set_language_changed(user_id, language_changed: bool):
        stats = Stats.get_stats(user_id)
        stats['language_changed'] = language_changed
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_language_changed(user_id):
        stats = Stats.get_stats(user_id)
        return stats['language_changed']

    @staticmethod
    def add_successful_orders(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['successful_orders'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    def get_successful_orders(user_id):
        stats = Stats.get_stats(user_id)
        return stats['successful_orders']

    @staticmethod
    def add_dollars_donated(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['dollars_donated'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    def get_dollars_donated(user_id):
        stats = Stats.get_stats(user_id)
        return stats['dollars_donated']

