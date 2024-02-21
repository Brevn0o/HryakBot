import cProfile

from . import config
from .imports import *

default_pig = {'name': 'Hryak',
               'weight': 1,
               'feed_history': [],
               'meat_history': [],
               'breed_history': [],
               'pregnant_time': None,
               'pregnant_with': None,
               'pregnant_by': None,
               'pregnancy_duration': None,
               'buffs': {
                   'laxative': 0
               },
               'genetic': {
                   'tail': 'default_body',
                   'left_ear': 'default_body',
                   'left_eye': 'white_eyes',
                   'right_eye': 'white_eyes',
                   'left_pupil': 'black_pupils',
                   'right_pupil': 'black_pupils',
                   'right_ear': 'default_body',
                   'nose': 'default_body',
                   'body': 'default_body',
                   'eyes': 'white_eyes',
                   'pupils': 'black_pupils',
               },
               'skins': {'body': None,
                         'tattoo': None,
                         'tail': None,
                         'left_ear': None,
                         'makeup': None,
                         'mouth': None,
                         'left_eye': None,
                         'right_eye': None,
                         'left_pupil': None,
                         'right_pupil': None,
                         'middle_ear': None,
                         'right_ear': None,
                         'suit': None,
                         'glasses': None,
                         'nose': None,
                         'piercing_nose': None,
                         'face': None,
                         'piercing_ear': None,
                         'back': None,
                         'hat': None,
                         'legs': None,
                         'tie': None}}
skin_layers_rules = {
    'mouth': {'before': [
        'nose',
    ]},
    'glasses': {'before': [
        'nose',
    ]},
    'nose': {'before': [
    ],
        'after': [
            'left_eye',
            'right_eye',
            'left_pupil',
            'right_pupil',
        ]},
    'piercing_nose': {'after': [
            'nose'
        ]},
    'piercing_ear': {'after': [
        'right_ear',
    ]},
'hat': {
    'hide': ['middle_ear']
}}

pig_feed_cooldown = 4 * 60 ** 2 if not config.TEST else 5  # seconds
premium_pig_feed_cooldown = 2 * 60 ** 2 if not config.TEST else 5  # seconds

pig_meat_cooldown = 40 * 60 ** 2 if not config.TEST else 10  # seconds
premium_pig_meat_cooldown = 20 * 60 ** 2 if not config.TEST else 5  # seconds

pig_breed_cooldown = 48 * 60 ** 2 if not config.TEST else 10  # seconds
premium_pig_breed_cooldown = 30 * 60 ** 2 if not config.TEST else 5  # seconds

daily_shop_items_types = {
    'hat': 1,
    'glasses': 1,
    'body': 1,
    'pupils': 1,
    'makeup': 1,
    'other': 2
}

fight_gifs = [
    'https://cdn.discordapp.com/attachments/1023656142863339550/1111719980988387468/guineapigs-fighting.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111722267009884160/giphy_2.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111723511011090562/fh.gif'
]
win_gifs = [
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727166938423437/5645cf1adc20bb60ef240d39a8b3389d.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727167336878231/IdleTautIndiancow-size_restricted.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727167726952468/angry-birds-pig-birthday-party-dance-16fdgnq0m6bmjya2.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727168129601606/47b99c0b237fd6e967e72f8cdcd1eebc.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727168473538661/QuarterlyLividGordonsetter-max-1mb.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727168918147184/dancing-pig-9.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727169345949847/dancing-pig-3.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727169744424980/EminentFlickeringAvocet-max-1mb.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727170180616192/200w.gif',
    'https://cdn.discordapp.com/attachments/933356358097580103/1111727170600050889/pig-cute.gif',
]
image_links = {
    'inventory': 'https://cdn.discordapp.com/attachments/933356358097580103/1173751766408511609/inventory.png',
    'invite': 'https://cdn.discordapp.com/attachments/933356358097580103/1173755632717942834/invite.png',
    'trade': 'https://cdn.discordapp.com/attachments/933356358097580103/1173755494003912775/trade.png',
    'shop': 'https://cdn.discordapp.com/attachments/933356358097580103/1173755603345231934/shop.png',
    'top': 'https://cdn.discordapp.com/attachments/933356358097580103/1173755540304830474/top.png'
}
db_api_cash_size = 10
db_api_cash_ttl = 1

