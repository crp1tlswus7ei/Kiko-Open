import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_
from utils.buttons import DocButton

class SclearW(commands.Cog):
   from mdw.WarnSys import get_warns, c_warns
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'clear_warns',
      description = 'Clears all warnings from a user.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to clear warns.'
   )
   async def clear_warns(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
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
         no_warns = embed_(interaction, f'{user.display_name} has no warns to clean.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_warns, ephemeral = True)
         return

      docs_button = DocButton()
      try:
         self.c_warns(user_id)
         cw_ = embed_(interaction, f'{user.display_name} warns cleaned.', discord.Color.dark_green())
         cw_.set_footer(text = f'Clean by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = cw_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-clear_warns: {e}')

async def setup(core):
   await core.add_cog(SclearW(core))

# Solved ECM (26-06-2025)