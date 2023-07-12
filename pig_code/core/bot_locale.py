from disnake import Locale
from . import config

valid_discord_locales = ['en', 'ru']

full_names = {'en': 'English',
              'ru': 'Russian | Pусский',
              'uk': 'Ukrainian | Українська'}

big_texts = {

}


class Locales:
    class Feed:
        description = {Locale.en_US: 'Feed your pig',
                       Locale.ru: 'Накормить своего хряка'}
        feed_scd_title = {'en': 'You fed your pig',
                          'ru': 'Вы покормили своего хряка'}
        feed_scd_desc_list = {'en': ['**{pig}** recovered by **{mass}** kg'],
                              'ru': ['**{pig}** поправился на **{mass}** кг',
                                     '**{pig}** набрал **{mass}** кг сала',
                                     '**{pig}** поправился на **{mass}** кг сала',
                                     '**{pig}** стал больше на **{mass}** кг',
                                     '**{pig}** добавил **{mass}** кг веса',
                                     '**{pig}** прибавил **{mass}** кг',
                                     '**{pig}** увеличил свой вес на **{mass}** кг',
                                     '**{pig}** набрал дополнительные **{mass}** кг',
                                     '**{pig}** получил **{mass}** кг жировых отложений',
                                     '**{pig}** добавил **{mass}** кг массы тела',
                                     '**{pig}** стал тяжелее на **{mass}** кг',
                                     '**{pig}** прибавил в весе **{mass}** кг',
                                     '**{pig}** получил дополнительные **{mass}** кг',
                                     '**{pig}** утяжелился на **{mass}** кг']
                              }
        feed_fail_desc_list = {'en': ['Your **{pig}** vomited and he lost **{mass}** kg'],
                               'ru': ['Вашего **{pig}** стошнило и он похудел на **{mass}** кг']}
        pig_pooped_desc_list = {'en': ['**{pig}** pooped and you got **{poop}** 💩'],
                                'ru': ['**{pig}** покакал и вы получили **{poop}** 💩',
                                       '**{pig}** испражнился и вы получили **{poop}** 💩',
                                       '**{pig}** дал вам **{poop}** 💩',
                                       '**{pig}** покакал и оставил **{poop}** 💩',
                                       '**{pig}** справил нужду, и теперь у вас есть **{poop}** 💩',
                                       '**{pig}** испражнился, и вы получили **{poop}** 💩',
                                       '**{pig}** сбросил навоз в размере **{poop}** 💩',
                                       '**{pig}** выпустил навоз объемом **{poop}** 💩',
                                       '**{pig}** дал вам свои экскременты в количестве **{poop}** 💩',
                                       '**{pig}** оставил после себя навоз в размере **{poop}** 💩',
                                       '**{pig}** справил нужду, и теперь у вас есть **{poop}** 💩',
                                       '**{pig}** выделил навоз объемом **{poop}** 💩',
                                       '**{pig}** сбросил свои экскременты в количестве **{poop}** 💩',
                                       '**{pig}** оставил после себя навоз в объеме **{poop}** 💩',
                                       '**{pig}** справил нужду, и вы получили **{poop}** 💩',
                                       '**{pig}** выпустил навоз в размере **{poop}** 💩',
                                       '**{pig}** дал вам свои экскременты в количестве **{poop}** 💩',
                                       '**{pig}** оставил после себя навоз в объеме **{poop}** 💩']}
        total_pig_weight = {'en': 'Weight of your pig: **{weight}** kg',
                            'ru': 'Масса твоего хряка: **{weight}** кг'}

    class Meat:
        description = {Locale.en_US: 'Take some meat from your pig',
                       Locale.ru: 'Снять немного сала с вашего хряка (ему не больно)'}
        meat_title = {'en': 'You cut off some meat',
                      'ru': 'Вы срезали немного сала'}
        meat_desc_list = {'en': ['You trimmed some fat from **{pig}** and got **{meat}** 🥓'],
                          'ru': ['Вы срезали немного сала с **{pig}** и получили **{meat}** 🥓']}
        weight_lost_desc_list = {'en': ['**{pig}** lost **{weight_lost}** kg of weight'],
                                 'ru': ['**{pig}** потерял **{weight_lost}** кг веса']}
        no_knife_desc = {'en': '*Are you going to cut off the meat with your hands? Find a knife*',
                         'ru': '*Ты собираешся мясо руками снимать? Найди нож*'}
        total_pig_weight = {'en': 'Weight of your pig: **{weight}** kg',
                            'ru': 'Масса твоего хряка: **{weight}** кг'}

    class Breed:
        description = {
            Locale.en_US: 'Try mating your pig with another boar',
            Locale.ru: 'Попробовать спарить вашего хряка с другим хряком'
        }
        user_var_name = {
            Locale.en_US: 'user',
            Locale.ru: 'пользователь'
        }
        user_var_desc = {
            Locale.en_US: 'The user whose pig you want to have children with',
            Locale.ru: 'Пользователь, с хряком которого хотите завести детей'
        }
        not_enough_weight_title = {
            'en': 'Not enough weight',
            'ru': 'Не достаточно веса'
        }
        not_enough_weight_desc = {
            'en': "**{pig}** is too small for this\n\n"
                  "- Pig should be at least **{weight}** kg",
            'ru': '**{pig}** слишком маленький для такого\n\n'
                  '- Хряк должен быть хотя бы **{weight}** кг'
        }
        invite_title = {
            'en': 'Proposal for mating',
            'ru': 'Предложение для спаривания'
        }
        personal_invite_desc = {
            'en': '{user} invited {partner} to breed their pigs',
            'ru': '**{user}** предложил **{partner}** спарить своих хряков'
        }
        personal_invite_dm_desc = {
            'en': '**You** were invited to mate pigs with **{user}**',
            'ru': '**Вы** были приглашены для спаривания хряков с **{user}**'
        }
        breed_canceled_title = {
            'en': 'Mate was canceled',
            'ru': 'Спаривание было отменено'
        }
        partner_reject_desc = {
            'en': '- **{user}** did not want to breed boars, very cruel of him',
            'ru': '- **{user}** не захотел спаривать хряков, очень жестоко с его стороны'
        }
        no_response_desc = {
            'en': "- **{user}** didn't answer, how cruel",
            'ru': '- **{user}** ничего не ответил, как жестоко'
        }
        fail_title = {
            'en': 'Failure',
            'ru': 'Неудача'
        }
        fail_desc = {
            'en': '**{pig}** tried to have children with **{partner}** but failed\n\n'
                  '- Try again **<t:{retry}:R>**',
            'ru': '**{pig}** попытался завести детей с **{partner}**, но ничего не получилось\n\n'
                  '- Попробуйте ещё раз **<t:{retry}:R>**'
        }

    class Pregnancy:
        description = {Locale.en_US: 'View boar pregnancy status',
                       Locale.ru: 'Посмотреть статус беременности хряка'}
        not_pregnant_title = {'en': 'Your pig is not pregnant',
                              'ru': 'Ваш хряк не беремен'}
        not_pregnant_desc = {'en': "You looked at your pig's belly, but it's a normal size",
                             'ru': '*Вы посмотрели на живот своего хряка, но он обычного размера*'}

    class Family:
        already_in_family_title = {'en': "You already have a family",
                                   'ru': 'У вас уже есть семья'}
        already_in_family_desc = {'en': "*You first need to exit the current one*",
                                  'ru': '*Вам сначала нужно выйти из текущей семьи*'}
        accept_user_title = {'en': "Great",
                             'ru': 'Отлично'}
        accept_user_desc = {'en': "*You have accepted the request to join from {user}*",
                            'ru': '*Вы приняли запрос на вступление от {user}*'}
        reject_user_title = {'en': "Great",
                             'ru': 'Отлично'}
        reject_user_desc = {'en': "*You have rejected the request to join from **{user}***",
                            'ru': '*Вы отклонили запрос на вступление от **{user}***'}
        no_family_title = {'en': "You don't have a family",
                           'ru': 'У вас нету семьи'}
        no_family_desc = {'en': "*You can't do this because you don't have a family.*",
                          'ru': '*Вы не можете сделать это, так как у вас нету семьи*'}
        not_exist_title = {'en': "You don't have a family",
                           'ru': 'Семьи не существует'}
        not_exist_desc = {'en': "*It seems that such a family does not exist. It's a pity...*",
                          'ru': '*Кажется, такой семьи не существует. Жаль...*'}

    class ViewFamily:
        description = {Locale.en_US: 'Look at your family',
                       Locale.ru: 'Посмотреть на свою семью'}
        family_id_name = {Locale.en_US: 'id',
                          Locale.ru: 'id'}
        family_id_desc = {Locale.en_US: 'ID of the family you want to look at',
                          Locale.ru: 'ID семьи, на которую хотите посмотреть'}
        no_family_title = {'en': "You don't have a family",
                           'ru': 'У вас нету семьи'}
        no_family_desc = {'en': "*You don't seem to have a family. What a pity*",
                          'ru': '*Кажется, у вас нету семьи. Как жаль*'}
        select_member_placeholder = {'en': "View profile",
                                     'ru': 'Посмотреть профиль'}

    class DeleteFamily:
        description = {Locale.en_US: 'Delete your family',
                       Locale.ru: 'Развалить свою семью'}
        not_owner_title = {'en': "Are you serious?",
                           'ru': 'Ты серьезно?'}
        not_owner_desc = {'en': "*You can't just go and destroy a family you're not the head of.*",
                          'ru': '*Вы не можете просто взять и уничтожить семью, в которой вы не глава*'}
        scd_title = {'en': 'Family destroyed',
                     'ru': 'Семья уничтожена'}
        scd_desc = {'en': '*You are so cruel. Destroyed their own family*',
                    'ru': '*Вы такой жестокий. Уничтожили собственную семью*'}

    class FamilyRequests:
        description = {Locale.en_US: 'View a list of family requests',
                       Locale.ru: 'Посмотреть список_запросов на добавление в семью'}
        not_owner_title = {'en': "You don't have permissions",
                           'ru': 'Вы не имеете прав'}
        not_owner_desc = {'en': "*You cannot view requests list because you do not have rights*",
                          'ru': '*Вы не можете посмотреть список запросов, так как не имеете прав*'}
        empty = {'en': "*No requests*",
                 'ru': '*Нету запросов*'}
        select_member_placeholder = {'en': "Choose member",
                                     'ru': 'Выберите пользователя'}

    class InviteFamily:
        description = {Locale.en_US: 'Invite a user to the family',
                       Locale.ru: 'Пригласить пользователя в семью'}
        no_family_title = {'en': "You don't have a family",
                           'ru': 'У вас нету семьи'}
        no_family_desc = {'en': "*You can't invite someone to a family that doesn't exist.*",
                          'ru': '*Вы не можете пригласить кого-тов в семью, которой не существует*'}
        not_owner_title = {'en': "You are not the owner",
                           'ru': 'Вы не имеете прав'}
        not_owner_desc = {'en': "*You cannot invite someone to your family because you do not have rights*",
                          'ru': '*Вы не можете пригласить кого-то в семью, так как не имеете прав*'}
        invite_code_title = {'en': 'Invitation code',
                     'ru': 'Код на приглашение'}
        invite_code_desc = {'en': 'A user can join your family using this code: **{code}**\n' 
                                  'The user you want to invite must use the **/family join** command\n\n' 
                                  'You may also have to issue the **/family requests** command to accept the user',
                    'ru': '*Пользователь может присоединиться к вашей семье используя данный код: **{code}**\n'
                          'Пользователь которого вы хотите пригласить должен использовать команду **/family join**\n\n'
                          'Также возможно вам прийдётся вызвать команду **/family requests** чтобы принять пользователя*'}

    class JoinFamily:
        description = {Locale.en_US: 'Join the family',
                       Locale.ru: 'Присоединиться в семью'}
        family_id_name = {Locale.en_US: 'id',
                          Locale.ru: 'id'}
        family_id_desc = {Locale.en_US: 'Name for your family',
                          Locale.ru: 'Вы можете получить ID семьи у главы семьи. /family invite'}
        dm_join_request_title = {'en': 'Join request',
                                 'ru': 'Запрос на вступление'}
        dm_join_request_desc = {'en': '***{user}** wants to join your family (**{family}**)*',
                                'ru': '***{user}** хочет вступить в вашу семью (**{family}**)*'}
        request_sent_title = {'en': 'Request has been sent',
                              'ru': 'Запрос отправлен'}
        request_sent_desc = {'en': '*You have submitted a request to join **{family}**. Wait to be accepted*',
                             'ru': '*Вы отправили запрос на вступление в **{family}**. Ждите пока вас примут*'}
        # request_sent_not_dm_desc = {'en': '*You have submitted a request to join **{family}**. Wait to be accepted*',
        #                      'ru': '*Вы отправили запрос на вступление в **{family}**. Вас*'}
        scd_title = {'en': 'You joined',
                     'ru': 'Вы присоединились'}
        scd_desc = {'en': '*You are now a member of the **{family}** family*',
                    'ru': '*Теперь вы участник семьи **{family}***'}

    class LeaveFamily:
        description = {Locale.en_US: 'Leave the family',
                       Locale.ru: 'Покинуть семью'}
        no_family_title = {'en': "You don't have a family",
                           'ru': 'У вас нету семьи'}
        no_family_desc = {'en': "*You can't leave a family that doesn't exist*",
                          'ru': '*Вы не можете покинуть семью, которой не существует*'}
        owner_title = {'en': "You are the owner",
                       'ru': 'Нельзя'}
        owner_desc = {'en': "*You cannot leave the family since you are the owner*",
                      'ru': '*Вы не можете покинуть семью, так как вы глава*'}
        scd_title = {'en': 'You leaved the family',
                     'ru': 'Вы покинули семью'}
        scd_desc = {'en': '*You have left **{family}**. Your family will miss you (Probably)*',
                    'ru': '*Вы ушли за хлебом. **{family}** будет скучать за вами (Наверное)*'}

    class CreateFamily:
        description = {Locale.en_US: 'Create your family',
                       Locale.ru: 'Создать свою семью. Семья важнее всего'}
        name_var_name = {Locale.en_US: 'name',
                         Locale.ru: 'имя'}
        name_var_desc = {Locale.en_US: 'Name for your family',
                         Locale.ru: 'Имя для вашей семьи'}
        desc_var_name = {Locale.en_US: 'description',
                         Locale.ru: 'описание'}
        desc_var_desc = {Locale.en_US: 'Description for your family',
                         Locale.ru: 'Описание для вашей семьи'}
        image_url_var_name = {Locale.en_US: 'image',
                              Locale.ru: 'картинка'}
        image_url_var_desc = {Locale.en_US: 'Link to a picture that will be a symbol of your family',
                              Locale.ru: 'Ссылка на картинку, которая будет символом вашей семьи'}
        private_var_name = {Locale.en_US: 'private',
                            Locale.ru: 'приватная'}
        private_var_desc = {Locale.en_US: 'Will your family be private or open?',
                            Locale.ru: 'Ваша семья будет приватной или открытой?'}
        ask_to_join_var_name = {Locale.en_US: 'ask_to_join',
                                Locale.ru: 'запрос_на_вход'}
        ask_to_join_var_desc = {Locale.en_US: 'To join, a person must send a request',
                                Locale.ru: 'Чтобы присоединится, человек должен будет отправить запрос'}
        scd_title = {'en': 'Family created',
                     'ru': 'Семья создана'}
        scd_desc = {'en': '*You are now the head of the **{family}** family. Congratulations!*',
                    'ru': '*Теперь вы глава семьи **{family}**. Поздравляем!*'}

    class Duel:
        description = {Locale.en_US: 'Arrange a duel between pigs',
                       Locale.ru: 'Устроить дуэль между хряками'}
        user_var_name = {Locale.en_US: 'user',
                         Locale.ru: 'пользователь'}
        user_var_desc = {Locale.en_US: 'The user you want to duel with',
                         Locale.ru: 'Пользователь с которым вы хотите провести дуэль'}
        bet_var_name = {Locale.en_US: 'bet',
                        Locale.ru: 'ставка'}
        bet_var_desc = {Locale.en_US: 'The number of coins you want to bet',
                        Locale.ru: 'Количество монет, которое хотите поставить'}
        user_app_name = {Locale.en_US: 'Challenge to a duel',
                         Locale.ru: 'Вызвать на дуэль'}
        invite_title = {'en': 'Invitation to a duel',
                        'ru': 'Приглашение на дуэль'}
        personal_invite_desc = {'en': '**{opponent}** was invited to duel with **{user}**\n\n'
                                      '- Bet: **{bet}** 🪙',
                                'ru': '**{opponent}** был приглашен на дуэль с **{user}**\n\n'
                                      '- Ставка: **{bet}** 🪙'}
        personal_invite_dm_desc = {'en': '**You** were invited to duel with **{user}**\n\n'
                                         '- Bet: **{bet}** 🪙',
                                   'ru': '**Вы** были приглашены на дуэль с **{user}**\n\n'
                                         '- Ставка: **{bet}** 🪙\n'}
        duel_canceled_title = {'en': 'Duel was canceled',
                               'ru': 'Дуэль была отменена'}
        opponent_reject_desc = {'en': '- **{user}** declined duel invitation',
                                'ru': '- **{user}** отклонил приглашение на дуэль'}
        no_money_for_bet_desc = {'en': "- **{user}** is so poor that he didn't have enough money to bet",
                                 'ru': '- **{user}** настолько бедный, что ему не хватило денег на ставку'}
        no_response_desc = {'en': "- **{user}** did not come to the duel",
                            'ru': '- **{user}** не пришёл на дуэль'}
        fight_will_start_in = {'en': 'Duel will start in {time_to_start} s',
                               'ru': 'Дуэль начнётся через {time_to_start} с'}
        fight_starting_field_value = {'en': '```Weight: {weight} kg\n'
                                            'Win chance: {chance} %```',
                                      'ru': '```Вес: {weight} кг\n'
                                            'Шанс на победу: {chance} %```'}
        fight_is_going_title = {'en': 'Duel is going...',
                                'ru': 'Идёт дуэль...'}
        fight_ended_title = {'en': 'Duel ended',
                             'ru': 'Дуэль окончена'}
        fight_ended_desc = {'en': '# {user} won the duel\n'
                                  '- **{user}** won **{money_earned}** 🪙',
                            'ru': '# {user} выиграл дуэль\n'
                                  '- **{user}** получил **{money_earned}** 🪙'}
        message_url_btn = {'en': 'Message',
                           'ru': 'Сообщение'}

    class TransferMoney:
        description = {Locale.en_US: 'Transfer money to another user',
                       Locale.ru: 'Перевести деньги другом пользователю'}
        user_var_name = {Locale.en_US: 'user',
                         Locale.ru: 'пользователь'}
        user_var_desc = {Locale.en_US: 'User you want to transfer money',
                         Locale.ru: 'Пользователь которому перевести деньги'}
        amount_var_name = {Locale.en_US: 'amount',
                           Locale.ru: 'количество'}
        amount_var_desc = {Locale.en_US: 'Amount of money to transfer',
                           Locale.ru: 'Количество денег для перевода'}
        message_var_name = {Locale.en_US: 'message',
                            Locale.ru: 'сообщение'}
        message_var_desc = {Locale.en_US: 'The message the user will receive',
                            Locale.ru: 'Сообщение, которое получит пользователь'}
        scd_title = {'en': 'Transaction was successful',
                     'ru': 'Транзакция прошла успешно'}
        scd_desc = {'en': '**{money}** 🪙 were sent to **{user}** account',
                    'ru': '**{money}** 🪙 были отправлены на счёт **{user}**'}
        cancel_title = {'en': 'Transaction was canceled',
                        'ru': 'Транзакция была отменена'}
        cancel_desc = {'en': '*You changed your mind about sending your money*',
                       'ru': '*Вы передумали отправлять свои деньги*'}
        event_title = {'en': 'You got some money',
                       'ru': 'Вам перевели деньги'}
        event_desc = {'en': '***{user}** transferred **{money}** 🪙 to your account*',
                      'ru': '***{user}** перевёл на ваш счёт **{money}** 🪙*'}
        confirm_description = {'en': 'Are you sure you want to send **{money}** 🪙 to **{user}**?\n\n'
                                     '- Commission is **{commission}** %\n'
                                     '- **{money_with_commission}** 🪙 will be charged from your account',
                               'ru': 'Вы точно хотите отправить **{money}** 🪙 на счёт **{user}**?\n\n'
                                     '- Коммисия составляет **{commission}** %\n'
                                     '- С вашего счёта снимут **{money_with_commission}** 🪙'}

    class Rename:
        description = {Locale.en_US: 'Rename your pig',
                       Locale.ru: 'Переименовать своего хряка'}
        name_var_name = {Locale.en_US: 'name',
                         Locale.ru: 'имя'}
        name_var_desc = {Locale.en_US: 'New name for pig',
                         Locale.ru: 'Новое имя для свинтуса'}
        scd_title = {'en': 'New pig name: {pig}',
                     'ru': 'Новое имя хряка: {pig}'}

    class Profile:
        description = {Locale.en_US: 'View your profile',
                       Locale.ru: 'Посмотреть свой профиль'}
        user_app_name = {Locale.en_US: 'Profile',
                         Locale.ru: 'Профиль'}
        user_var_name = {Locale.en_US: 'user',
                         Locale.ru: 'пользователь'}
        user_var_desc = {Locale.en_US: 'The user you want to see the profile of',
                         Locale.ru: 'Пользователь, у которого вы хотите посмотреть профиль'}
        profile_title = {'en': '{user}\'s profile',
                         'ru': 'Профиль {user}'}
        profile_desc = {'en': '> Balance: **{balance}** 🪙\n\n'
                              '> Pig name: **{pig_name}**\n'
                              '> Age: **{age}**\n'
                              '> Weight: **{weight}** kg',
                        'ru': '> Баланс: **{balance}** 🪙\n\n'
                              '> Имя хряка: **{pig_name}**\n'
                              '> Возраст: **{age}**\n'
                              '> Вес: **{weight}** кг'}
        pig_field_title = {'en': 'Pig',
                           'ru': 'Свинтус'}
        pig_field_value = {'en': 'Pig name: **{pig_name}**\n'
                                 'Weight: **{weight}** kg',
                           'ru': 'Имя хряка: **{pig_name}**\n'
                                 'Вес: **{weight}** кг'}

    class Stats:
        description = {Locale.en_US: 'View your stats',
                       Locale.ru: 'Посмотреть свою статистику'}
        base_stats = {'en': 'Base stats',
                      'ru': 'Основная статистика'}
        commands_stats = {'en': 'Commands',
                          'ru': 'Команды'}
        sell_stats = {'en': 'Sells',
                      'ru': 'Продажи'}
        base_stats_desc = {'en': 'Pig fed: {pig_fed} times\n'
                                 'Commands were used: {commands_used}\n'
                                 'Total money earned: {money_earned} 🪙\n'
                                 'Total items sold: {items_sold}',
                           'ru': 'Хряк покормлен: {pig_fed} раз\n'
                                 'Команд использовано: {commands_used}\n'
                                 'Всего денег заработано: {money_earned} 🪙\n'
                                 'Всего предметов продано: {items_sold}'}
        commands_stats_desc = {'en': 'How many times have you used the following commands:',
                               'ru': 'Сколько раз вы использовали следующие команды:'}
        sell_stats_desc = {'en': 'How many items you sold:',
                           'ru': 'Сколько предметов вы продали:'}
        no_stats = {'en': 'No stats',
                    'ru': 'Нету статистики'}

    class Top:
        description = {Locale.en_US: 'Players top',
                       Locale.ru: 'Топ игроков'}
        weight_top_title = {'en': 'Weight top',
                            'ru': 'Топ по весу'}
        weight_top_field_value = {'en': 'Pig name: {name}\n'
                                        'Pig weight: {weight} kg',
                                  'ru': 'Имя хряка: {name}\n'
                                        'Вес хряка: {weight} кг'}
        server_var_name = {Locale.en_US: 'server_only',
                           Locale.ru: 'только_сервер'}
        server_var_description = {Locale.en_US: 'Show top members on the server',
                                  Locale.ru: 'Показать топ участников на сервере'}
        money_top_title = {'en': 'Money top',
                           'ru': 'Топ богачей'}
        money_top_field_value = {'en': 'Balance: {money}',
                                 'ru': 'Баланс: {money}'}
        placeholder = {'en': 'View profile',
                       'ru': 'Посмотреть профиль'}

    class Help:
        description = {Locale.en_US: 'Get help for bot',
                       Locale.ru: 'Хряковое пособие и обучение'}
        basic_help_title = {'en': 'Basic Knowledge',
                            'ru': 'Базовые знания'}
        basic_help_desc = {
            'en': '> Before you start raising your boar, you must change the language (if you haven\'t already). </language:1107272196931461179>\n\n'
                  '> To start playing, enter the command </feed:1107375400734179428>. The pig will get a few kilograms of fat, and you will get manure. (Sometimes a boar can lose weight.)\n\n'
                  '> All your items will be visible in </inventory:1103128828345327636>. There you can sell or use the item. To view your balance use </profile:1107272196931461171>\n\n'
                  '> Where to spend money? You can spend the loot in the store </shop:1107272196931461175>, where you can buy some useful items, as well as skins.\n\n'
                  '> To put the skins on the boar, go to the wardrobe </wardrobe:1107272196931461174>. Here you can see all your skins and customize your pig\n\n'
                  '> If you want to have a fight between boars then use </duel:1111846289311793302>\n'
                  '> **What determines the chances of winning a duel:**\n'
                  '> - *The greater the weight, the greater the chances*\n'
                  '> - *If the boar is full, this will also increase the chances*\n\n'
                  '> You can make the piggie speak with the command </say:1108523630276653137>\n\n'
                  'That\'s all, good luck!',
            'ru': '> Перед тем как начать выращивать своего хряка ты должен поменять язык (если ты его ещё не поменял). </language:1107272196931461179>\n\n'
                  '> Чтобы начать играть, введи команду </feed:1107375400734179428>. Свинья получит несколько килограмм сала, а ты получишь навоз. (Иногда хряк может похудеть).\n\n'
                  '> Все твои предметы будут видны в </inventory:1103128828345327636>. Там ты сможешь продать или использовать предмет. Для просмотра баланса используй </profile:1107272196931461171>\n\n'
                  '> Куда тратить деньги? Потратить бабло можно в магазине </shop:1107272196931461175>, там ты сможешь купить некоторые полезные предметы, а также скины.\n\n'
                  '> Для того чтобы надеть скины на хряка, зайди в гардероб </wardrobe:1107272196931461174>. Здесь ты сможешь посмотреть все свои скины и костомизировать своего пига\n\n'
                  '> Если ты хочешь устроить бой между хряками то используй </duel:1111846289311793302>\n'
                  '> **От чего зависят шансы на победу в дуэли:**\n'
                  '> - *Чем больше вес, тем больше шансы*\n'
                  '> - *Если хряк сыт то это также увеличит шансы*\n\n'
                  '> Ты можешь заставить свинтуса говорить через команду </say:1108523630276653137>\n\n'
                  '> Также у бота есть свой сервер: **https://discord.gg/xFvV6wnWUd**\n'
                  '> *На сервере ты сможешь помочь боту в развитии и предложить свои идеи*\n\n'
                  'На этом всё, удачи!'}

    class Say:
        description = {Locale.en_US: 'Make hryak say something',
                       Locale.ru: 'Заставить хряка сказать что-то'}
        text_var_name = {Locale.en_US: 'text',
                         Locale.ru: 'текст'}
        text_var_description = {Locale.en_US: 'Use "\\\\" to go to the next line',
                                Locale.ru: 'Используйте "\\\\" для перехода на следующую строку'}
        user_var_name = {Locale.en_US: 'user',
                         Locale.ru: 'пользователь'}
        user_var_description = {Locale.en_US: 'Speak for the user',
                                Locale.ru: 'Говорить от лица пользователя'}

    class Report:
        description = {Locale.en_US: 'Report bug',
                       Locale.ru: 'Сообщить о баге'}
        text_var_name = {Locale.en_US: 'text',
                         Locale.ru: 'текст'}
        text_var_desc = {Locale.en_US: 'Describe a bug',
                         Locale.ru: 'Описание бага'}
        attachment_var_name = {Locale.en_US: 'attachment',
                               Locale.ru: 'картинка'}
        attachment_var_desc = {Locale.en_US: 'Attach a photo',
                               Locale.ru: 'Скриншот с багом'}
        title = {
            'en': 'Report sent!',
            'ru': 'Ваш репорт был отправлен'}
        desc = {
            'en': 'Thank you for helping to develop the bot\n\n*Contact email: brevnoo@proton.me*',
            'ru': 'Хряк доволен за твою помощь, спасибо'}

    class ChooseLanguage:
        title = {'en': 'Choose language',
                 'ru': 'Сначала выбери язык'}
        desc = {'en': 'Choose the language in which the bot will grunt',
                'ru': 'Выбери язык на котором бот будет хрюкать'}
        placeholder = {'en': 'Choose language',
                       'ru': 'Выберите язык'}

    class SetLanguage:
        description = {
            Locale.en_US: 'Change bot language',
            Locale.ru: 'Изменить язык бота'
        }
        language_var_name = {
            Locale.en_US: 'language',
            Locale.ru: 'язык'
        }
        scd_title = {
            'en': 'New bot language: **English**',
            'ru': 'Новый язык бота: **Русский**'
        }
        scd_desc = {
            'en': 'Now the bot will speak the freedom language 🦅🦅',
            'ru': 'Теперь бот будет говорить на великом и могучем 💪'
        }

    class PromoCode:
        description = {Locale.en_US: 'Use promo code',
                       Locale.ru: 'Использовать промо код'}
        code_var_name = {Locale.en_US: 'code',
                         Locale.ru: 'код'}
        code_var_desc = {Locale.en_US: 'Enter your promo code',
                         Locale.ru: 'Введите ваш промо-код'}
        promo_code_used_error_title = {'en': 'You have already used this promo code',
                                       'ru': 'Вы уже использовали этот промо код'}
        promo_code_used_error_desc = {
            'en': 'The cleverest? You cannot use the same promo code multiple times',
            'ru': 'Самый умный? Нельзя использовать один и тот же промо код несколько раз'}
        promocode_not_exist_title = {'en': 'Invalid promo code',
                                     'ru': 'Недействительный промо код'}
        promocode_not_exist_desc = {
            'en': '*This promo code does not exist*',
            'ru': '*Такого промо кода не существует*'}
        cant_use_promocode_title = {'en': 'Invalid promo code',
                                    'ru': 'Невозможно использовать промокод'}
        cant_use_promocode_desc = {
            'en': "*For some reason you can't use this promo code*",
            'ru': '*По какой-то причине вы не можете использовать этот промокод*'}
        promocode_expired_title = {'en': 'Promo code has expired',
                                   'ru': 'Промо код истёк'}
        promocode_expired_desc = {
            'en': "*The promo code has expired and is therefore no longer valid.*",
            'ru': '*Срок годности промокода истёк, поэтому он больше не рабочий*'}
        promocode_used_too_many_times_title = {'en': 'Invalid promo code',
                                               'ru': 'Промо код использован'}
        promocode_used_too_many_times_desc = {
            'en': 'This promo code has already been used and is therefore no longer valid.',
            'ru': 'Этот промо код уже использовали, поэтому он больше недействителен'}
        promo_code_used_title = {'en': 'Promo code used',
                                 'ru': 'Промо код активирован'}
        you_got_desc = {'en': 'You got:',
                        'ru': 'Вы получили:'}

    class PoopEaten:
        not_enough_money_for_doctor_title = {'en': 'Not enough money',
                                             'ru': 'Недостаточно средств'}
        not_enough_money_for_doctor_desc = {'en': "You don't have enough money to pay the doctor\n\n"
                                                  '*- Doctor takes pity on a beggar like you and just walks away*',
                                            'ru': 'У вас не хватает денег, чтобы заплатить доктору\n\n'
                                                  '*- Доктор жалеет такого нищего как вы и просто уходит*'}
        ran_away_and_not_payed_title = {'en': 'You ran away',
                                        'ru': 'Вы сбежали'}
        ran_away_and_not_payed_desc = {'en': "*You were able to escape. There doesn't seem to be anyone behind*",
                                       'ru': '*Вы смогли сбежать. Кажется никого позади нету*'}
        payed_to_doctor_title = {'en': 'You paid the doctor',
                                 'ru': 'Вы заплатили доктору'}
        payed_to_doctor_desc = {'en': '*The doctor took the money and left*',
                                'ru': '*Доктор взял деньги и уехал*'}

    class RateBot:
        title = {'en': 'Hey, do you like the bot?',
                 'ru': 'Эй, нравится бот?'}
        desc = {'en': 'If yes, then you can rate him on the site',
                'ru': 'Если да, то можешь оценить его на сайте'}
        later_btn = {'en': 'Later',
                     'ru': 'Позже'}
        support_btn = {'en': 'Support',
                       'ru': 'Оценить'}

    class Global:
        page = {'en': 'Page',
                'ru': 'Страница'}
        date = {'en': 'Date',
                'ru': 'Дата'}
        requests = {'en': 'Requests',
                    'ru': 'Запросы'}
        sent = {'en': 'Sent',
                'ru': 'Отправлено'}
        are_you_sure = {'en': 'Are you sure?',
                        'ru': 'Вы уверены?'}
        cost = {'en': 'Cost',
                'ru': 'Цена'}
        cost_per_item = {'en': 'Price/pc',
                         'ru': 'Цена/шт'}
        price = {'en': 'Price',
                 'ru': 'Стоимость'}
        type = {'en': 'Type',
                'ru': 'Тип'}
        amount = {'en': 'Amount',
                  'ru': 'Количество'}
        description = {'en': 'Description',
                       'ru': 'Описание'}
        resource = {'en': 'Resource',
                    'ru': 'Ресурс'}
        head_owner = {'en': 'Owner',
                      'ru': 'Глава'}
        use = {'en': 'Use',
               'ru': 'Использовать'}
        sell = {'en': 'Sell',
                'ru': 'Продать'}
        run_away = {'en': 'Run away',
                    'ru': 'Сбежать'}
        pay = {'en': 'Pay',
               'ru': 'Заплатить'}
        preview = {'en': 'Preview',
                   'ru': 'Предосмотр'}
        wear = {'en': 'Wear',
                'ru': 'Надеть'}
        remove_cloth = {'en': 'Remove',
                        'ru': 'Снять'}
        rarity = {'en': 'Rarity',
                  'ru': 'Редкость'}
        accept = {'en': 'Accept',
                  'ru': 'Принять'}
        reject = {'en': 'Reject',
                  'ru': 'Отклонить'}
        buy = {'en': 'Buy',
               'ru': 'Купить'}
        reason = {'en': 'Reason',
                  'ru': 'Причина'}
        created = {'en': 'Created',
                   'ru': 'Создан'}
        owner = {'en': 'Owner',
                 'ru': 'Владелец'}
        icon = {'en': 'Icon',
                'ru': 'Аватарка'}
        nicknames = {'en': 'Nicknames',
                     'ru': 'Никнеймы'}
        no_icon = {'en': 'No Icon',
                   'ru': 'Без Аватарки'}
        need = {'en': 'Need',
                'ru': 'Нужно'}
        channels = {'en': 'Channels',
                    'ru': 'Каналы'}
        total = {'en': 'Total',
                 'ru': 'Всего'}
        open = {'en': 'Open',
                'ru': 'Открыть'}
        category = {'en': 'Category',
                    'ru': 'Категорий'}
        text = {'en': 'Text',
                'ru': 'Текстовых'}
        voice = {'en': 'Voice',
                 'ru': 'Голосовых'}
        forum = {'en': 'Forum',
                 'ru': 'Форум'}
        stage = {'en': 'Stage',
                 'ru': 'Трибуны'}
        members = {'en': 'Members',
                   'ru': 'Участники'}
        users = {'en': 'Users',
                 'ru': 'Людей'}
        bots = {'en': 'Bots',
                'ru': 'Ботов'}
        bot_roles = {'en': 'Bot roles',
                     'ru': 'Ролей ботов'}
        premium = {'en': 'Premium',
                   'ru': 'Премиум'}
        role = {'en': 'Role',
                'ru': 'Роль'}
        roles = {'en': 'Roles',
                 'ru': 'Роли'}
        bans = {'en': 'Bans',
                'ru': 'Баны'}
        messages = {'en': 'Messages',
                    'ru': 'Сообщения'}
        invites = {'en': 'Invites',
                   'ru': 'Приглашения'}
        expires = {'en': 'Expires',
                   'ru': 'Истекает'}
        animated = {'en': 'Animated',
                    'ru': 'Анимированых'}
        stickers = {'en': 'Stickers',
                    'ru': 'Стикеров'}
        no_emojis = {'en': 'No emojis',
                     'ru': 'Нету эмодзи'}
        emojis = {'en': 'Emojis',
                  'ru': 'Эмодзи'}
        system_channel = {'en': 'System channel',
                          'ru': 'Системный канал'}
        join_messages = {'en': 'Join messages',
                         'ru': 'Нач. сообщения'}
        join_replies = {'en': 'Join replies',
                        'ru': 'Ответы'}
        boost_messages = {'en': 'Boost messages',
                          'ru': 'Буст уведомления'}
        reminder = {'en': 'Reminder',
                    'ru': 'Напоминания'}
        limits = {'en': 'Limits',
                  'ru': 'Лимиты'}
        emojis_limit = {'en': 'Emojis limit',
                        'ru': 'Лимит эмодзи'}
        stickers_limit = {'en': 'Stickers limit',
                          'ru': 'Лимит стикеров'}
        bitrate_limit = {'en': 'Bitrate limit',
                         'ru': 'Лимит битрейта'}
        files_limit = {'en': 'Files limit',
                       'ru': 'Лимит файлов'}
        safety = {'en': 'Safety',
                  'ru': 'Безопасность'}
        mfa = {'en': 'MFA',
               'ru': 'MFA'}
        attempt = {'en': 'Attempt',
                   'ru': 'Попытка'}
        verification = {'en': 'Verification',
                        'ru': 'Верификация'}
        nsfw_level = {'en': 'NSFW level',
                      'ru': 'Уровень NSFW'}
        content_filter = {'en': 'Content filter',
                          'ru': 'Фильтр контента'}
        default_notifications = {'en': 'Default notifications',
                                 'ru': 'Уведомления по умолчанию'}
        other = {'en': 'Other',
                 'ru': 'Другое'}
        yes = {'en': 'Yes',
               'ru': 'Да'}
        no = {'en': 'No',
              'ru': 'Нет'}
        true_yes_command = {Locale.en_US: '✅ True',
                            Locale.ru: '✅ Да'}
        false_no_command = {Locale.en_US: '❌ False',
                            Locale.ru: '❌ Нет'}
        total_bans = {'en': 'Total Bans',
                      'ru': 'Всего банов'}
        total_invites = {'en': 'Total Invites',
                         'ru': 'Всего приглашений'}
        locale = {'en': 'Locale',
                  'ru': 'Язык'}
        rules = {'en': 'Rules',
                 'ru': 'Правила'}
        community = {'en': 'Community',
                     'ru': 'Комьюнити'}
        click = {'en': 'Click',
                 'ru': 'Нажми'}
        joined = {'en': 'Joined',
                  'ru': 'Присоединился'}
        name_ = {'en': 'Name',
                 'ru': 'Имя'}
        status = {'en': 'Status',
                  'ru': 'Статус'}
        play = {'en': 'Playing',
                'ru': 'Играет в'}
        stream = {'en': 'Streaming',
                  'ru': 'Стримит'}
        listen = {'en': 'Listening',
                  'ru': 'Слушает'}
        watching = {'en': 'Watching',
                    'ru': 'Смотрит'}
        competing = {'en': 'Competing in',
                     'ru': 'Соревнуется в'}
        never = {'en': 'Never',
                 'ru': 'Никогда'}
        total_members = {'en': 'Total members',
                         'ru': 'Всего участников'}
        position = {'en': 'Position',
                    'ru': 'Позиция'}
        last_update = {'en': 'Last update',
                       'ru': 'Последнее обновление'}
        uses = {'en': 'Uses',
                'ru': 'Использований'}
        cook = {'en': 'Cook',
                'ru': 'Приготовить'}
        total_roles = {'en': 'Total roles',
                       'ru': 'Всего ролей'}
        total_channels = {'en': 'Total channels',
                          'ru': 'Всего каналов'}
        template_info = {'en': 'Template info',
                         'ru': 'О шаблоне'}
        source_guild_id = {'en': 'Source server ID',
                           'ru': 'ID исходного сервера'}
        creator_id = {'en': 'Creator ID',
                      'ru': 'ID создателя'}
        your_number = {'en': 'Your number',
                       'ru': 'Ваше число'}
        numbers = {'en': 'Numbers',
                   'ru': 'Числа'}
        color = {'en': 'Color',
                 'ru': 'Цвет'}
        weight = {'en': 'Weight',
                  'ru': 'Вес'}
        template = {'en': 'Template',
                    'ru': 'Шаблон'}
        templates = {'en': 'Templates',
                     'ru': 'Шаблоны'}
        creator = {'en': 'Creator',
                   'ru': 'Создатель'}
        kilograms_short = {'en': 'kg',
                           'ru': 'кг'}
        options = {'en': 'Options',
                   'ru': 'Настройки'}
        mentionable = {'en': 'Mentionable',
                       'ru': 'Упоминаимая'}
        hoist = {'en': 'Hoist',
                 'ru': 'Отдельная'}
        integration = {'en': 'Integration',
                       'ru': 'Интеграция'}
        refresh = {'en': 'Refresh',
                   'ru': 'Обновить'}
        reload = {'en': 'Reload',
                  'ru': 'Перезагрузить'}
        links = {'en': 'Links',
                 'ru': 'Ссылки'}
        title = {'en': 'Title',
                 'ru': 'Заголовок'}
        footer = {'en': 'Footer',
                  'ru': 'Нижний текст'}
        image_url = {'en': 'Image URL',
                     'ru': 'Ссылка на картинку'}
        thumbnail_url = {'en': 'Thumbnail URL',
                         'ru': 'Ссылка на маленькую картинку'}
        stats = {'en': 'Stats',
                 'ru': 'Статистика'}
        all_skins = {'en': 'All skins',
                     'ru': 'Все скины'}
        all_items = {'en': 'All items',
                     'ru': 'Все вещи'}
        everything = {'en': 'Everything',
                      'ru': 'Показать всё'}
        got_it_btn = {'en': 'Got it',
                      'ru': 'Хорошо'}
        choose_category = {'en': 'Choose category',
                           'ru': 'Выберите категорию'}
        none = {'en': 'No',
                'ru': 'Нету'}
        message = {'en': 'Message',
                   'ru': 'Сообщение'}
        you_have_amount = {'en': 'You have: {max_amount}',
                           'ru': 'У вас есть: {max_amount}'}

    class ErrorCallbacks:
        pig_feed_cooldown_title = {'en': 'Your pig is not yet hungry',
                                   'ru': 'Ваш хряк ещё не голоден'}
        pig_feed_cooldown_desc = {'en': '**{pig}** gets hungry **<t:{timestamp}:R>**',
                                  'ru': '**{pig}** проголодается **<t:{timestamp}:R>**'}
        pig_meat_cooldown_title = {'en': 'Your pig is not yet hungry',
                                   'ru': 'Вы слишком жестокие'}
        pig_meat_cooldown_desc = {'en': "You can't skim fat off **{pig}**\n"
                                        "Try again **<t:{timestamp}:R>**",
                                  'ru': 'Вы не можете так часто снимать сало с **{pig}**\n\n'
                                        '*Попробуйте ещё раз **<t:{timestamp}:R>***'}
        pig_breed_cooldown_title = {'en': 'Calm down',
                                    'ru': 'Успокойся'}
        pig_breed_cooldown_desc = {'en': "**{pig}** is too tired and can't have kids\n"
                                         "Try again **<t:{timestamp}:R>**",
                                   'ru': '**{pig}** слишком устал и не может заводить детей\n\n'
                                         '*Попробуйте ещё раз **<t:{timestamp}:R>***'}
        shop_buy_cooldown_title = {'en': 'Product is out of stock',
                                   'ru': 'Товар закончился'}
        shop_buy_cooldown_desc = {'en': "**{item}** is out of stock and out of stock\n"
                                        "New product will be **<t:{timestamp}:R>**",
                                  'ru': '**{item}** закончился и его больше нету на складе\n\n'
                                        '*Новый товар привезут **<t:{timestamp}:R>***'}
        language_not_supported_title = {'en': 'Your language is not supported',
                                        'ru': 'Ваш язык не поддерживается'}
        language_not_supported_desc = {'en': "*Try changing the language and try again*",
                                       'ru': '*Попробуйте поменять язык и попробуйте заново*'}
        wrong_component_clicked_title = {'en': "It's not your message",
                                         'ru': 'Это не ваше сообщение'}
        wrong_component_clicked_desc = {'en': "You can't push tie people's buttons",
                                        'ru': 'Ты не можешь нажимать на чужие кнопки'}
        not_enough_money_title = {'en': 'Not enough money',
                                  'ru': 'Недостаточно денег'}
        not_enough_money_desc = {'en': "*You don't have enough money to do this*",
                                 'ru': '*У вас не достаточно денег, чтобы сделать это*'}
        no_item_title = {'en': "You don't have a {item}",
                         'ru': 'У вас нету предмета "{item}"'}
        no_item_desc = {'en': "*Unfortunately, you couldn't find this item in your storage*",
                        'ru': '*К сожалению, вы не смогли найти этот предмет у себя в хранилище*'}
        not_allowed_to_use_command_title = {'en': "You are not allowed to use this command",
                                            'ru': 'Вам не разрешено использовать эту команду'}
        not_allowed_to_use_command_desc = {'en': "*You need special permission to use the command*",
                                           'ru': '*Вам нужно специальное разрешение, чтобы использовать команду*'}
        nsfw_required_title = {'en': "You are not allowed to use this command",
                               'ru': 'Это NSFW команда'}
        nsfw_required_desc = {'en': "*You need to be in an NSFW channel to use the command*",
                              'ru': '*Вам нужно находится в NSFW канале, чтобы использовать команду*'}
        not_owner_desc = {'en': "*Only the bot owner can use this command*",
                          'ru': '*Только владелец бота может использовать эту команду*'}
        bot_as_opponent_duel_title = {'en': "Are you playing against a bot?",
                                      'ru': 'Ты против бота играешь?'}
        bot_as_opponent_duel_desc = {
            'en': "I'll tell you a secret, bots don't know how to participate in duels. They can't even press a button.",
            'ru': 'Расскажу секрет, боты не умеют участвовать в дуэлях. Они даже на кнопку нажать не могут'}
        bot_as_partner_breed_title = {'en': "Going to have kids with a bot?",
                                      'ru': 'Собрался завести детей с ботом?'}
        bot_as_partner_breed_desc = {
            'en': "The future is not close enough for you to breed with robots",
            'ru': 'Будущее не настолько близко, чтобы вы могли заводить потомство с роботами'}
        cant_play_with_yourself_duel_title = {'en': "Going to play by yourself?",
                                              'ru': 'Собрался играть сам с собой?'}
        cant_play_with_yourself_duel_desc = {'en': "I thought users wouldn't choose themselves as opponents."
                                                   "I think I was wrong",
                                             'ru': 'Я думал что пользователи не станут выбирать самого себя в качестве соперника. '
                                                   'Кажется, я ошибался'}
        cant_breed_with_yourself_title = {'en': "Hey hey hey",
                                          'ru': 'Воу воу воу'}
        cant_breed_with_yourself_desc = {
            'en': "I understand that you love yourself so much that you chose yourself as a partner, but unfortunately you can’t",
            'ru': 'Я понимаю что вы любите себя настолько сильно что выбрали себя в качестве партнёра, но так к сожалению нельзя'}
        cooldown_title = {'en': "Cooldown",
                          'ru': 'Притормози'}
        cooldown_desc = {'en': 'You use the command too often\n\n'
                               '*Try again **<t:{timestamp}:R>***',
                         'ru': 'Ты слишком часто используешь команду\n\n'
                               '*Попробуй ещё раз **<t:{timestamp}:R>***'}
        no_mangal_to_cook = {'en': '*How are you going to roast the meat? Buy a grill!*',
                             'ru': '*Как ты собираешься жарить мясо? Купи мангал!*'}
        user_in_black_list_title = {'en': "You are in black list",
                                    'ru': 'Вы в чёрном списке'}
        user_in_black_list_desc = {'en': "*You are blacklisted by the bot, so you cannot use it*",
                                   'ru': '*Вы находитесь в чёрном списке бота, поэтому не можете использовать его.\n'
                                         '- Если вы считаете что это ошибка, то заходите на [сервер поддержки](https://discord.gg/xFvV6wnWUd)*'}
        unknown_error_title = {'en': "Unknown error",
                               'ru': 'Неизвестная ошибка'}
        unknown_error_desc = {
            'en': "*Oops, something seems to have gone wrong. You can report it via the </report:1106680848167739493> command*",
            'ru': '*Упс, кажется что-то пошло не так. Вы можете сообщить об этом через команду </report:1106680848167739493>*'}
        bot_missing_perms_title = {'en': "Hryak has no rights",
                                   'ru': 'У хряка нету прав'}
        user_missing_perms_title = {'en': "You have no rights 👩",
                                    'ru': 'У вас нет прав 👩'}
        modal_input_is_not_number_title = {'en': 'Invalid input',
                                           'ru': 'Неверный ввод'}
        modal_input_is_not_number_desc = {
            'en': "What you entered does not look like a number, but it would be better a number",
            'ru': 'То что ты ввёл не похоже на число, а лучше бы это было числом'}

    ItemTypes = {
        'resource': {'en': 'Resource',
                     'ru': 'Ресурс'},
        'consumable': {'en': 'Сonsumable',
                       'ru': 'Расходник'},
        'tool': {'en': 'Tool',
                 'ru': 'Инструмент'},
        'skin': {'en': 'Skin',
                 'ru': 'Скин'},
        'case': {'en': 'Case',
                 'ru': 'Кейс'},
        'skin:hat': {'en': 'Headdress',
                     'ru': 'Головной убор'},
        'skin:glasses': {'en': 'Glasses',
                         'ru': 'Очки'},
        'skin:tie': {'en': 'Tie',
                     'ru': 'Галстук'},
        'skin:body': {'en': 'Skin color',
                      'ru': 'Цвет кожи'},
        'skin:pupils': {'en': 'Pupils',
                        'ru': 'Зрачки'},
        'skin:tattoo': {'en': 'Tattoo',
                        'ru': 'Тату'},
        'skin:legs': {'en': 'Legs',
                      'ru': 'Ноги'},
        'skin:nose': {'en': 'Nose',
                      'ru': 'Нос'},
        'skin:_nose': {'en': 'Nose',
                       'ru': 'Нос'},
        'skin:eyes': {'en': 'Eyes',
                      'ru': 'Глаза'},
        'skin:suit': {'en': 'Suit',
                      'ru': 'Костюм'},
        'skin:piercing_nose': {'en': 'Piercing - nose',
                               'ru': 'Пирсинг - нос'},
        'skin:piercing_ear': {'en': 'Piercing - ear',
                              'ru': 'Пирсинг - ухо'},
        'skin:eye_emotion': {'en': 'Eyes emotion',
                             'ru': 'Эмоция глаз'},
    }

    ItemRarities = {
        '1': {'en': 'Common',
              'ru': 'Обычный'},
        '2': {'en': 'Uncommon',
              'ru': 'Необычный'},
        '3': {'en': 'Rare',
              'ru': 'Редкий'},
        '4': {'en': 'Epic',
              'ru': 'Эпический'},
        '5': {'en': 'Mythical',
              'ru': 'Мифическое'},
        '6': {'en': 'Legendary',
              'ru': 'Легендарный'},
    }

    FamilyRoles = {
        'owner': {'en': 'Owner',
                  'ru': 'Глава'},
        'member': {'en': 'Member',
                   'ru': 'Участник'},
    }

    FamilyRolesEmojis = {
        'owner': '⭐',
        'member': '👤',
    }

    PigAges = {
        '1': {'en': 'Mini-pig',
              'ru': 'Мини-пиг'},
        '2': {'en': 'Teenager',
              'ru': 'Подросток'},
        '3': {'en': 'Mature',
              'ru': 'Зрелый'},
        '4': {'en': 'Adult',
              'ru': 'Взрослый'},
        '5': {'en': 'Elder',
              'ru': 'Старец'},
        '6': {'en': 'Veteran',
              'ru': 'Ветеран'},
        '7': {'en': 'Timeless',
              'ru': 'Вечный'},
    }

    Permissions = {'add_reactions': {'en': 'Add reactions', 'ru': 'Добавлять реакции'},
                   'administrator': {'en': 'Administrator', 'ru': 'Администратор'},
                   'attach_files': {'en': 'Attach files', 'ru': 'Прикреплять файлы'},
                   'ban_members': {'en': 'Ban members', 'ru': 'Банить'},
                   'change_nickname': {'en': 'Change nickname', 'ru': 'Изменять имя'},
                   'connect': {'en': 'Connect', 'ru': 'Подключатся'},
                   'create_forum_threads': {'en': 'Create forum threads', 'ru': 'Создавать ветки на форуме'},
                   'create_instant_invite': {'en': 'Create instant invite', 'ru': 'Создавать приглашение'},
                   'create_private_threads': {'en': 'Create private threads', 'ru': 'Создавать приватные ветки'},
                   'create_public_threads': {'en': 'Create public threads', 'ru': 'Создавать публичные ветки'},
                   'deafen_members': {'en': 'Deafen members', 'ru': 'Отключать звук'},
                   'embed_links': {'en': 'Embed links', 'ru': 'Вставить ссылки'},
                   'external_emojis': {'en': 'External emojis', 'ru': 'Внешние эмодзи'},
                   'external_stickers': {'en': 'External stickers', 'ru': 'Внешние стикеры'},
                   'kick_members': {'en': 'Kick members', 'ru': 'Исключать участников'},
                   'manage_channels': {'en': 'Manage channels', 'ru': 'Управлять каналами'},
                   'manage_emojis': {'en': 'Manage emojis', 'ru': 'Управлять эмодзи'},
                   'manage_emojis_and_stickers': {'en': 'Manage emojis and stickers',
                                                  'ru': 'Управлять смайликами и стикерами'},
                   'manage_events': {'en': 'Manage events', 'ru': 'Управлять событиями'},
                   'manage_guild': {'en': 'Manage guild', 'ru': 'Управлять сервером'},
                   'manage_messages': {'en': 'Manage messages', 'ru': 'Управлять сообщениями'},
                   'manage_nicknames': {'en': 'Manage nicknames', 'ru': 'Управлять именами'},
                   'manage_permissions': {'en': 'Manage permissions', 'ru': 'Управлять правами'},
                   'manage_roles': {'en': 'Manage roles', 'ru': 'Управлять ролями'},
                   'manage_threads': {'en': 'Manage threads', 'ru': 'Управлять ветками'},
                   'manage_webhooks': {'en': 'Manage webhooks', 'ru': 'Управлять вэб-хуками'},
                   'mention_everyone': {'en': 'Mention everyone', 'ru': 'Упоминать everyone'},
                   'moderate_members': {'en': 'Moderate members', 'ru': 'Управлять учатниками'},
                   'move_members': {'en': 'Move members', 'ru': 'Перемещать участников'},
                   'mute_members': {'en': 'Mute members', 'ru': 'Заглушать участников'},
                   'priority_speaker': {'en': 'Priority speaker', 'ru': 'Приоритетный режим'},
                   'read_message_history': {'en': 'Read message history', 'ru': 'Читать историю сообщений'},
                   'read_messages': {'en': 'Read messages', 'ru': 'Читать сообщения'},
                   'request_to_speak': {'en': 'Request to speak', 'ru': 'Попросить выступить'},
                   'send_messages': {'en': 'Send messages', 'ru': 'Отправлять сообщения'},
                   'send_messages_in_threads': {'en': 'Send messages in threads',
                                                'ru': 'Отправлять сообщения в ветки'},
                   'send_tts_messages': {'en': 'Send tts messages', 'ru': 'Отправлять tts сообщения'},
                   'speak': {'en': 'Speak', 'ru': 'Говорить'},
                   'start_embedded_activities': {'en': 'Start embedded activities',
                                                 'ru': 'Начинать встроенные действия'},
                   'stream': {'en': 'Stream', 'ru': 'Стримить'},
                   'use_application_commands': {'en': 'Use application commands', 'ru': 'Использовать команды'},
                   'use_embedded_activities': {'en': 'Use embedded activities',
                                               'ru': 'Использовать встроенные активности'},
                   'use_external_emojis': {'en': 'Use external emojis', 'ru': 'Использовать внешние смайлики'},
                   'use_external_stickers': {'en': 'Use external stickers', 'ru': 'Использовать внешние стикеры'},
                   'use_slash_commands': {'en': 'Use slash commands', 'ru': 'Использовать слэш-команды'},
                   'use_voice_activation': {'en': 'Use voice activation', 'ru': 'Использовать режим рации'},
                   'view_audit_log': {'en': 'View audit log', 'ru': 'Просмотр журнала аудита'},
                   'view_channel': {'en': 'View channel', 'ru': 'Просмотр канала'},
                   'view_guild_insights': {'en': 'View guild insights', 'ru': 'Просмотр статистики сервера'}}

    # _____________________________________________________________________________________

    class Inventory:
        description = {Locale.en_US: 'View your inventory',
                       Locale.ru: 'Посмотреть свой инвентарь'}
        inventory_title = {'en': 'Inventory',
                           'ru': 'Инвентарь'}
        inventory_empty_desc = {'en': '*Your inventory is empty*',
                                'ru': '*Ваш инвентарь пуст*'}
        select_item_placeholder = {'en': 'Choose item',
                                   'ru': 'Выберите предмет'}

    class InventoryItemSellModal:
        label = {'en': 'Amount of items to sell',
                 'ru': 'Количество предметов для продажи'}
        placeholder = {'en': 'You have: {max_amount}',
                       'ru': 'У вас есть: {max_amount}'}
        title = {'en': 'Item selling',
                 'ru': 'Продажа'}

    class InventoryItemSold:
        title = {'en': 'Item sold',
                 'ru': 'Предмет продан'}
        desc = {'en': 'You sold **{item} x{amount}** and received **{money}** 🪙',
                'ru': 'Вы продали **{item} x{amount}** и получили **{money}** 🪙'}

    class InventoryItemCookModal:
        label = {'en': 'Amount of items to cook',
                 'ru': 'Количество предметов для готовки'}
        placeholder = {'en': 'You have: {max_amount}',
                       'ru': 'У вас есть: {max_amount}'}
        title = {'en': 'Cooking',
                 'ru': 'Готовка'}

    class InventoryItemCooked:
        title = {'en': 'Item cooked',
                 'ru': 'Предмет приготовлен'}
        desc = {'en': 'You cooked **{item} x{amount}**',
                'ru': 'Вы приготовили **{item} x{amount}**'}

    class ItemUsed:
        ate_poop_and_poisoned_title = {'en': 'You ate poop',
                                       'ru': 'Вы сьели какаху'}
        ate_poop_and_poisoned_desc = {
            'en': 'You ate poop. You liked its taste, but unfortunately you got poisoned\n\n'
                  '*- A doctor came to you and cured you, but now he asks 5 🪙 for treatment*',
            'ru': 'Вы сьели какашку. Вам понравился её вкус, но к сожалению вы отравились\n\n'
                  '*- К вам пришёл доктор и вылечил вас, но теперь он просит 5 🪙 за лечение*'}
        laxative_title = {'en': 'You used laxative',
                          'ru': 'Вы использовали слабительное'}
        laxative_desc = {
            'en': '**{pig}** will produce more manure on the next **{step}** feedings',
            'ru': '**{pig}** будет давать больше навоза следующие **{step}** кормёжек'}
        case_title = {'en': 'You opened case',
                      'ru': 'Вы открыли кейс'}
        case_desc = {
            'en': '## You got:\n```{items}```',
            'ru': '## Вы получили:\n```{items}```'}

    class Wardrobe:
        description = {Locale.en_US: 'Skins for your pig',
                       Locale.ru: 'Скины для вашего хряка'}
        wardrobe_title = {'en': 'Wardrobe',
                          'ru': 'Гардероб'}
        wardrobe_empty_desc = {'en': '*Your wardrobe is empty*',
                               'ru': '*Ваш гардероб пуст*'}
        select_item_placeholder = {'en': 'Choose item',
                                   'ru': 'Выберите предмет'}

    class WardrobeItemWear:
        title = {'en': 'You put on {item}',
                 'ru': 'Вы надели {item}'}
        desc_list = {'en': ['*This **{item}** really suits you!*'],
                     'ru': ['*Этот **{item}** вам очень идёт!*']}

    class WardrobeItemRemove:
        title = {'en': 'You removed {item}',
                 'ru': 'Вы сняли {item}'}
        desc = {'en': "*Now you don't wear **{item}***",
                'ru': '*Теперь вы не носите **{item}***'}

    class WardrobeItemPreview:
        title = {'en': 'Preview mode',
                 'ru': 'Режим предосмотра'}
        desc = {'en': "*This is how **{item}** will be if you imagine wearing it*",
                'ru': '*Вот как будет выглядеть **{item}**, если вы его наденете*'}

    class Shop:
        description = {Locale.en_US: 'View pig shop',
                       Locale.ru: 'Заглянуть в магазин'}
        shop_empty_desc = {'en': '*Shop is empty now*',
                           'ru': '*Магазин сейчас пустой*'}
        titles = {
            'daily_shop': {'en': 'Daily shop',
                           'ru': 'Ежедневный магазин'},
            'case_shop': {'en': 'Case shop',
                          'ru': 'Кейсы'},
            'static_shop': {'en': 'Shop',
                            'ru': 'Магазин'}
        }

    # 'pregnancy': {'description': {Locale.en_US: 'View boar pregnancy status',
    #                               Locale.ru: 'Посмотреть статус беременности хряка'},
    #               'not_enough_weight_title': {'en': 'Not enough weight',
    #                                           'ru': 'Не достаточно веса'}},
    class ShopItemBought:
        title = {'en': 'You bought {item}',
                 'ru': 'Вы купили {item}'}
        desc = {'en': "Hope you enjoy your purchase. (We do not return money)",
                'ru': 'Надеюсь, вам понравится ваша покупка. (Деньги не возвращаем)'}

    class JoinMessageSet:
        description = {Locale.en_US: 'Set message when user joins server',
                       Locale.ru: 'Установить сообщение, когда пользователь заходит на сервер'}
        channel_var_name = {Locale.en_US: 'channel',
                            Locale.ru: 'канал'}
        channel_var_desc = {Locale.en_US: 'The channel to which the message will be sent',
                            Locale.ru: 'Канал, в который будет отправляться сообщение'}
        message_var_name = {Locale.en_US: 'message',
                            Locale.ru: 'сообщение'}
        message_var_desc = {
            Locale.en_US: 'The message that will be sent when the participant enters. Use {user} to mention',
            Locale.ru: 'Сообщение, которое будет отправляться при заходе участника. Используйте {user} для упоминания'}
        scd_title = {'en': 'Great, the channel is set: {channel}',
                     'ru': 'Отлично, канал установлен: {channel}'}
        scd_desc = {'en': '**Here is the message that will be displayed:**\n\n{message}',
                    'ru': '**Вот сообщение которое будет выводится:**\n\n{message}'}
        reset_scd_title = {'en': 'Join message reset',
                           'ru': 'Приветственное сообщение сброшено'}

    class JoinMessageReset:
        description = {Locale.en_US: 'Reset greeting message settings',
                       Locale.ru: 'Сбросить настройки для приветственного сообщения'}
        scd_title = {'en': 'Join message reset',
                     'ru': 'Приветственное сообщение сброшено'}

    class Pagination:
        wrong_user_title = {'en': 'Hey, it\'s not your message',
                            'ru': 'Эй, это не твоё сообщение'}
        wrong_user_desc = {'en': 'You can\'t just take and flip through tie people\'s pages',
                           'ru': 'Ты не можешь просто взять и листать чужие страницы'}