default_pig_body_genetic = ['default_body']
default_pig_pupils_genetic = ['black_pupils', 'blue_pupils', 'green_pupils',
                              'orange_pupils', 'pink_pupils', 'yellow_pupils', 'purple_pupils']
default_pig_eyes_genetic = ['white_eyes']
user_stats = {'pig_fed': 0, 'money_earned': 0, 'commands_used': {}, 'items_used': {}, 'items_sold': {},
              'language_changed': False}
guild_settings = {'join_channel': None, 'join_message': None, 'allow_say': False}
user_settings = {'language': 'en', 'blocked': False, 'block_reason': None, 'isolated': False, 'family': None,
                 'isolation_level': 0}
emotions_erase_cords = {'sad': [(530, 508, 308, 774, 704, 648), (1292, 866, 888, 642, 1176, 570)],
                        'happy': [(695, 970, 865, 970, 865, 1030, 695, 1030), (1115, 985, 900, 985, 900, 1030, 1110, 1030)],
                        'angry': [(604, 498, 394, 658, 762, 832), (758, 842, 1220, 670, 840, 546)],
                        'sus': [(760, 786, 1268, 786, 1018, 426)],
                        'dont_care': [(328, 774, 732, 782, 654, 444),
                                      (760, 786, 1268, 786, 1018, 426)]}

ignore_users_in_top = [1102273144733049003, 932191352677097534, 715575898388037676]
# anti_bot_decreases = [0, 0, 0, 0, 0, 0, 2, 5, 15, 20, 25, 45, 60, 80, 95, 96, 97, 98, 99]
anti_bot_decreases = [0]

# text
start_text = '**I am alive!**'

# embed colors
main_color = 0xc7604c
error_color = 0xc94312
warn_color = 0xe0bb36
success_color = 0x2fc256
premium_color = 0x61dfff

common_rarity_color = 0x858784
uncommon_rarity_color = 0x45ff4b
rare_rarity_color = 0x4d9aff
epic_rarity_color = 0xc14dff
mythical_rarity_color = 0xff3d33
legendary_rarity_color = 0xffee54

pig_ages = {
    0: '1',
    20: '2',
    50: '3',
    100: '4',
    300: '5',
    500: '6',
    1000: '7',
}

rarity_colors = {
    '1': common_rarity_color,
    '2': uncommon_rarity_color,
    '3': rare_rarity_color,
    '4': epic_rarity_color,
    '5': mythical_rarity_color,
    '6': legendary_rarity_color,
}

db_caches = {
    'user.get_inventory': TTLCache(maxsize=1000, ttl=600000),
    'user.get_settings': TTLCache(maxsize=1000, ttl=600000),
    'item.get_data': TTLCache(maxsize=1000, ttl=600000),
    'item.get_emoji': TTLCache(maxsize=1000, ttl=600000),
    'tech.__get_all_items': TTLCache(maxsize=1000, ttl=600000),
    'tech.get_all_items': TTLCache(maxsize=1000, ttl=600000)
}
profiler = cProfile.Profile()
profiler.enable()

pig_names = [
    "Bacon",
    "Porkchop",
    "Hamlet",
    "Wilbur",
    "Piggy",
    "Sausage",
    "Oinkers",
    "Truffles",
    "Snout",
    "Piglet",
    "Hambone",
    "Peppa",
    "Pumbaa",
    "Babe",
    "Porky",
    "Hogwarts",
    "Mudpie",
    "Rasher",
    "Pigpen",
    "Scraps",
    "Porkins",
    "Piggy Smalls",
    "Miss Piggy",
    "Swine",
    "Snort",
    "Porkenstein",
    "Baconator",
    "Hamlet Jr.",
    "Muddy",
    "Snuffle",
    "Porker",
    "Pigtails",
    "Bacon Bits",
    "Sizzles",
    "Hoglet",
    "Pork Belly",
    "Squealer",
    "Oinkerbell",
    "Rasher",
    "Pork Chop",
    "Snuffles",
    "Nugget",
    "Curly",
    "Sir Oinks-a-lot",
    "Porkenstein",
    "Pigwig",
    "Piggy Sue",
    "Snorty",
    "Porkchops",
    "Porky Pie",
    "Baconator Jr.",
    "Porkums"
]
