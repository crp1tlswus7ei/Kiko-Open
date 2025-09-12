import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_
from utils.buttons import DocButton

class Warnings(commands.Cog):
   from mdw.WarnSys import get_warns
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'warnings',
      description = 'List of user warnings.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to review warns.'
   )
   async def warnings(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      docs_button = DocButton()
      user_id = str(user.id)
      try:
         user_warns = self.get_warns(user_id) # false-positive
         if user_warns:
            warnn_ = embed_(interaction, f'{user.display_name} warns:\n' + '\n'.join(user_warns), discord.Color.dark_green())
            warnn_.set_footer(text = f'List requested by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = warnn_, ephemeral = False)
         else:
            no_warnn_ = embed_(interaction, f'{user.display_name} has no warnings.', discord.Color.light_gray())
            no_warnn_.set_footer(text = f'List requested by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = no_warnn_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-warnings: {e}')

async def setup(core):
   await core.add_cog(Warnings(core))

# Solved ECM (26-06-2025)
# 10/09/25