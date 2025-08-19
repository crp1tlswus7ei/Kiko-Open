import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_
from utils.buttons import DocButton

class Sunwarn(commands.Cog):
   from mdw.WarnSys import get_warns, remove_warn
   def __init__(self, core):
        self.core = core

   @app_commands.command(
      name = 'unwarn',
      description = 'Removes only one warn from a user.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to clean warns.'
   )
   async def unwarn(self, interaction: discord.Interaction, user: discord.Member, amount: int):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if amount is None or amount <= 0:
         no_amount = embed_(interaction, 'Enter a valid amount.', discord.Color.light_gray())
         no_amount.set_footer(text = 'The amount must be greater than 0.')
         await interaction.response.send_message(embed = no_amount, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't remove your own warns.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      user_id = str(user.id)
      warns_ = self.get_warns(user_id)

      if not warns_:
         no_warns = embed_(interaction, f'{user.display_name} has no warns to remove.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_warns, ephemeral = True)
         return

      docs_button = DocButton()
      try:
         if 1 <= amount <= len(warns_):
            self.remove_warn(user_id, amount - 1)
            unwarn_ = embed_(interaction, f'{user.display_name} warn(s) removed.', discord.Color.dark_green())
            unwarn_.set_footer(text = f'Warns: {len(warns_) - 1}')
            await interaction.response.send_message(embed = unwarn_, ephemeral = False)
         else:
            uw_e = embed_(interaction, 'Invalid warn.', discord.Color.light_gray())
            uw_e.set_footer(text = 'Enter a valid number.')
            await interaction.response.send_message(embed = uw_e, ephemeral = True)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-unwarn: {e}')

async def setup(core):
   await core.add_cog(Sunwarn(core))

# Solved ECM (26-06-2025)