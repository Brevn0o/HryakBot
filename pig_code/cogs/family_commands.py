from ..core import *
from ..utils import *
from .. import modules


class FamilyCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def family(self, inter):
        pass

    @commands.cooldown(2, 240, commands.BucketType.user)
    @family.sub_command(description=Localized(data=Locales.CreateFamily.description))
    async def create(self, inter,
                     name: str = commands.Param(
                         name=Localized(data=Locales.CreateFamily.name_var_name),
                         description=Localized(data=Locales.CreateFamily.name_var_desc)),
                     description: str = commands.Param(name=Localized(
                                                           data=Locales.CreateFamily.desc_var_name),
                                                       description=Localized(
                                                           data=Locales.CreateFamily.desc_var_desc), default='', max_length=512),
                     image_url: str = commands.Param(name=Localized(
                         data=Locales.CreateFamily.image_url_var_name),
                         description=Localized(
                             data=Locales.CreateFamily.image_url_var_desc), default='', max_length=512),
                     private: str = commands.Param(
                         name=Localized(data=Locales.CreateFamily.private_var_name),
                         description=Localized(data=Locales.CreateFamily.private_var_desc),
                         default='False', choices=Botutils.bool_command_choice()),
                     ask_to_join: str = commands.Param(
                         name=Localized(data=Locales.CreateFamily.ask_to_join_var_name),
                         description=Localized(data=Locales.CreateFamily.ask_to_join_var_desc),
                         default='True', choices=Botutils.bool_command_choice())
                     ):
        await modules.family.callbacks.create_family(inter, name, description, image_url,
                                                     Func.str_to_bool(private),
                                                     Func.str_to_bool(ask_to_join))

    @family.sub_command(description=Localized(data=Locales.ViewFamily.description))
    async def view(self, inter, family_id: str = commands.Param(
                         name=Localized(data=Locales.ViewFamily.family_id_name),
                         description=Localized(data=Locales.ViewFamily.family_id_desc), default=None)):
        await modules.family.callbacks.view_family(inter, family_id)

    @family.sub_command(description=Localized(data=Locales.InviteFamily.description))
    async def invite(self, inter):
        await modules.family.callbacks.invite_family(inter)

    @commands.cooldown(2, 120, commands.BucketType.user)
    @family.sub_command(description=Localized(data=Locales.JoinFamily.description))
    async def join(self, inter, family_id: str = commands.Param(
                         name=Localized(data=Locales.JoinFamily.family_id_name),
                         description=Localized(data=Locales.JoinFamily.family_id_desc))):
        await modules.family.callbacks.join_family(inter, family_id)

    @family.sub_command(description=Localized(data=Locales.LeaveFamily.description))
    async def leave(self, inter):
        await modules.family.callbacks.leave_family(inter)

    @family.sub_command(description=Localized(data=Locales.DeleteFamily.description))
    async def delete(self, inter):
        await modules.family.callbacks.delete_family(inter)

    @family.sub_command(description=Localized(data=Locales.FamilyRequests.description))
    async def requests(self, inter):
        await modules.family.callbacks.family_requests(inter)

def setup(client):
    client.add_cog(FamilyCommands(client))
