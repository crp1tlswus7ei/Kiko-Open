import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_, pdesc_
from utils.buttons import DocButton

class Warn(commands.Cog):
   from mdw.WarnSys import get_warns, add_warns
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'warn',
      description = 'Warn a user about behavior.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def warn(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_roles.')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't warn yourself.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      user_id = str(user.id)
      docs_button = DocButton()
      try:
         total_warns = self.add_warns(user_id, reason = reason)
         warn_ = pdesc_(interaction, f'{user.display_name} has been warned.', f'**Warns:** {total_warns}', discord.Color.dark_green())
         warn_.set_footer(text = f'Warn by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = warn_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-warn: {e}')

async def setup(core):
   await core.add_cog(Warn(core))

# Solved ECM (26-06-2025)
# 10/09/25