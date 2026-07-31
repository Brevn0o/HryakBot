from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *


async def generate_top_embed(inter, lang: str, title: str, description: str, users_list: list,
                             user_position: int = None,
                             prefix_emoji: str = None,
                             thumbnail_url=None):
    """
    :type users_list: object
        Example: [('user_id1', '20', 'kg'), ('user_id2', '10', 'kg')]
    """
    leader_emojis = ['🥇', '🥈', '🥉']

    async def generate_line(place, user):
        return f'> {leader_emojis[place] if place < 3 else place + 1}・{await User.get_discord_name(inter.client, user[0])} - **{user[1]}** {user[2]}\n'

    fields = []
    best_users_field = {'name': translate(Locales.Top.best_of_the_bests, lang),
                        'value': '',
                        'inline': False}
    for n, i in enumerate(users_list[:3]):
        best_users_field['value'] += await generate_line(n, i)
    fields.append(best_users_field)
    other_users_field = {'name': translate(Locales.Top.also_not_bad, lang),
                         'value': '',
                         'inline': False}
    for n, i in enumerate(users_list[3:]):
        other_users_field['value'] += await generate_line(n + 3, i)
    if other_users_field['value']:
        fields.append(other_users_field)
    if user_position is not None:
        if other_users_field['value']:
            other_users_field[
                'value'] += f"\n\n{translate(Locales.Top.your_position, lang, format_options={'place': user_position + 1})}"
        elif best_users_field['value']:
            best_users_field[
                'value'] += f"\n\n{translate(Locales.Top.your_position, lang, format_options={'place': user_position + 1})}"
    embed = generate_embed(
        title=title,
        description=description,
        prefix=Func.generate_prefix(prefix_emoji),
        inter=inter,
        thumbnail_url=thumbnail_url,
        fields=fields
    )
    return embed
