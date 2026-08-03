from discord import Locale
from . import config

valid_discord_locales = ['en', 'ru', 'uk']

full_names = {'en': 'English',
              'ru': 'Russian | Pусский',
              'uk': 'Ukrainian | Українська'}

big_texts = {}


class Locales:
    app_commands_locales = {
        'choice-true': {'en': '✅ True',
                        'ru': '✅ Да',
                        'uk': '✅ Так'},
        'choice-false': {'en': '❌ False',
                         'ru': '❌ Нет',
                         'uk': '❌ Ні'},
        'help-desc': {'en': 'Get help for the bot',
                      'ru': 'Хряковое пособие и обучение',
                      'uk': 'Хрякова допомога та навчання'},
        'context-profile-name': {'en': 'Profile',
                                 'ru': 'Профиль',
                                 'uk': 'Профіль'},
        'profile-desc': {'en': 'View players\'s profile',
                         'ru': 'Посмотреть профиль игрока',
                         'uk': 'Переглянути профіль гравця'},
        'profile-user-name': {'en': 'user',
                              'ru': 'пользователь',
                              'uk': 'користувач'},
        'profile-user-desc': {'en': 'The user whose profile you want to view',
                              'ru': 'Пользователь, у которого вы хотите посмотреть профиль',
                              'uk': 'Користувач, у якого ви хочете переглянути профіль'},
        'top-desc': {'en': 'Players top',
                     'ru': 'Топ игроков',
                     'uk': 'Топ гравців'},
        'top-global-name': {'en': 'global',
                            'ru': 'глобальный',
                            'uk': 'глобальний'},
        'top-global-desc': {'en': 'Display the global user leaderboard',
                            'ru': 'Показать глобальный топ пользователей',
                            'uk': 'Показати глобальний топ користувачів'},
        'buffs-desc': {'en': 'Buffs applied to your pig',
                       'ru': 'Баффы, примененные к вашему Хряку',
                       'uk': 'Бафи, застосовані до вашого Хряка'},
        'inventory-desc': {'en': 'View your inventory',
                           'ru': 'Посмотреть свой инвентарь',
                           'uk': 'Переглянути свій інвентар'},
        'wardrobe-desc': {'en': 'Skins for your pig',
                          'ru': 'Скины для вашего хряка',
                          'uk': 'Скіни для вашого хряка'},
        'shop-desc': {'en': 'View pig shop',
                      'ru': 'Заглянуть в магазин',
                      'uk': 'Зазирнути до магазину'},
        'quests-desc': {'en': 'View available quests',
                        'ru': 'Посмотреть доступные квесты',
                        'uk': 'Переглянути доступні квести'},
        'feed-desc': {
            'en': 'Feed your pig',
            'ru': 'Накормить своего хряка',
            'uk': 'Погодувати свого хряка',
        },
        'butcher-desc': {'en': 'Harvest meat from your pig',
                         'ru': 'Снять немного сала с вашего хряка (ему не больно)',
                         'uk': 'Зрізати трохи сала з вашого хряка (йому не боляче)'},
        'rename-desc': {'en': 'Rename your pig',
                        'ru': 'Переименовать своего хряка',
                        'uk': 'Перейменувати свого хряка'},
        'rename-name-name': {'en': 'name',
                             'ru': 'имя',
                             'uk': "ім'я"},
        'rename-name-desc': {'en': 'Choose a new name for your pig',
                             'ru': 'Новое имя для свинтуса',
                             'uk': "Нове ім'я для свинтуса"},
        'duel-desc': {'en': 'Arrange a duel between pigs',
                      'ru': 'Устроить дуэль между хряками',
                      'uk': 'Влаштувати дуель між хряками'},
        'duel-user-name': {'en': 'user',
                           'ru': 'пользователь',
                           'uk': 'користувач'},
        'duel-user-desc': {'en': 'Select the user you want to duel with',
                           'ru': 'Пользователь с которым вы хотите провести дуэль',
                           'uk': 'Користувач, з яким ви хочете провести дуель'},
        'duel-bet-name': {'en': 'bet',
                          'ru': 'ставка',
                          'uk': 'ставка'},
        'duel-bet-desc': {'en': 'The number of coins you want to bet',
                          'ru': 'Количество монет, которое хотите поставить',
                          'uk': 'Кількість монет, яку хочете поставити'},
        'trade-desc': {'en': 'Trade with user',
                       'ru': 'Торговать с пользователем',
                       'uk': 'Торгувати з користувачем'},
        'trade-user-name': {'en': 'user',
                            'ru': 'пользователь',
                            'uk': 'користувач'},
        'trade-user-desc': {'en': 'The user you want to trade with',
                            'ru': 'Пользователь с которым вы хотите торговать',
                            'uk': 'Користувач, з яким ви хочете торгувати'},
        'send_money-desc': {'en': 'Transfer money to another user',
                            'ru': 'Перевести деньги другом пользователю',
                            'uk': 'Переказати гроші іншому користувачу'},
        'send_money-user-name': {'en': 'user',
                                 'ru': 'пользователь',
                                 'uk': 'користувач'},
        'send_money-user-desc': {'en': 'User to whom you want to send money',
                                 'ru': 'Пользователь которому отправить деньги',
                                 'uk': 'Користувач, якому надіслати гроші'},
        'send_money-amount-name': {'en': 'amount',
                                   'ru': 'количество',
                                   'uk': 'кількість'},
        'send_money-amount-desc': {'en': 'Amount of money to transfer',
                                   'ru': 'Количество денег для перевода',
                                   'uk': 'Кількість грошей для переказу'},
        'send_money-currency-name': {'en': 'currency',
                                     'ru': 'валюта',
                                     'uk': 'валюта'},
        'send_money-currency-desc': {'en': 'Currency you want to send',
                                     'ru': 'Валюта, которую вы хотите отправить',
                                     'uk': 'Валюта, яку ви хочете надіслати'},
        'send_money-message-name': {'en': 'message',
                                    'ru': 'сообщение',
                                    'uk': 'повідомлення'},
        'send_money-message-desc': {'en': 'The message the user will receive',
                                    'ru': 'Сообщение, которое получит пользователь',
                                    'uk': 'Повідомлення, яке отримає користувач'},
        'report-desc': {'en': 'Report bug',
                        'ru': 'Сообщить о баге',
                        'uk': 'Повідомити про баг'},
        'report-text-name': {'en': 'text',
                             'ru': 'текст',
                             'uk': 'текст'},
        'report-text-desc': {'en': 'Describe a bug',
                             'ru': 'Описание бага',
                             'uk': 'Опис бага'},
        'report-attachment-name': {'en': 'attachment',
                                   'ru': 'картинка',
                                   'uk': 'картинка'},
        'report-attachment-desc': {'en': 'Attach a screenshot',
                                   'ru': 'Скриншот с багом',
                                   'uk': 'Скриншот з багом'},
        'promocode-desc': {'en': 'Use promo code',
                           'ru': 'Использовать промо код',
                           'uk': 'Використати промокод'},
        'promocode-code-name': {'en': 'code',
                                'ru': 'код',
                                'uk': 'код'},
        'promocode-code-desc': {'en': 'Enter your promo code',
                                'ru': 'Введите ваш промо-код',
                                'uk': 'Введіть ваш промокод'},
        'say-desc': {'en': 'Make hryak say something',
                     'ru': 'Заставить хряка сказать что-то',
                     'uk': 'Змусити хряка сказати щось'},
        'say-text-name': {'en': 'text',
                          'ru': 'текст',
                          'uk': 'текст'},
        'say-text-desc': {'en': 'Use "\\\\" for a line break',
                          'ru': 'Используйте "\\\\" для перехода на следующую строку',
                          'uk': 'Використовуйте "\\\\" для переходу на наступний рядок'},
        'say-user-name': {'en': 'user',
                          'ru': 'пользователь',
                          'uk': 'користувач'},
        'say-user-desc': {'en': 'Speak for the user',
                          'ru': 'Говорить от лица пользователя',
                          'uk': 'Говорити від імені користувача'},
        'view-desc': {'en': 'View the appearance of your pig',
                      'ru': 'Посмотреть внешний вид хряка',
                      'uk': 'Переглянути зовнішній вигляд хряка'},
        'view-user-name': {'en': 'user',
                           'ru': 'пользователь',
                           'uk': 'користувач'},
        'view-user-desc': {'en': 'The user you want to see the pig of',
                           'ru': 'Пользователь, у которого вы хотите посмотреть хряка',
                           'uk': 'Користувач, у якого ви хочете переглянути хряка'},
        'language-desc': {
            'en': 'Change bot language',
            'ru': 'Изменить язык бота',
            'uk': 'Змінити мову бота'
        },
        'language-language-name': {
            'en': 'language',
            'ru': 'язык',
            'uk': 'мова'
        },
        'language-language-desc': {
            'en': 'The language that Hryak will speak',
            'ru': 'Язык, на котором Хряк будет хрюкать',
            'uk': 'Мова, якою Хряк буде хрюкати'
        },
        'settings-say-desc': {'en': 'Configuring the say command',
                              'ru': 'Настройка команды /say',
                              'uk': 'Налаштування команди /say'},
        'settings-say-allow-name': {'en': 'allow',
                                    'ru': 'включить',
                                    'uk': 'увімкнути'},
        'settings-say-allow-desc': {'en': 'Just choose yes or no',
                                    'ru': 'Просто выбери да или нет',
                                    'uk': 'Просто обери так чи ні'},
        'settings-top-desc': {'en': 'Configuring the leaderboard command',
                                      'ru': 'Настройка ко��анды /leaderboard',
                                      'uk': 'Налаштування команди /leaderboard'},
        'settings-top-participate-name': {'en': 'participate',
                                             'ru': 'участвовать',
                                             'uk': 'брати участь'},
        'settings-top-participate-desc': {'en': 'Just choose yes or no',
                                                  'ru': 'Просто выбери да или нет',
                                                  'uk': 'Просто обери так чи ні'},
    }

    user_install_content = {
        'en': f'*[Feed and grow your pig!]({config.BOT_AUTH_LINK})*',
        'ru': f'*[Вырасти своего Хряка!]({config.BOT_AUTH_LINK})*',
        'uk': None
    }

    class Feed:
        feed_scd_title = {
            'en': 'Your pig has been fed',
            'ru': 'Вы покормили своего хряка',
            'uk': 'Ви погодували свого хряка'
        }
        feed_scd_desc_list = {
            'en': ['**{pig}** has gained **{mass}** kg'],
            'ru': ['**{pig}** поправился на **{mass}** кг',
                   '**{pig}** набрал **{mass}** кг сала',
                   '**{pig}** стал больше на **{mass}** кг',
                   '**{pig}** прибавил **{mass}** кг'],
            'uk': ['**{pig}** набрала **{mass}** кг',
                   '**{pig}** здобула **{mass}** кг сала',
                   '**{pig}** стала більшою на **{mass}** кг',
                   '**{pig}** додала **{mass}** кг']
        }
        feed_fail_desc_list = {
            'en': ['Your **{pig}** vomited and lost **{mass}** kg'],
            'ru': ['Вашего **{pig}** стошнило и он похудел на **{mass}** кг'],
            'uk': ['Вашого **{pig}** стошнило і він схуд на **{mass}** кг']
        }
        pig_pooped_desc_list = {
            'en': ['**{pig}** has pooped, yielding **{poop}** 💩'],
            'ru': ['**{pig}** покакал и вы получили **{poop}** 💩',
                   '**{pig}** испражнился и вы получили **{poop}** 💩',
                   '**{pig}** справил нужду, и вы получили **{poop}** 💩'],
            'uk': ['**{pig}** покакав і ви отримали **{poop}** 💩',
                   '**{pig}** випорожнився і ви отримали **{poop}** 💩',
                   '**{pig}** зробив потребу, і ви отримали **{poop}** 💩']
        }
        total_pig_weight = {
            'en': "Your pig's weight: **{weight}** kg",
            'ru': 'Масса твоего хряка: **{weight}** кг',
            'uk': 'Вага вашого хряка: **{weight}** кг'
        }

    class Butcher:
        butcher_title = {'en': "You've harvested some meat",
                         'ru': 'Вы срезали немного сала',
                         'uk': 'Ви зрізали трохи сала'}
        butcher_desc_list = {'en': ["You've harvested some lard from **{pig}** and obtained **{meat}** 🥓"],
                             'ru': ['Вы срезали немного сала с **{pig}** и получили **{meat}** 🥓'],
                             'uk': ['Ви зрізали трохи сала з **{pig}** та отримали **{meat}** 🥓']}
        weight_lost_desc_list = {'en': ['**{pig}** lost **{weight_lost}** kg of weight'],
                                 'ru': ['**{pig}** потерял **{weight_lost}** кг веса'],
                                 'uk': ['**{pig}** втратив **{weight_lost}** кг ваги']}
        no_knife_desc = {'en': '*Planning to slice the meat barehanded? Better find a knife*',
                         'ru': '*Ты собираешся мясо руками снимать? Найди нож*',
                         'uk': "*Ти збираєшся м'ясо руками знімати? Знайди ніж*"}
        total_pig_weight = {'en': "Your pig's weight: **{weight}** kg",
                            'ru': 'Масса твоего хряка: **{weight}** кг',
                            "uk": 'Маса твого кнура: **{weight}** кг'}

    class Duel:
        invite_title = {'en': 'Invitation to a duel',
                        'ru': 'Приглашение на дуэль',
                        'uk': 'Запрошення на дуель'}
        personal_invite_desc = {'en': '***{opponent}** was invited to duel with **{user}***\n\n'
                                      '- Bet: **{bet}** 🪙',
                                'ru': '***{opponent}** был приглашен на дуэль с **{user}***\n\n'
                                      '- Ставка: **{bet}** 🪙',
                                'uk': '***{opponent}** був запрошений на дуель з **{user}***\n\n- Ставка: **{bet}** 🪙'}
        personal_invite_dm_desc = {'en': '***You** were invited to duel with **{user}***\n\n'
                                         '- Bet: **{bet}** 🪙',
                                   'ru': '***Вы** были приглашены на дуэль с **{user}***\n\n'
                                         '- Ставка: **{bet}** 🪙\n',
                                   'uk': '***Ви** були запрошені на дуель з **{user}***\n\n- Ставка: **{bet}** 🪙\n'}
        duel_canceled_title = {'en': 'Duel was canceled',
                               'ru': 'Дуэль была отменена',
                               'uk': 'Дуель була скасована'}
        opponent_reject_desc = {'en': '***{user}** declined duel invitation*',
                                'ru': '***{user}** отклонил приглашение на дуэль*',
                                'uk': '***{user}** відхилив запрошення на дуель*'}
        no_money_for_bet_desc = {'en': "***{user}** is so poor that he didn't have enough money to bet*",
                                 'ru': '***{user}** настолько бедный, что ему не хватило денег на ставку*',
                                 'uk': '***{user}** настільки бідний, що йому не вистачило грошей на ставку*'}
        no_response_desc = {'en': "***{user}** did not come to the duel*",
                            'ru': '***{user}** не пришёл на дуэль*',
                            'uk': '***{user}** не прийшов на дуель*'}
        fight_is_starting_title = {'en': 'The duel will start in {time_to_start} s',
                                   'ru': 'Дуэль начнётся через {time_to_start} сек',
                                   'uk': 'Дуель почнеться через {time_to_start} сек'}
        fight_is_starting_desc = {'en': '***{pig1}** is about to fight **{pig2}**. Who will win?*\n\n'
                                        '- *Here\'s what our experts think:*',
                                  'ru': '***{pig1}** собирается сразиться с **{pig2}**. Кто же победит?*\n\n'
                                        '- *Вот что думают наши эксперты:*',
                                  'uk': '***{pig1}** збирається битися з **{pig2}**. Хто ж переможе?*\n\n- *Ось що думають наші експерти:*'}
        fight_starting_field_value = {'en': '```Weight: {weight} kg\n'
                                            'Win chance: {chance} %```',
                                      'ru': '```Вес: {weight} кг\n'
                                            'Шанс на победу: {chance} %```',
                                      'uk': '```Вага: {weight} кг\nШанс на перемогу: {chance} %```'}
        fight_is_going_title = {'en': 'Duel is going...',
                                'ru': 'Идёт дуэль...',
                                'uk': 'Триває дуель...'}
        fight_is_going_desc = {
            'en': "***{pig1}** and **{pig2}** fight each other brutally. It's not yet clear who will win*",
            'ru': '***{pig1}** и **{pig2}** брутально сражаются друг с другом. Ещё не ясно кто победит*',
            'uk': "***{pig1}** та **{pig2}** брутально б'ються один з одним. Ще не ясно, хто переможе*"}
        fight_ended_title = {'en': 'Duel ended',
                             'ru': 'Дуэль окончена',
                             'uk': 'Дуель закінчена'}
        fight_ended_desc = {'en': '***{pig}** won the duel. Let\'s congratulate him*\n\n'
                                  '- *Its owner - **{user}** received **{money_earned}** 🪙*',
                            'ru': '***{pig}** выиграл дуэль. Давайте поздравим его*\n\n'
                                  '- *Его владелец - **{user}** получил **{money_earned}** 🪙*',
                            'uk': '***{pig}** виграв дуель. Давайте привітаємо його*\n\n- *Його власник - **{user}** отримав **{money_earned}** 🪙*'}

    class Trade:
        scd_title = {'en': 'Successful trade',
                     'ru': 'Успешная торговля',
                     'uk': 'Успішна торгівля'}
        scd_desc = {'en': '*Trading between **{user1}** and **{user2}** was successful*',
                    'ru': '*Торговля между **{user1}** и **{user2}** прошла успешно*',
                    'uk': '*Торгівля між **{user1}** та **{user2}** пройшла успішно*'}
        add_item_placeholder = {'en': 'Add item',
                                'ru': 'Добавить предмет',
                                'uk': 'Додати предмет'}
        cancel_title = {'en': 'Trade canceled',
                        'ru': 'Трэйд отменен',
                        'uk': 'Трейд скасовано'}
        cancel_desc = {'en': '***{user}** has canceled the trade*',
                       'ru': '*Пользователю **{user}** не понравилась сделка*',
                       'uk': '*Користувачу **{user}** не сподобалася угода*'}
        trade_invitation_title = {'en': 'You have been invited to a trade',
                                  'ru': 'Вы были приглашены на торговлю',
                                  'uk': 'Вас запросили на торгівлю'}
        trade_invitation_desc = {'en': '***{user}** invited you to trade*',
                                 'ru': '***{user}** пригласил вас, чтобы поторговаться*',
                                 'uk': '***{user}** запросив вас, щоб поторгуватися*'}
        add_item_modal_title = {'en': 'Trade',
                                'ru': 'Трейд',
                                'uk': 'Трейд'}
        add_item_with_tax_modal_label = {'en': 'Add {item_name} (tax {tax}%)',
                                         'ru': 'Добавить {item_name} (налог {tax}%)',
                                         'uk': 'Додати {item_name} (податок {tax}%)'}
        add_item_modal_label = {'en': 'Add {item}',
                                'ru': 'Добавить {item}',
                                'uk': 'Додати {item}'}
        tax_splitting_process_title = {'en': 'Payment of taxes',
                                       'ru': 'Оплата налогов',
                                       'uk': 'Сплата податків'}
        tax_splitting_process_desc = {'en': '*You need to pay some taxes in order to trade*',
                                      'ru': '*Вам нужно заплатить некоторое количество налогов, чтобы осуществить трейд*',
                                      'uk': '*Вам потрібно сплатити певну кількість податків, щоб здійснити трейд*'}
        tax_splitting_process_who_pays_desc = {'en': '*You need to decide who will pay the tax*',
                                               'ru': '*Вам нужно решить, кто заплатит налог*',
                                               'uk': '*Вам потрібно вирішити, хто сплатить податок*'}
        split_equally = {'en': 'Split equally',
                            'ru': 'Пополам',
                            'uk': 'Навпіл'}

    class SendMoney:
        scd_title = {'en': 'Transaction was successful',
                     'ru': 'Транзакция прошла успешно',
                     'uk': 'Транзакція пройшла успішно'}
        scd_desc = {'en': '***{money}** {currency_emoji} were sent to **{user}** account*',
                    'ru': '***{money}** {currency_emoji} были отправлены на счёт **{user}***',
                    'uk': '***{money}** {currency_emoji} були надіслані на рахунок **{user}***'}
        cancel_title = {'en': 'Transaction was canceled',
                        'ru': 'Транзакция была отменена',
                        'uk': 'Транзакція була скасована'}
        cancel_desc = {'en': "*You've decided against sending the money*",
                       'ru': '*Вы передумали отправлять свои деньги*',
                       'uk': '*Ви передумали надсилати свої гроші*'}
        event_title = {'en': 'You got some money',
                       'ru': 'Вам перевели деньги',
                       'uk': 'Вам переказали гроші'}
        event_desc = {'en': '***{user}** has transferred **{money}** {currency_emoji} to your account*',
                      'ru': '***{user}** перевёл на ваш счёт **{money}** {currency_emoji}*',
                      'uk': '***{user}** переказав на ваш рахунок **{money}** {currency_emoji}*'}
        confirm_desc = {'en': '*Are you sure you want to send **{money}** {currency_emoji} to **{user}**?*\n\n'
                              '- Tax is **{tax}** %\n'
                              '- **{money_with_tax}** {currency_emoji} will be charged from your account',
                        'ru': '*Вы точно хотите отправить **{money}** {currency_emoji} на счёт **{user}**?*\n\n'
                              '- Налог составляет **{tax}** %\n'
                              '- С вашего счёта снимут **{money_with_tax}** {currency_emoji}',
                        'uk': '*Ви точно хочете надіслати **{money}** {currency_emoji} на рахунок **{user}**?*\n\n- Податок становить **{tax}** %\n- З вашого рахунку знімуть **{money_with_tax}** {currency_emoji}'}

    class Rename:
        scd_title = {'en': 'You renamed the pig',
                     'ru': 'Вы переименовали хряка',
                     'uk': 'Ви перейменували хряка'}
        scd_desc = {'en': '- *The new name of your pig: **{pig}***',
                    'ru': '- *Новое имя вашего хряка: **{pig}***',
                    'uk': "- *Нове ім'я вашого хряка: **{pig}***"}

    class Profile:
        profile_title = {'en': 'Profile of {user}',
                         'ru': 'Профиль {user}',
                         'uk': 'Профіль {user}'}
        user_profile_desc = {'en': '> Balance: **{coins}** 🪙 **{hollars}** 💵\n'
                                   '> Reputation: **{likes}** {rating_status} **|** {pos_amount} - {neg_amount}',
                             'ru': '> Баланс: **{coins}** 🪙 **{hollars}** 💵\n'
                                   '> Репутация: **{likes}** {rating_status} **|** {pos_amount} - {neg_amount}\n',
                             'uk': '> Баланс: **{coins}** 🪙 **{hollars}** 💵\n> Репутація: **{likes}** {rating_status} **|** {pos_amount} - {neg_amount}\n'}
        pig_profile_desc = {'en': '> Pig name: **{pig_name}**\n'
                                  '> Age: **{age}**\n'
                                  '> Weight: **{weight}** kg',
                            'ru': '> Имя хряка: **{pig_name}**\n'
                                  '> Возраст: **{age}**\n'
                                  '> Вес: **{weight}** кг',
                            'uk': "> Ім'я хряка: **{pig_name}**\n> Вік: **{age}**\n> Вага: **{weight}** кг"}
        family_profile_desc = {'en': '> Role: **{role}**',
                               'ru': '> Роль: **{role}**',
                               'uk': '> Роль: **{role}**'}
        pig_field_title = {'en': 'Pig',
                           'ru': 'Свинтус',
                           'uk': 'Свинтус'}
        pig_field_value = {'en': 'Pig name: **{pig_name}**\n'
                                 'Weight: **{weight}** kg',
                           'ru': 'Имя хряка: **{pig_name}**\n'
                                 'Вес: **{weight}** кг',
                           'uk': "Ім'я хряка: **{pig_name}**\nВага: **{weight}** кг"}

    class View:
        title = {'en': 'Pig of {user}',
                 'ru': 'Хряк {user}',
                 'uk': 'Хряк {user}'}

    class ProfileLike:
        scd_title = {'en': 'Liked',
                     'ru': 'Лайк поставлен',
                     'uk': 'Лайк поставлено'}
        scd_desc = {'en': "*You liked **{user}'s** profile*",
                    'ru': '*Вам понравился профиль **{user}***',
                    'uk': '*Вам сподобався профіль **{user}***'}
        already_put_title = {'en': 'No no no',
                             'ru': 'Эй, нельзя',
                             'uk': 'Гей, не можна'}
        already_put_desc = {'en': "*You can't like the same profile twice*",
                            'ru': '*Вы не можете поставить лайк 2 раза*',
                            'uk': '*Ви не можете поставити лайк 2 рази*'}

    class Top:
        best_of_the_bests = {'en': 'Best of the bests',
                             'ru': 'Лучшие из лучших',
                             'uk': 'Найкращі з найкращих'}
        also_not_bad = {'en': 'Also not bad',
                        'ru': 'Тоже неплохи',
                        'uk': 'Теж непогані'}
        weight_top_title = {'en': 'Weight top',
                            'ru': 'Топ по весу',
                            'uk': 'Топ за вагою'}
        weight_top_desc = {'en': "*Featuring the world's heaviest pigs*",
                           'ru': '*Здесь у нас самые жирные Хряки в мире*',
                           'uk': '*Тут у нас найжирніші Хряки у світі*'}
        coins_top_title = {'en': 'Money top',
                           'ru': 'Монетный топ',
                           'uk': 'Монетний топ'}
        coins_top_desc = {'en': '*Here we have the richest coin millionaires*',
                          'ru': '*Здесь у нас самые богатые монетные миллионеры*',
                          'uk': '*Тут у нас найбагатші монетні мільйонери*'}
        hollars_top_title = {'en': 'Dollar top',
                             'ru': 'Долларовый топ',
                             'uk': 'Доларовий топ'}
        hollars_top_desc = {'en': '*Here we have the richest dollar millionaires*',
                            'ru': '*Здесь у нас самые богатые долларовые миллионеры*',
                            'uk': '*Тут у нас найбагатші доларові мільйонери*'}
        streak_top_title = {'en': 'Streak top',
                            'ru': 'Стриковый топ',
                            'uk': 'Стріковий топ'}
        streak_top_desc = {'en': '*Here we have the hottest users*',
                           'ru': '*Здесь у нас самые горячие пользователи*',
                           'uk': '*Тут у нас найгарячіші користувачі*'}
        your_position = {'en': '*Your current ranking: **{place}*** ',
                         'ru': '*Ваше место: **{place}***',
                         'uk': '*Ваше місце: **{place}***'}
        placeholder = {'en': 'View profile',
                       'ru': 'Посмотреть профиль',
                       'uk': 'Переглянути профіль'}

    class Buffs:
        main_page_title = {'en': 'Buffs',
                           'ru': 'Баффы',
                           'uk': 'Бафи'}
        main_page_desc = {'en': '*Buffs applied to your pig are shown here*',
                          'ru': '*Здесь показываются баффы, примененные к вашему Хряку*',
                          'uk': '*Тут показуються бафи, застосовані до вашого Хряка*'}
        main_page_no_buffs_desc = {'en': '- *It seems you don\'t have any buffs applied*',
                                   'ru': '- *Кажется, у вас нету никаких примененных баффов*',
                                   'uk': '- *Здається, у вас немає жодних застосованих бафів*'}
        buff_expires_in = {'en': '  - *Expires <t:{expiration_timestamp}:R>*',
                           'ru': '  - *Истекает <t:{expiration_timestamp}:R>*',
                           'uk': '  - *Спливає <t:{expiration_timestamp}:R>*'}
        weight_buffs_desc = {'en': "*Your weight gain multipliers are shown here*",
                             'ru': '*Здесь показываются множители вашего весо-набирания*',
                             'uk': '*Тут показуються множники вашого набору ваги*'}
        pooping_buffs_desc = {'en': "*This shows the multipliers for how much manure the pig will produce per feeding*",
                              'ru': '*Здесь показываются множители того, сколько Хряк будет производить навоза за 1 кормежку*',
                              'uk': '*Тут показуються множники того, скільки Хряк вироблятиме гною за 1 годування*'}
        vomit_chance_desc = {'en': "*Here you can see the chance that the pig will vomit while feeding*",
                             'ru': '*Здесь показываются шанс того что Хряка стошнит при кормежке*',
                             'uk': '*Тут показується шанс того, що Хряка знудить при годуванні*'}
        base_multiplier_value = {'en': "Base value: **{mult}%**",
                                 'ru': 'Базовое значение: **{mult}%**',
                                 'uk': 'Базове значення: **{mult}%**'}
        final_multiplier_value = {'en': "Final value: **{mult}%**",
                                  'ru': 'Финальное значение: **{mult}%**',
                                  'uk': 'Фінальне значення: **{mult}%**'}

    class Help:
        description = {'en-US': 'Get help for bot',
                       'ru': 'Хряковое пособие и обучение'}
        basic_help_title = {'en': 'Getting Started',
                            'ru': 'С чего начать?',
                            'uk': 'З чого почати?'}
        basic_help_desc = {
            'en': '*The main essence of the bot is feeding and clothing the pig*\n\n'
                  '1. To start playing, enter the command </feed:1118970976282095676>. Your pig will gain some weight, and you will also receive some manure in your inventory\n\n'
                  '2. To open the inventory, use </inventory:1107272196931461173>. In the inventory, you can sell and use your items\n'
                  '  - You can try to sell manure or open a case\n\n'
                  '3. Your balance and the weight of the pig will be displayed in </profile:1107272196931461171>\n\n'
                  '4. After earning money, you can spend it in </shop:1107272196931461175>\n'
                  '  - In the shop, you can buy various skins and boosts for the pig\n\n'
                  '5. To dress the pig, use </wardrobe:1107272196931461174>. Then select an item and press the **Wear** button\n\n'
                  f'> If you have additional questions, visit the [support server]({config.BOT_GUILDS[config.EN_BOT_GUILD_ID]['url']})',
            'ru': '*Основная суть бота в кормлении и одевании хряка*\n\n'
                  '1. Чтобы начать играть, введите команду </feed:1118970976282095676>. Ваш хряк наберёт несколько килограмм веса, а также вы получите немного навоза в ваш инвентарь\n\n'
                  '2. Чтобы открыть инвентарь, используйте </inventory:1107272196931461173>. В инвентаре можно продавать и использовать ваши предметы\n'
                  '  - Можете попробовать продать навоз либо открыть кейс\n\n'
                  '3. Ваш баланс и вес хряка будет отображаться в </profile:1107272196931461171>\n\n'
                  '4. После получения денег, вы можете потратить их в </shop:1107272196931461175>\n'
                  '  - В магазине вы сможете купить различные скины и бусты для хряка\n\n'
                  '5. Чтобы одеть хряка, используйте </wardrobe:1107272196931461174>. Затем выберите предмет и нажмите на кнопку **Надеть**\n\n'
                  f'> Если есть дополнительные вопросы, заходите на [сервер поддержки]({config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']})',
            'uk': None}

    class Say:
        not_allowed_title = {'en': 'Forbidden',
                             'ru': 'Нельзя',
                             'uk': 'Не можна'}
        not_allowed_desc = {
            'en': '*Command `/say` is currently disabled on this server. Ask the admin to enable it with `/settings say`*',
            'ru': '*Команда `/say` отключена на этом сервере. Попросите администрацию включить её при помощи `/settings say`*',
            'uk': '*Команду `/say` вимкнено на цьому сервері. Попросіть адміністрацію увімкнути її за допомогою `/settings say`*'}

    class SettingsSay:
        scd_content = {'en': '*Settings for the `/say` command have been changed and set to `{value}`*',
                    'ru': '*Настройки для команды `/say` изменены и выставлены на `{value}`*',
                    'uk': '*Налаштування для команди `/say` змінено та виставлено на `{value}`*'}


    class SettingsTop:
        scd_content = {'en': '*Participation settings for the `/top` command have been changed and set to `{value}`*',
                    'ru': '*Настройки участия для команды `/top` изменены и выставлены на `{value}`*',
                    'uk': '*Налаштування участі для команди `/top` змінено та виставлено на `{value}`*'}

    class Report:
        title = {
            'en': 'Report sent!',
            'ru': 'Ваш репорт был отправлен',
            'uk': 'Ваш репорт було надіслано'}
        desc = {
            'en': "Thanks for contributing to the bot's development\n\n"
                  f"*Support server: {config.BOT_GUILDS[config.EN_BOT_GUILD_ID]['url']}*",
            'ru': 'Хряк доволен за твою помощь, спасибо\n\n'
                  f'*Сервер поддержки: {config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']}*',
            'uk': None}

    class ChooseLanguage:
        title = {'en': 'Choose language',
                 'ru': 'Сначала выбери язык',
                 'uk': 'Спочатку обери мову'}
        desc = {'en': 'Select the language the bot will use',
                'ru': 'Выбери язык на котором бот будет хрюкать',
                'uk': 'Обери мову, якою бот буде хрюкати'}
        placeholder = {'en': 'Choose language',
                       'ru': 'Выберите язык',
                       'uk': 'Оберіть мову'}

    class SetLanguage:
        scd_title = {
            'en': 'New bot language: **English**',
            'ru': 'Новый язык бота: **Русский**',
            'uk': 'Нова мова бота: **Українська**'
        }
        scd_desc = {
            'en': 'Now the bot will speak the language of freedom 🦅🦅',
            'ru': 'Теперь бот будет говорить на великом и могучем 💪',
            'uk': "Тепер бот говоритиме солов'їною 🇺🇦"
        }

    class PromoCode:
        promo_code_used_error_title = {'en': 'You have already used this promo code',
                                       'ru': 'Вы уже использовали этот промо код',
                                       'uk': 'Ви вже використали цей промокод'}
        promo_code_used_error_desc = {
            'en': "*Trying to be clever? Promo codes can't be used more than once*",
            'ru': '*Самый умный? Нельзя использовать один и тот же промо код несколько раз*',
            'uk': '*Найрозумніший? Не можна використовувати один і той самий промокод декілька разів*'}
        promocode_not_exist_title = {'en': 'Invalid promo code',
                                     'ru': 'Недействительный промо код',
                                     'uk': 'Недійсний промокод'}
        promocode_not_exist_desc = {
            'en': '*The entered promo code does not exist*',
            'ru': '*Такого промо кода не существует*',
            'uk': '*Такого промокоду не існує*'}
        cant_use_promocode_title = {'en': 'Invalid promo code',
                                    'ru': 'Невозможно использовать промокод',
                                    'uk': 'Неможливо використати промокод'}
        cant_use_promocode_desc = {
            'en': "*For some reason you can't use this promo code*",
            'ru': '*По какой-то причине вы не можете использовать этот промокод*',
            'uk': '*З якоїсь причини ви не можете використати цей промокод*'}
        promocode_expired_title = {'en': 'Promo code has expired',
                                   'ru': 'Промо код истёк',
                                   'uk': 'Промокод минув'}
        promocode_expired_desc = {
            'en': "*The promo code has expired and is therefore no longer valid.*",
            'ru': '*Срок годности промокода истёк, поэтому он больше не рабочий*',
            'uk': '*Термін дії промокоду минув, тому він більше не працює*'}
        promocode_used_too_many_times_title = {'en': 'Invalid promo code',
                                               'ru': 'Промо код использован',
                                               'uk': 'Промокод використано'}
        promocode_used_too_many_times_desc = {
            'en': 'This promo code has already been used and is therefore no longer valid.',
            'ru': 'Этот промо код уже использовали, поэтому он больше недействителен',
            'uk': 'Цей промокод уже використали, тому він більше недійсний'}
        promo_code_used_title = {'en': 'Promo code used',
                                 'ru': 'Промо код активирован',
                                 'uk': 'Промокод активовано'}
        you_got_desc = {'en': 'You got:',
                        'ru': 'Вы получили:',
                        'uk': 'Ви отримали:'}

    class PoopEaten:
        not_enough_money_for_doctor_title = {'en': 'Not enough money',
                                             'ru': 'Недостаточно средств',
                                             'uk': 'Недостатньо коштів'}
        not_enough_money_for_doctor_desc = {'en': "You don't have enough money to pay the doctor\n\n"
                                                  '- *Doctor takes pity on a beggar like you and just walks away*',
                                            'ru': 'У вас не хватает денег, чтобы заплатить доктору\n\n'
                                                  '- *Доктор жалеет такого нищего как вы и просто уходит*',
                                            'uk': 'У вас не вистачає грошей, щоб заплатити лікарю\n\n- *Лікар жаліє такого жебрака, як ви, і просто йде*'}
        ran_away_and_not_payed_title = {'en': 'You ran away',
                                        'ru': 'Вы сбежали',
                                        'uk': 'Ви втекли'}
        ran_away_and_not_payed_desc = {'en': "*You managed to escape. It looks like no one is following you*",
                                       'ru': '*Вы смогли сбежать. Кажется никого позади нету*',
                                       'uk': '*Вам вдалося втекти. Здається, позаду нікого немає*'}
        payed_to_doctor_title = {'en': 'You paid the doctor',
                                 'ru': 'Вы заплатили доктору',
                                 'uk': 'Ви заплатили лікарю'}
        payed_to_doctor_desc = {'en': '*The doctor took the money and left*',
                                'ru': '*Доктор взял деньги и уехал*',
                                'uk': '*Лікар взяв гроші та поїхав*'}

    class RateBot:
        title = {'en': 'Hey, do you like the bot?',
                 'ru': 'Эй, нравится бот?',
                 'uk': 'Гей, подобається бот?'}
        desc = {'en': 'If so, feel free to rate it on our website',
                'ru': 'Если да, то можешь оценить его на сайте',
                'uk': 'Якщо так, то можеш оцінити його на сайті'}
        later_btn = {'en': 'Later',
                     'ru': 'Позже',
                     'uk': 'Пізніше'}
        support_btn = {'en': 'Support',
                       'ru': 'Оценить',
                       'uk': 'Оцінити'}

    class Pagination:
        page = {'en': 'Page',
                'ru': 'Страница',
                'uk': 'Сторінка'}
        next = {'en': 'Next',
                'ru': 'Следующая',
                'uk': 'Наступна'}
        previous = {'en': 'Previous',
                    'ru': 'Предыдущая',
                    'uk': 'Попередня'}
        select_category = {'en': 'Select category',
                            'ru': 'Выберите категорию',
                            'uk': 'Оберіть категорію'}
        wrong_user_title = {'en': 'Hey, it\'s not your message',
                            'ru': 'Эй, это не твоё сообщение',
                            'uk': 'Гей, це не твоє повідомлення'}
        wrong_user_desc = {'en': "*You cannot simply flip through other people's pages*",
                           'ru': '*Ты не можешь просто взять и листать чужие страницы*',
                           'uk': '*Ти не можеш просто взяти й гортати чужі сторінки*'}

    class Global:
        balance = {'en': 'Balance',
                   'ru': 'Баланс',
                   'uk': 'Баланс'}
        page = {'en': 'Page',
                'ru': 'Страница',
                'uk': 'Сторінка'}
        shop = {'en': 'Shop',
                'ru': 'Магазин',
                'uk': 'Магазин'}
        money = {'en': 'Money',
                 'ru': 'Деньги',
                 'uk': 'Гроші'}
        clear = {'en': 'Clear',
                 'ru': 'Очистить',
                 'uk': 'Очистити'}
        inventory = {'en': 'Inventory',
                     'ru': 'Инвентарь',
                     'uk': 'Інвентар'}
        wardrobe = {'en': 'Wardrobe',
                    'ru': 'Гардероб',
                    'uk': 'Гардероб'}
        no_items = {'en': 'No items',
                    'ru': 'Нету предметов',
                    'uk': 'Немає предметів'}
        successfully = {'en': 'Successfully',
                        'ru': 'Успешно',
                        'uk': 'Успішно'}
        trade = {'en': 'Trade',
                 'ru': 'Торговля',
                 'uk': 'Торгівля'}
        like = {'en': 'Like',
                'ru': 'Нравится',
                'uk': 'Подобається'}
        kick = {'en': 'Kick',
                'ru': 'Выгнать',
                'uk': 'Вигнати'}
        ban = {'en': 'Ban',
               'ru': 'Бан',
               'uk': 'Бан'}
        date = {'en': 'Date',
                'ru': 'Дата',
                'uk': 'Дата'}
        requests = {'en': 'Requests',
                    'ru': 'Запросы',
                    'uk': 'Запити'}
        sent = {'en': 'Sent',
                'ru': 'Отправлено',
                'uk': 'Надіслано'}
        are_you_sure = {'en': 'Are you sure?',
                        'ru': 'Вы уверены?',
                        'uk': 'Ви впевнені?'}
        cost = {'en': 'Cost',
                'ru': 'Цена',
                'uk': 'Ціна'}
        cost_per_item = {'en': 'Price/pc',
                         'ru': 'Цена/шт',
                         'uk': 'Ціна/шт'}
        price = {'en': 'Price',
                 'ru': 'Стоимость',
                 'uk': 'Вартість'}
        type = {'en': 'Type',
                'ru': 'Тип',
                'uk': 'Тип'}
        amount = {'en': 'Amount',
                  'ru': 'Количество',
                  'uk': 'Кількість'}
        description = {'en': 'Description',
                       'ru': 'Описание',
                       'uk': 'Опис'}
        resource = {'en': 'Resource',
                    'ru': 'Ресурс',
                    'uk': 'Ресурс'}
        head_owner = {'en': 'Owner',
                      'ru': 'Глава',
                      'uk': 'Глава'}
        use = {'en': 'Use',
               'ru': 'Использовать',
               'uk': 'Використати'}
        sell = {'en': 'Sell',
                'ru': 'Продать',
                'uk': 'Продати'}
        run_away = {'en': 'Run away',
                    'ru': 'Сбежать',
                    'uk': 'Втекти'}
        pay = {'en': 'Pay',
               'ru': 'Заплатить',
               'uk': 'Заплатити'}
        preview = {'en': 'Preview',
                   'ru': 'Предосмотр',
                   'uk': 'Передперегляд'}
        wear = {'en': 'Wear',
                'ru': 'Надеть',
                'uk': 'Надіти'}
        remove_cloth = {'en': 'Remove',
                        'ru': 'Снять',
                        'uk': 'Зняти'}
        rarity = {'en': 'Rarity',
                  'ru': 'Редкость',
                  'uk': 'Рідкість'}
        accept = {'en': 'Accept',
                  'ru': 'Принять',
                  'uk': 'Прийняти'}
        reject = {'en': 'Reject',
                  'ru': 'Отклонить',
                  'uk': 'Відхилити'}
        buy = {'en': 'Buy',
               'ru': 'Купить',
               'uk': 'Купити'}
        reason = {'en': 'Reason',
                  'ru': 'Причина',
                  'uk': 'Причина'}
        created = {'en': 'Created',
                   'ru': 'Создан',
                   'uk': 'Створено'}
        owner = {'en': 'Owner',
                 'ru': 'Владелец',
                 'uk': 'Власник'}
        icon = {'en': 'Icon',
                'ru': 'Аватарка',
                'uk': 'Аватарка'}
        nicknames = {'en': 'Nicknames',
                     'ru': 'Никнеймы',
                     'uk': 'Ніки'}
        no_icon = {'en': 'No Icon',
                   'ru': 'Без Аватарки',
                   'uk': 'Без Аватарки'}
        need = {'en': 'Need',
                'ru': 'Нужно',
                'uk': 'Потрібно'}
        channels = {'en': 'Channels',
                    'ru': 'Каналы',
                    'uk': 'Канали'}
        total = {'en': 'Total',
                 'ru': 'Всего',
                 'uk': 'Усього'}
        open = {'en': 'Open',
                'ru': 'Открыть',
                'uk': 'Відкрити'}
        category = {'en': 'Category',
                    'ru': 'Категорий',
                    'uk': 'Категорій'}
        text = {'en': 'Text',
                'ru': 'Текстовых',
                'uk': 'Текстових'}
        voice = {'en': 'Voice',
                 'ru': 'Голосовых',
                 'uk': 'Голосових'}
        forum = {'en': 'Forum',
                 'ru': 'Форум',
                 'uk': 'Форум'}
        stage = {'en': 'Stage',
                 'ru': 'Трибуны',
                 'uk': 'Трибуни'}
        members = {'en': 'Members',
                   'ru': 'Участники',
                   'uk': 'Учасники'}
        users = {'en': 'Users',
                 'ru': 'Людей',
                 'uk': 'Людей'}
        bots = {'en': 'Bots',
                'ru': 'Ботов',
                'uk': 'Ботів'}
        bot_roles = {'en': 'Bot roles',
                     'ru': 'Ролей ботов',
                     'uk': 'Ролей ботів'}
        premium = {'en': 'Premium',
                   'ru': 'Премиум',
                   'uk': 'Преміум'}
        role = {'en': 'Role',
                'ru': 'Роль',
                'uk': 'Роль'}
        roles = {'en': 'Roles',
                 'ru': 'Роли',
                 'uk': 'Ролі'}
        bans = {'en': 'Bans',
                'ru': 'Баны',
                'uk': 'Бани'}
        messages = {'en': 'Messages',
                    'ru': 'Сообщения',
                    'uk': 'Повідомлення'}
        invites = {'en': 'Invites',
                   'ru': 'Приглашения',
                   'uk': 'Запрошення'}
        expires = {'en': 'Expires',
                   'ru': 'Истекает',
                   'uk': 'Спливає'}
        animated = {'en': 'Animated',
                    'ru': 'Анимированых',
                    'uk': 'Анімованих'}
        stickers = {'en': 'Stickers',
                    'ru': 'Стикеров',
                    'uk': 'Стікерів'}
        no_emojis = {'en': 'No emojis',
                     'ru': 'Нету эмодзи',
                     'uk': 'Немає емодзі'}
        emojis = {'en': 'Emojis',
                  'ru': 'Эмодзи',
                  'uk': 'Емодзі'}
        system_channel = {'en': 'System channel',
                          'ru': 'Системный канал',
                          'uk': 'Системний канал'}
        join_messages = {'en': 'Join messages',
                         'ru': 'Нач. сообщения',
                         'uk': 'Поч. повідомлення'}
        join_replies = {'en': 'Join replies',
                        'ru': 'Ответы',
                        'uk': 'Відповіді'}
        boost_messages = {'en': 'Boost messages',
                          'ru': 'Буст уведомления',
                          'uk': 'Буст сповіщення'}
        reminder = {'en': 'Reminder',
                    'ru': 'Напоминания',
                    'uk': 'Нагадування'}
        limits = {'en': 'Limits',
                  'ru': 'Лимиты',
                  'uk': 'Ліміти'}
        emojis_limit = {'en': 'Emojis limit',
                        'ru': 'Лимит эмодзи',
                        'uk': 'Ліміт емодзі'}
        stickers_limit = {'en': 'Stickers limit',
                          'ru': 'Лимит стикеров',
                          'uk': 'Ліміт стікерів'}
        bitrate_limit = {'en': 'Bitrate limit',
                         'ru': 'Лимит битрейта',
                         'uk': 'Ліміт бітрейта'}
        files_limit = {'en': 'Files limit',
                       'ru': 'Лимит файлов',
                       'uk': 'Ліміт файлів'}
        safety = {'en': 'Safety',
                  'ru': 'Безопасность',
                  'uk': 'Безпека'}
        mfa = {'en': 'MFA',
               'ru': 'MFA',
               'uk': 'MFA'}
        attempt = {'en': 'Attempt',
                   'ru': 'Попытка',
                   'uk': 'Спроба'}
        verification = {'en': 'Verification',
                        'ru': 'Верификация',
                        'uk': 'Верифікація'}
        nsfw_level = {'en': 'NSFW level',
                      'ru': 'Уровень NSFW',
                      'uk': 'Рівень NSFW'}
        content_filter = {'en': 'Content filter',
                          'ru': 'Фильтр контента',
                          'uk': 'Фільтр контенту'}
        default_notifications = {'en': 'Default notifications',
                                 'ru': 'Уведомления по умолчанию',
                                 'uk': 'Сповіщення за замовчуванням'}
        other = {'en': 'Other',
                 'ru': 'Другое',
                 'uk': 'Інше'}
        yes = {'en': 'Yes',
               'ru': 'Да',
               'uk': 'Так'}
        no = {'en': 'No',
              'ru': 'Нет',
              'uk': 'Ні'}
        true_yes_command = {'en': '✅ True',
                            'ru': '✅ Да',
                            'uk': '✅ Так'}
        false_no_command = {'en': '❌ False',
                            'ru': '❌ Нет',
                            'uk': '❌ Ні'}
        total_bans = {'en': 'Total Bans',
                      'ru': 'Всего банов',
                      'uk': 'Усього банів'}
        total_invites = {'en': 'Total Invites',
                         'ru': 'Всего приглашений',
                         'uk': 'Усього запрошень'}
        locale = {'en': 'Locale',
                  'ru': 'Язык',
                  'uk': 'Мова'}
        rules = {'en': 'Rules',
                 'ru': 'Правила',
                 'uk': 'Правила'}
        community = {'en': 'Community',
                     'ru': 'Комьюнити',
                     'uk': "Ком'юніті"}
        click = {'en': 'Click',
                 'ru': 'Нажми',
                 'uk': 'Натисни'}
        joined = {'en': 'Joined',
                  'ru': 'Присоединился',
                  'uk': 'Приєднався'}
        name_ = {'en': 'Name',
                 'ru': 'Имя',
                 'uk': "Ім'я"}
        status = {'en': 'Status',
                  'ru': 'Статус',
                  'uk': 'Статус'}
        play = {'en': 'Playing',
                'ru': 'Играет в',
                'uk': 'Грає в'}
        stream = {'en': 'Streaming',
                  'ru': 'Стримит',
                  'uk': 'Стрімить'}
        listen = {'en': 'Listening',
                  'ru': 'Слушает',
                  'uk': 'Слухає'}
        watching = {'en': 'Watching',
                    'ru': 'Смотрит',
                    'uk': 'Дивиться'}
        competing = {'en': 'Competing in',
                     'ru': 'Соревнуется в',
                     'uk': 'Змагається в'}
        never = {'en': 'Never',
                 'ru': 'Никогда',
                 'uk': 'Ніколи'}
        total_members = {'en': 'Total members',
                         'ru': 'Всего участников',
                         'uk': 'Усього учасників'}
        position = {'en': 'Position',
                    'ru': 'Позиция',
                    'uk': 'Позиція'}
        last_update = {'en': 'Last update',
                       'ru': 'Последнее обновление',
                       'uk': 'Останнє оновлення'}
        uses = {'en': 'Uses',
                'ru': 'Использований',
                'uk': 'Використань'}
        cook = {'en': 'Cook',
                'ru': 'Приготовить',
                'uk': 'Приготувати'}
        total_roles = {'en': 'Total roles',
                       'ru': 'Всего ролей',
                       'uk': 'Усього ролей'}
        total_channels = {'en': 'Total channels',
                          'ru': 'Всего каналов',
                          'uk': 'Усього каналів'}
        template_info = {'en': 'Template info',
                         'ru': 'О шаблоне',
                         'uk': 'Про шаблон'}
        source_guild_id = {'en': 'Source server ID',
                           'ru': 'ID исходного сервера',
                           'uk': 'ID вихідного сервера'}
        creator_id = {'en': 'Creator ID',
                      'ru': 'ID создателя',
                      'uk': 'ID створювача'}
        your_number = {'en': 'Your number',
                       'ru': 'Ваше число',
                       'uk': 'Ваше число'}
        numbers = {'en': 'Numbers',
                   'ru': 'Числа',
                   'uk': 'Числа'}
        color = {'en': 'Color',
                 'ru': 'Цвет',
                 'uk': 'Колір'}
        weight = {'en': 'Weight',
                  'ru': 'Вес',
                  'uk': 'Вага'}
        template = {'en': 'Template',
                    'ru': 'Шаблон',
                    'uk': 'Шаблон'}
        templates = {'en': 'Templates',
                     'ru': 'Шаблоны',
                     'uk': 'Шаблони'}
        creator = {'en': 'Creator',
                   'ru': 'Создатель',
                   'uk': 'Створювач'}
        options = {'en': 'Options',
                   'ru': 'Настройки',
                   'uk': 'Налаштування'}
        mentionable = {'en': 'Mentionable',
                       'ru': 'Упоминаимая',
                       'uk': 'Згадувана'}
        hoist = {'en': 'Hoist',
                 'ru': 'Отдельная',
                 'uk': 'Окрема'}
        integration = {'en': 'Integration',
                       'ru': 'Интеграция',
                       'uk': 'Інтеграція'}
        refresh = {'en': 'Refresh',
                   'ru': 'Обновить',
                   'uk': 'Оновити'}
        reload = {'en': 'Reload',
                  'ru': 'Перезагрузить',
                  'uk': 'Перезавантажити'}
        links = {'en': 'Links',
                 'ru': 'Ссылки',
                 'uk': 'Посилання'}
        title = {'en': 'Title',
                 'ru': 'Заголовок',
                 'uk': 'Заголовок'}
        footer = {'en': 'Footer',
                  'ru': 'Нижний текст',
                  'uk': 'Нижній текст'}
        image_url = {'en': 'Image URL',
                     'ru': 'Ссылка на картинку',
                     'uk': 'Посилання на картинку'}
        thumbnail_url = {'en': 'Thumbnail URL',
                         'ru': 'Ссылка на маленькую картинку',
                         'uk': 'Посилання на маленьку картинку'}
        stats = {'en': 'Stats',
                 'ru': 'Статистика',
                 'uk': 'Статистика'}
        all_skins = {'en': 'All skins',
                     'ru': 'Все скины',
                     'uk': 'Усі скіни'}
        all_items = {'en': 'All items',
                     'ru': 'Все вещи',
                     'uk': 'Усі речі'}
        everything = {'en': 'Everything',
                      'ru': 'Показать всё',
                      'uk': 'Показати все'}
        got_it_btn = {'en': 'Got it',
                      'ru': 'Хорошо',
                      'uk': 'Добре'}
        choose_category = {'en': 'Select category',
                           'ru': 'Выберите категорию',
                           'uk': 'Оберіть категорію'}
        none = {'en': 'No',
                'ru': 'Нету',
                'uk': 'Немає'}
        message = {'en': 'Message',
                   'ru': 'Сообщение',
                   'uk': 'Повідомлення'}
        you_have_amount = {'en': 'You have: {max_amount}',
                           'ru': 'У вас есть: {max_amount}',
                           'uk': 'У вас є: {max_amount}'}

    class ErrorCallbacks:
        pig_feed_cooldown_title = {'en': 'Your pig is not yet hungry',
                                   'ru': 'Ваш хряк ещё не голоден',
                                   'uk': 'Ваш хряк ще не голодний'}
        pig_feed_cooldown_desc = {'en': '***{pig}** will be hungry again **<t:{timestamp}:R>***',
                                  'ru': '***{pig}** проголодается **<t:{timestamp}:R>***',
                                  'uk': '***{pig}** зголодніє **<t:{timestamp}:R>***'}
        pig_butcher_cooldown_title = {'en': 'You are so cruel',
                                      'ru': 'Вы слишком жестокие',
                                      'uk': 'Ви занадто жорстокі'}
        pig_butcher_cooldown_desc = {'en': "You can't butcher **{pig}** so often\n\n"
                                           "Try again **<t:{timestamp}:R>**",
                                     'ru': 'Вы не можете так часто снимать сало с **{pig}**\n\n'
                                           '*Попробуйте ещё раз **<t:{timestamp}:R>***',
                                     'uk': 'Ви не можете так часто зрізати сало з **{pig}**\n\n*Спробуйте ще раз **<t:{timestamp}:R>***'}
        pig_breed_cooldown_title = {'en': 'Calm down',
                                    'ru': 'Успокойся',
                                    'uk': 'Заспокойся'}
        pig_breed_cooldown_desc = {'en': "**{pig}** is too tired and can't have kids\n"
                                         "Try again **<t:{timestamp}:R>**",
                                   'ru': '**{pig}** слишком устал и не может заводить детей\n\n'
                                         '*Попробуйте ещё раз **<t:{timestamp}:R>***',
                                   'uk': '**{pig}** занадто втомився і не може заводити дітей\n\n*Спробуйте ще раз **<t:{timestamp}:R>***'}
        shop_buy_cooldown_title = {'en': 'Product is out of stock',
                                   'ru': 'Товар закончился',
                                   'uk': 'Товар закінчився'}
        shop_buy_cooldown_desc = {'en': "**{item}** is out of stock\n\n"
                                        "*New product will arrive **<t:{timestamp}:R>***",
                                  'ru': '**{item}** закончился и его больше нету на складе\n\n'
                                        '*Новый товар привезут **<t:{timestamp}:R>***',
                                  'uk': '**{item}** закінчився і його більше немає на складі\n\n*Новий товар привезуть **<t:{timestamp}:R>***'}
        wrong_component_clicked_title = {'en': "It's not your message",
                                         'ru': 'Это не ваше сообщение',
                                         'uk': 'Це не ваше повідомлення'}
        wrong_component_clicked_desc = {'en': "*You can't push tie people's buttons*",
                                        'ru': '*Ты не можешь нажимать на чужие кнопки*',
                                        'uk': '*Ти не можеш натискати на чужі кнопки*'}
        skin_not_compatible_title = {'en': "Can't be worn",
                                     'ru': 'Нельзя надеть',
                                     'uk': 'Не можна надіти'}
        skin_not_compatible_desc = {
            'en': '***{skin1}** conflicts with **{skin2}**\n\n> Remove **{skin2}** to put on **{skin1}***',
            'ru': '***{skin1}** конфликтует с **{skin2}**\n\n> Снимите **{skin2}**, чтобы надеть **{skin1}***',
            'uk': '***{skin1}** конфліктує з **{skin2}**\n\n> Зніміть **{skin2}**, щоб надіти **{skin1}***'}
        not_enough_money_title = {'en': 'Not enough money',
                                  'ru': 'Недостаточно денег',
                                  'uk': 'Недостатньо грошей'}
        not_enough_money_desc = {'en': "*You don't have enough money to do this*",
                                 'ru': '*У вас не достаточно денег, чтобы сделать это*',
                                 'uk': '*У вас недостатньо грошей, щоб зробити це*'}
        item_is_not_in_shop_title = {'en': 'No item',
                                     'ru': 'Нету предмета',
                                     'uk': 'Немає предмета'}
        item_is_not_in_shop_desc = {'en': '*This item is not in the shop. Try updating the command*',
                                    'ru': '*Этого предмета нету в магазине. Попробуйте обновить команду*',
                                    'uk': '*Цього предмета немає в магазині. Спробуйте оновити команду*'}
        no_item_title = {'en': "You don't have a {item}",
                         'ru': 'У вас нету предмета "{item}"',
                         'uk': 'У вас немає предмета "{item}"'}
        no_item_desc = {'en': "*Unfortunately, you couldn't find this item in your storage*",
                        'ru': '*К сожалению, вы не смогли найти этот предмет у себя в хранилище*',
                        'uk': '*На жаль, ви не змогли знайти цей предмет у себе в сховищі*'}
        not_enough_item_title = {'en': "Not enough items",
                                 'ru': 'У вас не хватает предметов',
                                 'uk': 'У вас не вистачає предметів'}
        not_enough_item_desc = {'en': "*Unfortunately, you couldn't find enough amount in your storage:*\n\n"
                                      "> {item_emoji}・{item}",
                                'ru': '*К сожалению, вы не смогли найти нужное количество у себя в хранилище:*\n\n'
                                      '> {item_emoji}・{item}',
                                'uk': '*На жаль, ви не змогли знайти потрібну кількість у себе в сховищі:*\n\n> {item_emoji}・{item}'}
        user_not_enough_item_title = {'en': "Not enough items",
                                      'ru': 'Не хватает предметов',
                                      'uk': 'Не вистачає предметів'}
        user_not_enough_item_desc = {'en': "*Unfortunately, **{user}** couldn't find enough amount in his storage*\n\n"
                                           "> {item_emoji}・{item}",
                                     'ru': '*К сожалению, **{user}** не смог найти нужное количество у себя в хранилище:*\n\n'
                                           '> {item_emoji}・{item}',
                                     'uk': '*На жаль, **{user}** не зміг знайти потрібну кількість у себе в сховищі:*\n\n> {item_emoji}・{item}'}
        not_allowed_to_use_command_title = {'en': "You are not allowed to use this command",
                                            'ru': 'Вам не разрешено использовать эту команду',
                                            'uk': 'Вам не дозволено використовувати цю команду'}
        not_allowed_to_use_command_desc = {'en': "*You need special permission to use the command*",
                                           'ru': '*Вам нужно специальное разрешение, чтобы использовать команду*',
                                           'uk': '*Вам потрібен спеціальний дозвіл, щоб використовувати команду*'}
        nsfw_required_title = {'en': "You are not allowed to use this command",
                               'ru': 'Это NSFW команда',
                               'uk': 'Це NSFW команда'}
        nsfw_required_desc = {'en': "*You need to be in an NSFW channel to use the command*",
                              'ru': '*Вам нужно находится в NSFW канале, чтобы использовать команду*',
                              'uk': '*Вам потрібно перебувати в NSFW каналі, щоб використовувати команду*'}
        no_private_message_title = {'en': "Servers only",
                                    'ru': 'Только для серверов',
                                    'uk': 'Тільки для серверів'}
        no_private_message_desc = {'en': "*You need to be on the server to use the command*",
                                   'ru': '*Вам нужно находится на сервере, чтобы использовать команду*',
                                   'uk': '*Вам потрібно перебувати на сервері, щоб використовувати команду*'}
        not_owner_desc = {'en': "*Only the bot owner can use this command*",
                          'ru': '*Только владелец бота может использовать эту команду*',
                          'uk': '*Тільки власник бота може використовувати цю команду*'}
        bot_as_opponent_duel_title = {'en': "Are you playing against a bot?",
                                      'ru': 'Ты против бота играешь?',
                                      'uk': 'Ти проти бота граєш?'}
        bot_as_opponent_duel_desc = {
            'en': "*I'll tell you a secret, bots don't know how to participate in duels. They can't even press a button.*",
            'ru': '*Расскажу секрет, боты не умеют участвовать в дуэлях. Они даже на кнопку нажать не могут*',
            'uk': '*Розкажу секрет, боти не вміють брати участь у дуелях. Вони навіть на кнопку натиснути не можуть*'}
        bot_as_partner_breed_title = {'en': "Going to have kids with a bot?",
                                      'ru': 'Собрался завести детей с ботом?',
                                      'uk': 'Зібрався завести дітей з ботом?'}
        bot_as_partner_breed_desc = {
            'en': "*The future is not close enough for you to breed with robots*",
            'ru': '*Будущее не настолько близко, чтобы вы могли заводить потомство с роботами*',
            'uk': '*Майбутнє не настільки близько, щоб ви могли заводити потомство з роботами*'}
        cant_play_with_yourself_duel_title = {'en': "Going to play by yourself?",
                                              'ru': 'Собрался играть сам с собой?',
                                              'uk': 'Зібрався грати сам із собою?'}
        cant_play_with_yourself_duel_desc = {'en': "*I thought users wouldn't choose themselves as opponents. "
                                                   "I think I was wrong*",
                                             'ru': '*Я думал что пользователи не станут выбирать самого себя в качестве соперника. '
                                                   'Кажется, я ошибался*',
                                             'uk': '*Я думав, що користувачі не обиратимуть самих себе як суперника. Здається, я помилявся*'}
        cant_breed_with_yourself_title = {'en': "Hey hey hey",
                                          'ru': 'Воу воу воу',
                                          'uk': 'Воу воу воу'}
        cant_breed_with_yourself_desc = {
            'en': "*I understand that you love yourself so much that you chose yourself as a partner, but unfortunately you can’t*",
            'ru': '*Я понимаю что вы любите себя настолько сильно что выбрали себя в качестве партнёра, но так к сожалению нельзя*',
            'uk': '*Я розумію, що ви любите себе настільки сильно, що обрали себе як партнера, але так, на жаль, не можна*'}
        cant_trade_with_yourself_title = {'en': "You can't trade with yourself",
                                          'ru': 'Нельзя торговать с собой',
                                          'uk': 'Не можна торгувати із собою'}
        cant_trade_with_yourself_desc = {
            'en': "*What are you going to inject yourself? Like \"Hey Me, let me sell you 10 coins for 10 coins\"?*",
            'ru': '*Что ты себе впаривать собрался? Типо "Эй Я, давай я тебе продам 10 монет за 10 монет"?*',
            'uk': '*Що ти собі впарювати зібрався? Типу "Гей Я, давай я тобі продам 10 монет за 10 монет"?*'}
        bot_as_trade_user_title = {'en': "Can't trade with a bot",
                                   'ru': 'Нельзя торговать с ботом',
                                   'uk': 'Не можна торгувати з ботом'}
        bot_as_trade_user_desc = {
            'en': "Hey, seriously. I'm already tired of reminding users that they can't interact with bots",
            'ru': '*Эй, ну серьезно. Мне уже надоело напоминать пользователям что они не могут взаимодействовать с ботами*',
            'uk': '*Гей, ну серйозно. Мені вже набридло нагадувати користувачам, що вони не можуть взаємодіяти з ботами*'}
        cooldown_title = {'en': "Cooldown",
                          'ru': 'Притормози',
                          'uk': 'Пригальмуй'}
        cooldown_desc = {'en': 'You use the command too often\n\n'
                               '- *Try again **<t:{timestamp}:R>***',
                         'ru': 'Ты слишком часто используешь команду\n\n'
                               '- *Попробуй ещё раз **<t:{timestamp}:R>***',
                         'uk': 'Ти занадто часто використовуєш команду\n\n- *Спробуй ще раз **<t:{timestamp}:R>***'}
        no_mangal_to_cook = {'en': '*How are you going to roast the meat? Buy a grill!*',
                             'ru': '*Как ты собираешься жарить мясо? Купи мангал!*',
                             'uk': "*Як ти збираєшся смажити м'ясо? Купи мангал!*"}
        user_in_black_list_title = {'en': "You are in black list",
                                    'ru': 'Вы в чёрном списке',
                                    'uk': 'Ви в чорному списку'}
        user_in_black_list_desc = {'en': "*You are blacklisted by the bot, so you cannot use it*",
                                   'ru': '*Вы находитесь в чёрном списке бота, поэтому не можете использовать его.\n\n'
                                         f'- Если вы считаете что это ошибка, то заходите на [сервер поддержки]({config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']})*',
                                   'uk': '*Ви в чорному списку бота, тому не можете ним користуватися*'}
        unknown_error_title = {'en': "Unknown error",
                               'ru': 'Неизвестная ошибка',
                               'uk': 'Невідома помилка'}
        unknown_error_desc = {
            'en': "*Oops, something seems to have gone wrong. You can report it via the </report:1106680848167739493> command*",
            'ru': '*Упс, кажется что-то пошло не так. Вы можете сообщить об этом через команду </report:1106680848167739493>*',
            'uk': '*Упс, здається, щось пішло не так. Ви можете повідомити про це через команду </report:1106680848167739493>*'}
        bot_missing_perms_title = {'en': "The bot doesn't have enough permissions",
                                   'ru': 'У хряка не достаточно прав',
                                   'uk': 'У хряка недостатньо прав'}
        bot_missing_perms_desc = {'en': "*Give the bot the following permissions:*",
                                  'ru': '*Выдайте боту следующие права:*',
                                  'uk': '*Видайте боту наступні права:*'}
        user_missing_perms_title = {'en': "You have no rights",
                                    'ru': 'У вас нет прав',
                                    'uk': 'У вас немає прав'}
        user_missing_perms_desc = {'en': "*You don't have the following permissions:*",
                                   'ru': '*У вас не хватает следующих прав:*',
                                   'uk': '*Вам не вистачає наступних прав:*'}
        forbidden_title = {'en': "Forbidden",
                           'ru': 'Что-то пошло не так',
                           'uk': 'Щось пішло не так'}
        forbidden_desc = {
            'en': "This probably happened because the bot did not have enough permissions. Double-check whether the Hryak has all the necessary permissions",
            'ru': '*Вероятно это случилось потому-что у бота не достаточно прав. Перепроверьте есть ли у Хряка все нужные права*',
            'uk': '*Ймовірно, це сталося тому, що в бота недостатньо прав. Перевірте, чи є у Хряка всі потрібні права*'}
        modal_input_is_not_number_title = {'en': 'Invalid input',
                                           'ru': 'Неверный ввод',
                                           'uk': 'Невірне введення'}
        modal_input_is_not_number_desc = {
            'en': "*What you entered does not look like a number, but it would be better a number*",
            'ru': '*То что ты ввёл не похоже на число, а лучше бы это было числом*',
            'uk': '*Те, що ти ввів, не схоже на число, а краще б це було числом*'}
        bot_is_restarting_title = {'en': 'Bot is restarting',
                                   'ru': 'Бот перезагружается',
                                   'uk': 'Бот перезавантажується'}
        bot_is_restarting_desc = {
            'en': "*The bot is currently restarting, some functions may not work*",
            'ru': '*В данный момент бот перезагружается, некоторые функции могут не работать*',
            'uk': '*Наразі бот перезавантажується, деякі функції можуть не працювати*'}
        cannot_use_command_in_this_channel_title = {'en': 'The command is not available',
                                                    'ru': 'Команда не доступна',
                                                    'uk': 'Команда недоступна'}
        cannot_use_command_in_this_channel_desc = {
            'en': "*This command cannot be used in this channel*",
            'ru': '*Эту команду нельзя использовать в этом канале*',
            'uk': '*Цю команду не можна використовувати в цьому каналі*'}

    Permissions = {'add_reactions': {'en': 'Add reactions', 'ru': 'Добавлять реакции',
    'uk': 'Додавати реакції'},
                   'administrator': {'en': 'Administrator', 'ru': 'Администратор',
                   'uk': 'Адміністратор'},
                   'attach_files': {'en': 'Attach files', 'ru': 'Прикреплять файлы',
                   'uk': 'Прикріплювати файли'},
                   'ban_members': {'en': 'Ban members', 'ru': 'Банить',
                   'uk': 'Банити'},
                   'change_nickname': {'en': 'Change nickname', 'ru': 'Изменять имя',
                   'uk': "Змінювати ім'я"},
                   'connect': {'en': 'Connect', 'ru': 'Подключатся',
                   'uk': 'Підключатися'},
                   'create_forum_threads': {'en': 'Create forum threads', 'ru': 'Создавать ветки на форуме',
                   'uk': 'Створювати гілки на форумі'},
                   'create_instant_invite': {'en': 'Create instant invite', 'ru': 'Создавать приглашение',
                   'uk': 'Створювати запрошення'},
                   'create_private_threads': {'en': 'Create private threads', 'ru': 'Создавать приватные ветки',
                   'uk': 'Створювати приватні гілки'},
                   'create_public_threads': {'en': 'Create public threads', 'ru': 'Создавать публичные ветки',
                   'uk': 'Створювати публічні гілки'},
                   'deafen_members': {'en': 'Deafen members', 'ru': 'Отключать звук',
                   'uk': 'Вимикати звук'},
                   'embed_links': {'en': 'Embed links', 'ru': 'Вставить ссылки',
                   'uk': 'Вставляти посилання'},
                   'external_emojis': {'en': 'External emojis', 'ru': 'Внешние эмодзи',
                   'uk': 'Зовнішні емодзі'},
                   'external_stickers': {'en': 'External stickers', 'ru': 'Внешние стикеры',
                   'uk': 'Зовнішні стікери'},
                   'kick_members': {'en': 'Kick members', 'ru': 'Исключать участников',
                   'uk': 'Виключати учасників'},
                   'manage_channels': {'en': 'Manage channels', 'ru': 'Управлять каналами',
                   'uk': 'Керувати каналами'},
                   'manage_emojis': {'en': 'Manage emojis', 'ru': 'Управлять эмодзи',
                   'uk': 'Керувати емодзі'},
                   'manage_emojis_and_stickers': {'en': 'Manage emojis and stickers',
                                                  'ru': 'Управлять смайликами и стикерами',
                                                  'uk': 'Керувати смайликами та стікерами'},
                   'manage_events': {'en': 'Manage events', 'ru': 'Управлять событиями',
                   'uk': 'Керувати подіями'},
                   'manage_guild': {'en': 'Manage guild', 'ru': 'Управлять сервером',
                   'uk': 'Керувати сервером'},
                   'manage_messages': {'en': 'Manage messages', 'ru': 'Управлять сообщениями',
                   'uk': 'Керувати повідомленнями'},
                   'manage_nicknames': {'en': 'Manage nicknames', 'ru': 'Управлять именами',
                   'uk': 'Керувати іменами'},
                   'manage_permissions': {'en': 'Manage permissions', 'ru': 'Управлять правами',
                   'uk': 'Керувати правами'},
                   'manage_roles': {'en': 'Manage roles', 'ru': 'Управлять ролями',
                   'uk': 'Керувати ролями'},
                   'manage_threads': {'en': 'Manage threads', 'ru': 'Управлять ветками',
                   'uk': 'Керувати гілками'},
                   'manage_webhooks': {'en': 'Manage webhooks', 'ru': 'Управлять вэб-хуками',
                   'uk': 'Керувати вебхуками'},
                   'mention_everyone': {'en': 'Mention everyone', 'ru': 'Упоминать everyone',
                   'uk': 'Згадувати everyone'},
                   'moderate_members': {'en': 'Moderate members', 'ru': 'Управлять учатниками',
                   'uk': 'Керувати учасниками'},
                   'move_members': {'en': 'Move members', 'ru': 'Перемещать участников',
                   'uk': 'Переміщувати учасників'},
                   'mute_members': {'en': 'Mute members', 'ru': 'Заглушать участников',
                   'uk': 'Заглушувати учасників'},
                   'priority_speaker': {'en': 'Priority speaker', 'ru': 'Приоритетный режим',
                   'uk': 'Пріоритетний режим'},
                   'read_message_history': {'en': 'Read message history', 'ru': 'Читать историю сообщений',
                   'uk': 'Читати історію повідомлень'},
                   'read_messages': {'en': 'Read messages', 'ru': 'Читать сообщения',
                   'uk': 'Читати повідомлення'},
                   'request_to_speak': {'en': 'Request to speak', 'ru': 'Попросить выступить',
                   'uk': 'Попросити виступити'},
                   'send_messages': {'en': 'Send messages', 'ru': 'Отправлять сообщения',
                   'uk': 'Надсилати повідомлення'},
                   'send_messages_in_threads': {'en': 'Send messages in threads',
                                                'ru': 'Отправлять сообщения в ветки',
                                                'uk': 'Надсилати повідомлення в гілки'},
                   'send_tts_messages': {'en': 'Send tts messages', 'ru': 'Отправлять tts сообщения',
                   'uk': 'Надсилати tts повідомлення'},
                   'speak': {'en': 'Speak', 'ru': 'Говорить',
                   'uk': 'Говорити'},
                   'start_embedded_activities': {'en': 'Start embedded activities',
                                                 'ru': 'Начинать встроенные действия',
                                                 'uk': 'Починати вбудовані дії'},
                   'stream': {'en': 'Stream', 'ru': 'Стримить',
                   'uk': 'Стрімити'},
                   'use_application_commands': {'en': 'Use application commands', 'ru': 'Использовать команды',
                   'uk': 'Використовувати команди'},
                   'use_embedded_activities': {'en': 'Use embedded activities',
                                               'ru': 'Использовать встроенные активности',
                                               'uk': 'Використовувати вбудовані активності'},
                   'use_external_emojis': {'en': 'Use external emojis', 'ru': 'Использовать внешние смайлики',
                   'uk': 'Використовувати зовнішні смайлики'},
                   'use_external_stickers': {'en': 'Use external stickers', 'ru': 'Использовать внешние стикеры',
                   'uk': 'Використовувати зовнішні стікери'},
                   'use_slash_commands': {'en': 'Use slash commands', 'ru': 'Использовать слэш-команды',
                   'uk': 'Використовувати слеш-команди'},
                   'use_voice_activation': {'en': 'Use voice activation', 'ru': 'Использовать режим рации',
                   'uk': 'Використовувати режим рації'},
                   'view_audit_log': {'en': 'View audit log', 'ru': 'Просмотр журнала аудита',
                   'uk': 'Перегляд журналу аудиту'},
                   'view_channel': {'en': 'View channel', 'ru': 'Просмотр канала',
                   'uk': 'Перегляд каналу'},
                   'view_guild_insights': {'en': 'View guild insights', 'ru': 'Просмотр статистики сервера',
                   'uk': 'Перегляд статистики сервера'}}

    # _____________________________________________________________________________________

    class Inventory:
        inventory_title = {'en': 'Inventory',
                           'ru': 'Инвентарь',
                           'uk': 'Інвентар'}
        inventory_empty_desc = {'en': '*Your inventory is empty*',
                                'ru': '*Ваш инвентарь пуст*',
                                'uk': '*Ваш інвентар порожній*'}
        select_item_placeholder = {'en': 'Choose item',
                                   'ru': 'Выберите предмет',
                                   'uk': 'Оберіть предмет'}

    class InventoryItemSellModal:
        label = {'en': 'Number of items you want to sell',
                 'ru': 'Количество предметов для продажи',
                 'uk': 'Кількість предметів для продажу'}
        placeholder = {'en': 'You have: {max_amount}',
                       'ru': 'У вас есть: {max_amount}',
                       'uk': 'У вас є: {max_amount}'}
        title = {'en': 'Item selling',
                 'ru': 'Продажа',
                 'uk': 'Продаж'}

    class InventoryItemSold:
        title = {'en': 'Item sold',
                 'ru': 'Предмет продан',
                 'uk': 'Предмет продано'}
        desc = {'en': "*You sold **{item} x{amount}** and received **{money}** 🪙*",
                'ru': '*Вы продали **{item} x{amount}** и получили **{money}** 🪙*',
                'uk': '*Ви продали **{item} x{amount}** та отримали **{money}** 🪙*'}

    class InventoryItemCookModal:
        label = {'en': 'Amount of items to cook',
                 'ru': 'Количество предметов для готовки',
                 'uk': 'Кількість предметів для готування'}
        placeholder = {'en': 'You have: {max_amount}',
                       'ru': 'У вас есть: {max_amount}',
                       'uk': 'У вас є: {max_amount}'}
        title = {'en': 'Cooking',
                 'ru': 'Готовка',
                 'uk': 'Готування'}

    class InventoryItemCooked:
        title = {'en': 'Item cooked',
                 'ru': 'Предмет приготовлен',
                 'uk': 'Предмет приготовано'}
        desc = {'en': '*You cooked **{item} x{amount}***',
                'ru': '*Вы приготовили **{item} x{amount}***',
                'uk': '*Ви приготували **{item} x{amount}***'}

    class ItemUsed:
        ate_poop_and_poisoned_title = {'en': 'You ate poop',
                                       'ru': 'Вы сьели какаху',
                                       'uk': "Ви з'їли какаху"}
        ate_poop_and_poisoned_desc = {
            'en': 'You ate poop. You liked its taste, but unfortunately you got poisoned\n\n'
                  '*- A doctor came to you and cured you, but now he asks 5 🪙 for treatment*',
            'ru': 'Вы сьели какашку. Вам понравился её вкус, но к сожалению вы отравились\n\n'
                  '*- К вам пришёл доктор и вылечил вас, но теперь он просит 5 🪙 за лечение*',
            'uk': "Ви з'їли какашку. Вам сподобався її смак, але, на жаль, ви отруїлися\n\n*- До вас прийшов лікар і вилікував вас, але тепер він просить 5 🪙 за лікування*"}
        ate_poop_and_dizzy_title = {'en': 'You ate poop',
                                    'ru': 'Вы сьели какаху',
                                    'uk': "Ви з'їли какаху"}
        ate_poop_and_dizzy_desc = {
            'en': '*> You ate poop. You felt dizzy and almost fell, but overall everything was fine*',
            'ru': '*> Вы сьели какашку. У вас закрутилась голова и вы чуть не упали, но в целом всё хорошо*',
            'uk': "*> Ви з'їли какашку. У вас запаморочилася голова і ви ледь не впали, але загалом усе добре*"}
        ate_poop_and_question_title = {'en': 'You ate poop',
                                       'ru': 'Вы сьели какаху',
                                       'uk': "Ви з'їли какаху"}
        ate_poop_and_question_desc = {
            'en': '*> Out of your curiosity, you ate poop. There is only one question left, why?*',
            'ru': '*> Из своего любопытства вы сьели какаху. Остается лишь один вопрос, зачем?*',
            'uk': "*> Зі своєї цікавості ви з'їли какаху. Залишається лише одне питання, навіщо?*"}
        ate_poop_and_dad_title = {'en': 'You ate poop',
                                  'ru': 'Вы сьели какаху',
                                  'uk': "Ви з'їли какаху"}
        ate_poop_and_dad_desc = {
            'en': '*> After the meal, you went outside to breathe some fresh air where you saw your father. He turned around silently and left*',
            'ru': '*> После трапезы, вы вышли подышать свежим воздухом где увидели своего отца. Он молча развернулся и ушел*',
            'uk': '*> Після трапези ви вийшли подихати свіжим повітрям, де побачили свого батька. Він мовчки розвернувся і пішов*'}
        laxative_title = {'en': 'You used laxative',
                          'ru': 'Вы использовали слабительное',
                          'uk': 'Ви використали проносне'}
        laxative_desc = {
            'en': '**{pig}** will produce more manure on the next **{step}** feedings',
            'ru': '**{pig}** будет давать больше навоза следующие **{step}** кормёжек',
            'uk': '**{pig}** даватиме більше гною наступні **{step}** годувань'}
        case_title = {'en': 'You got:',
                      'ru': 'Вы получили:',
                      'uk': 'Ви отримали:'}

    class Wardrobe:
        wardrobe_title = {'en': 'Wardrobe',
                          'ru': 'Гардероб',
                          'uk': 'Гардероб'}
        wardrobe_empty_desc = {'en': '*Your wardrobe is empty*',
                               'ru': '*Ваш гардероб пуст*',
                               'uk': '*Ваш гардероб порожній*'}
        select_item_placeholder = {'en': 'Choose item',
                                   'ru': 'Выберите предмет',
                                   'uk': 'Оберіть предмет'}

    class WardrobeItemChooseLayerToWear:
        title = {'en': 'Choose parts to wear',
                 'ru': 'Выберите части для надевания',
                 'uk': 'Оберіть частини для надягання'}
        desc = {'en': 'This skin can be worn in parts. Choose the pieces you wish to equip',
                'ru': 'Вы можете надеть этот скин частично. Выберите части, которые хотите надеть',
                'uk': 'Ви можете надіти цей скін частково. Оберіть частини, які хочете надіти'}
        wear_all_option = {'en': 'Wear all',
                           'ru': 'Надеть всё',
                           'uk': 'Надіти все'}

    class WardrobeItemWear:
        title = {'en': 'You put on {item}',
                 'ru': 'Вы надели {item}',
                 'uk': 'Ви надягли {item}'}
        desc_list = {'en': ['*This **{item}** looks fantastic on you!*'],
                     'ru': ['*Этот **{item}** вам очень идёт!*'],
                     'uk': ['*Цей **{item}** вам дуже личить!*']}

    class WardrobeItemRemove:
        title = {'en': 'You removed {item}',
                 'ru': 'Вы сняли {item}',
                 'uk': 'Ви зняли {item}'}
        desc = {'en': "*Now you don't wear **{item}***",
                'ru': '*Теперь вы не носите **{item}***',
                'uk': '*Тепер ви не носите **{item}***'}

    class WardrobeItemPreview:
        title = {'en': 'Preview mode',
                 'ru': 'Режим предосмотра',
                 'uk': 'Режим передперегляду'}
        desc = {'en': "*Imagine wearing **{item}** - this is how it would look*",
                'ru': '*Вот как будет выглядеть **{item}**, если вы его наденете*',
                'uk': '*Ось як виглядатиме **{item}**, якщо ви його надінете*'}

    class Shop:
        shop_empty_desc = {'en': '*Shop is empty now*',
                           'ru': '*Магазин сейчас пустой*',
                           'uk': '*Магазин зараз порожній*'}
        main_page_title = {'en': 'Магазин',
                           'ru': 'Shop',
                           'uk': 'Shop'}
        main_page_desc = {'en': '*Welcome to the store, where you can purchase anything at any time*\n\n'
                                '**Choose one of the categories below:**',
                          'ru': '*Добро пожаловать в магазин. Тут вы можете купить что угодно и когда угодно*\n\n'
                                '**Выберите одну из категорий ниже:**',
                          'uk': '*Ласкаво просимо до магазину. Тут ви можете купити що завгодно і коли завгодно*\n\n**Оберіть одну з категорій нижче:**'}
        buy_hollars_description = {'en': '💵 | *You can buy **Hryak-Dollars** **[here](https://boosty.to/brevnoo.en)***',
                                   'ru': '💵 | *Вы можете покупать **Хряк-Доллары** **[на этом сайте](https://boosty.to/brevnoo)***',
                                   'uk': '💵 | *Ви можете купувати **Хряк-Долари** **[на цьому сайті](https://boosty.to/brevnoo)***'}
        titles = {
            'daily_shop': {'en': 'Daily shop',
                           'ru': 'Ежедневный магазин',
                           'uk': 'Щоденний магазин'},
            'case_shop': {'en': 'Case shop',
                          'ru': 'Кейсы',
                          'uk': 'Кейси'},
            'consumables_shop': {'en': 'Consumables',
                                 'ru': 'Расходники',
                                 'uk': 'Витратники'},
            'tools_shop': {'en': 'Tools',
                           'ru': 'Инструменты',
                           'uk': 'Інструменти'},
            'premium_skins_shop': {'en': 'Premium skins',
                                   'ru': 'Премиум скины',
                                   'uk': 'Преміум скіни'},
            'coins_shop': {'en': 'Buy coins',
                           'ru': 'Купить монеты',
                           'uk': 'Купити монети'},
            'donation_shop': {'en': 'Donate',
                              'ru': 'Донат',
                              'uk': 'Донат'},
        }
        donation_shop_title = {
            'en': 'Support me',
            'ru': 'Поддержка',
            'uk': 'Підтримка'
        }
        # donation_shop_desc = {
        #     'en': 'Sorry, donation is temporarily unavailable. The service on which I accepted donations is broken and I\'m trying to solve this problem\n'
        #           '- Creator of the Hryak',
        #     'ru': '*Сорян, донат временно недоступен. Сервис на котором я принимал донаты сломался и я пытаюсь решить эту проблему*\n'
        #           '- Создатель Хряка'}
        donation_shop_desc = {
            'en': 'Hi, if you suddenly want to support me with a donation, and in return get some money, here is the link: [buymeacoffee.com](https://buymeacoffee.com/brevnoo/extras)\n\n'
                  'Of course you don\'t have to support me, but I would be pleased. Thx anyways <:pigWatermelon:1284935022758854719>',
            'ru': 'Здарова! Если вдруг хочешь поддержать меня донатом и в ответ получить немного игровой валюты, вот ссылка: [buymeacoffee.com](https://buymeacoffee.com/brevnoo/extras)\n\n'
                  'Естественно, ты не обязан меня поддерживать, но мне будет приятно. В любом случае, спасибо <:pigWatermelon:1284935022758854719>',
            'uk': "Здоров! Якщо раптом хочеш підтримати мене донатом і у відповідь отримати трохи ігрової валюти, ось посилання: [buymeacoffee.com](https://buymeacoffee.com/brevnoo/extras)\n\nЗвісно, ти не зобов'язаний мене підтримувати, але мені буде приємно. У будь-якому разі, дякую <:pigWatermelon:1284935022758854719>"}

    class PremiumShop:
        main_page_title = {'en': 'Donation page',
                           'ru': 'Страница доната',
                           'uk': 'Сторінка донату'}
        main_page_desc = {
            'en': '*Sup, this is a donation page. Here you can buy game currency, thereby saving the creator of the Hryak from starvation*\n\n'
                  '- Select the product below that you want to buy',
            'ru': '*Здарова, это страница доната. Здесь можно купить игровую валюту, тем самым спасая создателя Хряка от голодной смерти*\n\n'
                  '- Выберите товар ниже, который хотите купить',
            'uk': '*Здоров, це сторінка донату. Тут можна купити ігрову валюту, тим самим рятуючи творця Хряка від голодної смерті*\n\n- Оберіть товар нижче, який хочете купити'}
        main_page_select_placeholder = {'en': 'Select product',
                                        'ru': 'Выберите товар',
                                        'uk': 'Оберіть товар'}
        main_page_select_option_hollars = {'en': 'Hryak-dollars',
                                           'ru': 'Хряк-доллары',
                                           'uk': 'Хряк-долари'}
        main_page_select_option_coins = {'en': 'Coins',
                                         'ru': 'Монеты',
                                         'uk': 'Монети'}
        buy_hollars_page_title = {'en': 'Donation page',
                                  'ru': 'Покупка валюты',
                                  'uk': 'Купівля валюти'}
        buy_hollars_page_desc = {
            'en': '*Hryak-dollars are the best currency in the game. For it you can buy coins or premium skins*\n\n'
                  '- 1 dollar = {amount} hryak-dollars',
            'ru': '*Хряк-доллары - это лучшая валюта в игре. За неё вы можете покупать монеты либо же эксклюзивные скины*\n\n'
                  '- 1 рубль = {amount} хряк-доллар',
            'uk': '*Хряк-долари - це найкраща валюта в грі. За неї ви можете купувати монети або ж ексклюзивні скіни*\n\n- 1 рубль = {amount} хряк-долар'}
        buy_hollars_button_label = {'en': 'Select quantity',
                                    'ru': 'Выберите количество',
                                    'uk': 'Оберіть кількість'}
        get_amount_of_hollars_modal_title = {'en': 'Buying page',
                                             'ru': 'Покупка',
                                             'uk': 'Купівля'}
        get_amount_of_hollars_modal_label = {'en': 'Amount',
                                             'ru': 'Количество',
                                             'uk': 'Кількість'}
        get_amount_of_hollars_modal_placeholder = {'en': 'Enter the number of hryak-dollars',
                                                   'ru': 'Введите количество хряк-долларов',
                                                   'uk': 'Введіть кількість хряк-доларів'}
        buy_coins_page_title = {'en': 'Donation page',
                                'ru': 'Покупка монет',
                                'uk': 'Купівля монет'}
        buy_coins_page_desc = {
            'en': '*Coins are the main currency in the game. You can buy most items and skins with it*\n\n'
                  '- Select the quantity you need below',
            'ru': '*Монеты - основная валюта в игре. За неё можно купить большинство предметов и скинов*\n\n'
                  '- Выберите нужное вам количество ниже',
            'uk': '*Монети - основна валюта в грі. За неї можна купити більшість предметів і скінів*\n\n- Оберіть потрібну вам кількість нижче'}
        select_coins_option_label = {
            'en': 'Coins x{amount}',
            'ru': 'Монеты x{amount}',
            'uk': 'Монети x{amount}'}
        select_coins_option_desc = {
            'en': 'Price: {price}{currency}',
            'ru': 'Цена: {price}{currency}',
            'uk': 'Ціна: {price}{currency}'}
        select_coins_placeholder = {
            'en': 'Select amount',
            'ru': 'Выберите количество',
            'uk': 'Оберіть кількість'}
        select_payment_method_title = {'en': 'Payment method',
                                       'ru': 'Способ оплаты',
                                       'uk': 'Спосіб оплати'}
        select_payment_method_desc = {'en': '*Choose a payment method below*',
                                      'ru': '*Выберите способ оплаты ниже. Если вас не устраивают тарифы в каком либо способе оплаты, просто попробуйте другой способ*',
                                      'uk': '*Оберіть спосіб оплати нижче. Якщо вас не влаштовують тарифи в якомусь способі оплати, просто спробуйте інший спосіб*'}
        payment_methods_descs = {
            'donatello': {'en': '- May take up to a day\n'
                                '- Ukrainian cards\n'
                                '- Cryptocurrency\n',
                          'ru': '- Выдача может занимать до суток\n'
                                '- Доступны украинские карточки\n'
                                '- Доступна криптовалюта\n'
                                '- Рекомендуется для украинцев\n',
                          'uk': '- Видача може займати до доби\n- Доступні українські картки\n- Доступна криптовалюта\n- Рекомендується для українців\n'},
            'lava.top': {'en': '- Instant delivery\n'
                               '- Russian / American cards\n',
                         'ru': '- Моментальная выдача\n'
                               '- Доступны русские и американские карточки\n',
                         'uk': '- Моментальна видача\n- Доступні російські та американські картки\n'},
        }
        pay_below_title = {'en': 'Payment',
                           'ru': 'Оплата',
                           'uk': 'Оплата'}
        pay_below_desc = {'en': '*Pay for your order below*\n'
                                f'- If you have any problems, write to the developer in DM: @{config.DEVELOPER_USERNAME}\n\n'
                                '⚠️ Carefully follow the instructions that will be given',
                          'ru': '*Оплатите ваш заказ ниже*\n'
                                f'- Если у вас возникли проблемы, обратитесь на [сервер поддержки]({config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']})\n\n'
                                '⚠️ Чётко следуйте инструкциям, которые будут указаны',
                          'uk': None}
        aaio_pay_title = {'en': 'AAIO payment',
                          'ru': 'Оплата AAIO',
                          'uk': 'Оплата AAIO'}
        aaio_pay_desc = {'en': ''
                               '- Pay for your order using this link: [link]({url})\n'
                               '  - Order number: {order_id}',
                         'ru': '*На некоторые способы оплаты может быть увеличенная минимальная сумма. Я знаю что это не удобно, но ничего не могу с этим поделать*\n\n'
                               '- Оплатите заказ по этой ссылке: [ссылка]({url})\n'
                               '  - Номер заказа: {order_id}',
                         'uk': '*На деякі способи оплати може бути збільшена мінімальна сума. Я знаю, що це незручно, але нічого не можу з цим вдіяти*\n\n- Оплатіть замовлення за цим посиланням: [посилання]({url})\n  - Номер замовлення: {order_id}'}
        boosty_pay_title = {'en': 'Boosty',
                            'ru': 'Boosty',
                            'uk': 'Boosty'}
        boosty_pay_desc = {'en': '- Send {amount}{currency} via this link: [link](https://boosty.to/brevnoo/donate)\n'
                                 '- In the "message" field, enter the order number\n'
                                 ' > Order number: {order_id}',
                           'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка](https://boosty.to/brevnoo/donate)\n'
                                 '- В поле "сообщение" введите номер заказа\n'
                                 ' > Номер заказа: {order_id}',
                           'uk': '- Надішліть {amount}{currency} за цим посиланням: [посилання](https://boosty.to/brevnoo/donate)\n- У полі "повідомлення" введіть номер замовлення\n > Номер замовлення: {order_id}'}
        donatepay_pay_title = {'en': 'DonatePay',
                               'ru': 'DonatePay',
                               'uk': 'DonatePay'}
        donatepay_pay_desc = {
            'en': '- Send {amount}{currency} via this link: [link](https://new.donatepay.ru/@brevnoo)\n'
                  '- In the "message" field, enter the order number\n'
                  ' > Order number: {order_id}',
            'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка](https://new.donatepay.ru/@brevnoo)\n'
                  '- В поле "сообщение стримеру" введите номер заказа\n'
                  ' > Номер заказа: {order_id}',
            'uk': '- Надішліть {amount}{currency} за цим посиланням: [посилання](https://new.donatepay.ru/@brevnoo)\n- У полі "повідомлення стримеру" введіть номер замовлення\n > Номер замовлення: {order_id}'}
        donatello_pay_title = {'en': 'Donatello',
                               'ru': 'Donatello',
                               'uk': 'Donatello'}
        donatello_pay_desc = {'en': '- Send {amount}{currency} via this link: [link](https://donatello.to/brevnoo)\n'
                                    '- In the "message" field, enter the order number\n'
                                    ' > Order number: {order_id}\n\n'
                                    '*Payment method "Mono", accepts all cards*',
                              'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка](https://donatello.to/brevnoo)\n'
                                    '- В поле "сообщение" введите номер заказа\n'
                                    ' > Номер заказа: {order_id}\n\n'
                                    '*Способ оплаты "Моно", принимает все карточки*',
                              'uk': '- Надішліть {amount}{currency} за цим посиланням: [посилання](https://donatello.to/brevnoo)\n- У полі "повідомлення" введіть номер замовлення\n > Номер замовлення: {order_id}\n\n*Спосіб оплати "Моно", приймає всі картки*'}
        lava_pay_title = {'en': 'Lava.top',
                               'ru': 'Lava.top',
                               'uk': 'Lava.top'}
        lava_pay_desc = {'en': '- Send {amount}{currency} via this link: [link]({url})\n'
                                    ' > Order number: {order_id}',
                              'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка]({url})\n'
                                    ' > Номер заказа: {order_id}\n\n',
                              'uk': '- Надішліть {amount}{currency} за цим посиланням: [посилання]({url})\n > Номер замовлення: {order_id}\n\n\n'}
        lava_pay_desc_minimum_requirement = {'en': '*The minimum amount for Lava.top is {amount} {currency}. Please choose another payment method*',
                                            'ru': '*Минимальная сумма для Lava.top - {amount} {currency}*',
                                            'uk': '*Мінімальна сума для Lava.top - {amount} {currency}*'}
        item_give_notification_title = {'en': 'Donation paid',
                                        'ru': 'Донат оплачен',
                                        'uk': 'Донат оплачено'}
        item_give_notification_desc = {'en': '*You received items for your donation:*\n\n'
                                             '{items}\n\n'
                                             '*Thank you for your support 💝*',
                                       'ru': '*Вы получили предметы за ваш донат:*\n\n'
                                             '{items}\n\n'
                                             '*Спасибо за вашу поддержку 💝*',
                                       'uk': '*Ви отримали предмети за ваш донат:*\n\n{items}\n\n*Дякуємо за вашу підтримку 💝*'}

    class ShopItemBought:
        title = {'en': 'You bought {item}',
                 'ru': 'Вы купили {item}',
                 'uk': 'Ви купили {item}'}
        desc = {'en': "*We hope you enjoy your purchase. (Refunds are not available)*",
                'ru': '*Надеюсь, вам понравится ваша покупка. (Деньги не возвращаем)*',
                'uk': '*Сподіваюся, вам сподобається ваша покупка. (Гроші не повертаємо)*'}

    class JoinMessageSet:
        description = {'en': 'Set message when user joins server',
                       'ru': 'Установить сообщение, когда пользователь заходит на сервер',
                       'uk': 'Встановити повідомлення, коли користувач заходить на сервер'}
        channel_var_name = {'en': 'channel',
                            'ru': 'канал',
                            'uk': 'канал'}
        channel_var_desc = {'en': 'The channel where the message will be sent',
                            'ru': 'Канал, в который будет отправляться сообщение',
                            'uk': 'Канал, у який надсилатиметься повідомлення'}
        message_var_name = {'en': 'message',
                            'ru': 'сообщение',
                            'uk': 'повідомлення'}
        message_var_desc = {
            'en': 'The message that will be sent when the participant enters. Use {user} to mention',
            'ru': 'Сообщение, которое будет отправляться при заходе участника. Используйте {user} для упоминания',
            'uk': 'Повідомлення, яке надсилатиметься при заході учасника. Використовуйте {user} для згадки'}
        scd_title = {'en': 'Great, the channel is set: {channel}',
                     'ru': 'Отлично, канал установлен: {channel}',
                     'uk': 'Чудово, канал встановлено: {channel}'}
        scd_desc = {'en': '*This is the message that will appear:*\n\n{message}',
                    'ru': '*Вот сообщение которое будет выводится:*\n\n{message}',
                    'uk': '*Ось повідомлення, яке виводитиметься:*\n\n{message}'}
        reset_scd_title = {'en': 'Join message reset',
                           'ru': 'Приветственное сообщение сброшено',
                           'uk': 'Привітальне повідомлення скинуто'}

    class JoinMessageReset:
        description = {'en': 'Reset greeting message settings',
                       'ru': 'Сбросить настройки для приветственного сообщения',
                       'uk': 'Скинути налаштування для привітального повідомлення'}
        scd_title = {'en': 'Join message reset',
                     'ru': 'Приветственное сообщение сброшено',
                     'uk': 'Привітальне повідомлення скинуто'}

