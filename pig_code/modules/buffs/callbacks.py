import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components


async def buffs(inter, _global: bool = False):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    await DisUtils.pagination(inter, lang,
                           embeds={
                               translate(Locales.Buffs.main_page_title, lang): {
                                   'embed': await embeds.generate_basic_buffs_embed(inter, lang,
                                                                                    thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                        config.image_links[
                                                                                            'buffs']))},
                               translate(hryak.locale.Locale.BuffTypes['weight'], lang): {
                                   'embed': await embeds.generate_buffs_multipliers_embed(inter, lang,
                                                                                          buff_type='weight',
                                                                                          thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                              config.image_links[
                                                                                                  'buffs']))},
                               translate(hryak.locale.Locale.BuffTypes['pooping'], lang): {
                                   'embed': await embeds.generate_buffs_multipliers_embed(inter, lang,
                                                                                          buff_type='pooping',
                                                                                          thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                              config.image_links[
                                                                                                  'buffs']))},
                               translate(hryak.locale.Locale.BuffTypes['vomit_chance'], lang): {
                                   'embed': await embeds.generate_buffs_multipliers_embed(inter, lang,
                                                                                          buff_type='vomit_chance',
                                                                                          thumbnail_url=await hryak.Func.get_image_temp_path_from_path_or_link(
                                                                                              config.image_links[
                                                                                                  'buffs']))}
                           },
                           arrows=False,
                           categories=True)
