import shutil

import requests

from ..core import *


class Translator(discord.app_commands.Translator):
    async def load(self):
        pass

    async def unload(self):
        pass

    async def translate(self, string: discord.app_commands.locale_str, locale: discord.Locale,
                        context: discord.app_commands.TranslationContext):
        if context.location in [discord.app_commands.TranslationContextLocation.command_name,
                                discord.app_commands.TranslationContextLocation.command_description,
                                discord.app_commands.TranslationContextLocation.parameter_name,
                                discord.app_commands.TranslationContextLocation.parameter_description,
                                discord.app_commands.TranslationContextLocation.choice_name]:
            if string.message not in Locales.app_commands_locales:
                return string.message
            if locale in [discord.Locale.russian, discord.Locale.ukrainian]:
                return translate(Locales.app_commands_locales[string.message], 'ru')
            elif locale in [discord.Locale.american_english, discord.Locale.british_english]:
                return translate(Locales.app_commands_locales[string.message], 'en')
            return translate(Locales.app_commands_locales[string.message], 'en')
        return None


class Func:

    @staticmethod
    async def async_speed_test(func, **kwargs):
        start = datetime.datetime.now().timestamp()
        await func(**kwargs)
        final = datetime.datetime.now().timestamp() - start
        return final

    @staticmethod
    def speed_test(func, **kwargs):
        start = datetime.datetime.now().timestamp()
        func(**kwargs)
        final = datetime.datetime.now().timestamp() - start
        return final

    @staticmethod
    def generate_temp_path(key_word: str, file_extension: str = None):
        while True:
            path = f'{config.TEMP_FOLDER_PATH}/{key_word}_{hryak.Func.generate_current_timestamp()}_{random.randrange(10000)}{f'.{file_extension}' if file_extension is not None else ''}'
            if not os.path.exists(path):
                break
        return path

    @staticmethod
    def sort_by_values(dictionary, reverse: bool = False):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse)}

    @staticmethod
    def get_command_name_and_options(ctx):
        name = ctx.data.get('name')
        options = []
        if ctx.data.get('options') is not None:
            options = ctx.data.get('options')[0]
        if isinstance(options, dict) and options.get('options') is not None:
            options = options.get('options')
        command_name = name
        if options and ctx.data.get('options')[0].get('name') is not None:
            command_name += f' {ctx.data.get('options')[0].get('name')}'
        return command_name, options

    @staticmethod
    def str_to_bool(target):
        if target is None:
            return None
        return True if target.lower() in ['✅ true', 'true', '✅', 'yes', 'да', 'так', True] else False

    @staticmethod
    def clear_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)
            return
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'! Failed to delete {file_path}. Reason: {e}')

    @staticmethod
    def generate_footer(inter=None, first_part: str = 'user', second_part: str = '', user: discord.User = None):
        separator = ' ・ '
        if inter is not None:
            if user is None:
                user = inter.user
            if second_part == 'com_name':
                second_part, options = Func.get_command_name_and_options(inter)
                second_part = f'/{second_part}'
        if first_part == 'user':
            first_part = user.display_name
        if not first_part or not second_part:
            separator = ''
        footer = f'{first_part}{separator}{second_part}'
        return footer

    @staticmethod
    def generate_footer_url(footer_url: str = 'user_avatar', user: discord.User = None):
        if footer_url == 'user_avatar' and user is not None:
            if user.avatar is not None:
                footer_url = user.avatar.url
            else:
                footer_url = f'https://cdn.discordapp.com/embed/avatars/{user.default_avatar.key}.png'
        else:
            return None
        return footer_url

    @staticmethod
    def generate_prefix(prefix: str = 'scd', sep: str = '・', backticks: bool = False):
        if prefix is None or not prefix:
            return ''
        prefix_emoji = prefix
        if prefix == 'scd':
            prefix_emoji = '✅'
        elif prefix == 'error':
            prefix_emoji = '❌'
        elif prefix == 'warn':
            prefix_emoji = '⚠️'
        if not backticks:
            prefix = f'{prefix_emoji}{sep}'
        else:
            prefix = f'`{prefix_emoji}`{sep}'
        return prefix

    @staticmethod
    def translate_permissions(perms: list, lang: str):
        missing_perms = []
        for perm in perms:
            if perm in Locales.Permissions:
                missing_perms.append(translate(Locales.Permissions[perm], lang))
            else:
                missing_perms.append(perm.replace('_', ' ').capitalize())
        return missing_perms

    @staticmethod
    def get_image_link_from_path(image_path, name=None, expiration=None, service: str = 'thumbsnap'):
        if service == 'imgbb':
            url = "https://api.imgbb.com/1/upload"
            payload = {
                'key': config.IMGBB_TOKEN,
                'expiration': expiration,
                'name': name
            }
            with open(image_path, 'rb') as image_url:
                files = {
                    'image': image_url
                }
                response = requests.post(url, files=files, data=payload)
            return response.json()['data']['url']
        elif service == 'thumbsnap':
            url = 'https://thumbsnap.com/api/upload'
            files = {'media': open(image_path, 'rb').read()}
            data = {'key': config.THUMBSNAP_TOKEN}
            response = requests.post(url, files=files, data=data)
            return response.json()['data']['media']

    @staticmethod
    def get_changed_page_number(total_pages, current_page, dif):
        if dif > 0:
            if current_page + dif > total_pages:
                current_page = 1
            else:
                current_page += dif
        elif dif < 0:
            if current_page + dif < 1:
                current_page = total_pages
            else:
                current_page += dif
        return current_page

    @staticmethod
    def startswith_list(string, lst: list[str]) -> bool:
        for i in lst:
            if string.startswith(i):
                return True
        return False

    @staticmethod
    def field_inline_alternation(fields: list):
        for i in range(1, len(fields) + 1):
            fields[i - 1]['inline'] = False if i % 3 == 0 else True
        return fields

    @staticmethod
    async def send_data_to_stats_channel(client, servers):
        for i in config.BOT_GUILDS:
            if 'guild_count_channel' in config.BOT_GUILDS[i]:
                channel = client.get_channel(config.BOT_GUILDS[i]['guild_count_channel'])
                try:
                    await channel.edit(name=str(re.sub(r'\d+', str(servers), str(channel))))
                except:
                    pass

    @staticmethod
    def send_data_to_sdc(client, shards: int = 1):
        requests.post(f'https://api.server-discord.com/v2/bots/{client.user.id}/stats',
                      headers={'Authorization': f'SDC {config.SDC_TOKEN}'},
                      json={'servers': len(client.guilds),
                            'shards': shards
                            })

    @staticmethod
    def send_data_to_boticord(client):
        requests.post(f'https://api.boticord.top/bots/{client.user.id}/stats',
                      headers={'Authorization': f'Bot {config.BOTICORD_TOKEN}'},
                      json={'servers': len(client.guilds)})

    @staticmethod
    def cut_text(text, chars, dots: bool = True):
        if len(text) > chars + 1:
            if dots:
                text = text[:chars - 3] + '...'
            else:
                text = text[:chars]
        return text