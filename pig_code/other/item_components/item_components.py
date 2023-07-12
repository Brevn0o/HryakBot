from ...core import *
from ...utils import *
from .special import *


async def item_remove(inter, item_id, update):
    User.remove_item(inter.author.id, item_id)
    # await update()


async def use_laxative(inter, item_id, update):
    User.remove_item(inter.author.id, item_id)
    Pig.add_buff(inter.author.id, 'laxative', 1)
    return {'pig': Pig.get_name(inter.author.id), 'step': Pig.get_buff_value(inter.author.id, 'laxative')}


async def cook(inter, item_id, update):
    if Inventory.get_item_amount(inter.author.id, 'grill') == 0:
        await error_callbacks.error(
            errors.NoItemInInventory('grill', Locales.ErrorCallbacks.no_mangal_to_cook, ephemeral=True,
                                     edit_original_message=False), inter)
        return

    async def cook_item(inter, item_id, amount):
        lang = User.get_language(inter.author.id)
        User.remove_item(inter.author.id, item_id, amount)
        User.add_item(inter.author.id, Inventory.get_item_cooked_id(item_id), amount)
        await update()
        await send_callback(inter, ephemeral=True,
                            embed=generate_embed(
                                title=Locales.InventoryItemCooked.title[lang].format(
                                    item=Inventory.get_item_name(item_id, lang)),
                                description=f"- {Locales.InventoryItemCooked.desc[lang].format(item=Inventory.get_item_name(item_id, lang), amount=amount)}",
                                prefix=Func.generate_prefix('scd'),
                                inter=inter,
                            ))

    await inter.response.send_modal(
        modal=modals.GetItemAmountModal(inter, item_id, cook_item, Locales.InventoryItemCookModal.label))


async def sell(inter, item_id, update):
    async def sell_item(inter, item_id, amount):
        lang = User.get_language(inter.author.id)
        User.remove_item(inter.author.id, item_id, amount)
        money_received = Inventory.get_item_cost(item_id) * amount
        Stats.add_money_earned(inter.author.id, money_received)
        Stats.add_items_sold(inter.author.id, item_id, amount)
        User.add_money(inter.author.id, money_received)
        await update()
        await send_callback(inter, ephemeral=True,
                            embed=generate_embed(
                                title=Locales.InventoryItemSold.title[lang].format(
                                    item=Inventory.get_item_name(item_id, lang)),
                                description=f"- {Locales.InventoryItemSold.desc[lang].format(item=Inventory.get_item_name(item_id, lang), amount=amount, money=money_received)}",
                                prefix=Func.generate_prefix('scd'),
                                inter=inter,
                            ))

    await inter.response.send_modal(
        modal=modals.GetItemAmountModal(inter, item_id, sell_item, Locales.InventoryItemSellModal.label))


def cook_comp():
    return {'label': {'en': 'Cook',
                      'ru': 'Приготовить'},
            'color': disnake.ButtonStyle.primary,
            'options': ['modal'],
            'func': cook}


def sell_comp():
    return {'label': {'en': 'Sell',
                      'ru': 'Продать'},
            'color': disnake.ButtonStyle.green,
            'options': ['modal'],
            'func': sell}


def case_comp():
    return {'label': {'en': 'Open',
                      'ru': 'Открыть'},
            'color': disnake.ButtonStyle.primary,
            'func': case.case_used}


item_components = {
    'laxative': {'use': {'label': {'en': 'Use',
                                   'ru': 'Использовать'},
                         'color': disnake.ButtonStyle.primary,
                         'func': use_laxative,
                         'callback': {'title': {'en': 'You used laxative',
                                                'ru': 'Вы использовали слабительное'},
                                      'description': {
                                          'en': '**{pig}** will produce more manure on the next **{step}** feedings',
                                          'ru': '**{pig}** будет давать больше навоза следующие **{step}** кормёжек'},
                                      'prefix': '💊'
                                      },
                         # 'sell'
                         }},
    'poop': {'use': {'label': {'en': 'Eat',
                               'ru': 'Съесть'},
                     'color': disnake.ButtonStyle.primary,
                     'func': poop.ate_and_poisoned},
             'sell': sell_comp()},
    'lard': {
        'cook': cook_comp(),
        'sell': sell_comp()},
    'barbecue': {'eat': {'label': {'en': 'Eat',
                                   'ru': 'Съесть'},
                         'color': disnake.ButtonStyle.primary,
                         'func': item_remove,
                         'callback': {'title': {'en': 'You ate barbecue',
                                                'ru': 'Вы съели шашлык'},
                                      'description': {
                                          'en': '*You feel guilty for biting off a piece of your pig*',
                                          'ru': '*Вы чувствуете вину за то что откусили кусочек своего хряка*'},
                                      'prefix': '🍖'
                                      }}, 'sell': sell_comp()},
    'common_case': {'sell': case_comp()},
    'rare_case': {'sell': case_comp()}
}

for item in items:
    if item not in item_components:
        item_components[item] = {}
