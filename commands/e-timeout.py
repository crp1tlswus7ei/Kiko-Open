import discord
from datetime import timedelta
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_, pdesc_

class Stimeout(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'timeout',
      description = 'Mutes a user for certain period of time.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      duration = 'Minutes of sanction.',
      reason = 'Reason for sanction.'
   )
   async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: int, *, reason: str = None):
      if not interaction.user.guild_permissions.mute_members:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: mute_members')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if duration is None or duration <= 0:
         no_dr = embed_(interaction, 'Enter a valid duration in minutes.', discord.Color.light_gray())
         no_dr.set_footer(text = 'Duration must be greater than 0.')
         await interaction.response.send_message(embed = no_dr, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't mute yourself.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         await user.timeout(timedelta(minutes = duration), reason = reason)
         timeout_ = pdesc_(interaction, f'Timeout: {user.display_name}', f'**Duration:** {duration} minutes.', discord.Color.dark_green())
         timeout_.set_footer(text = f'Timeout by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = timeout_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
      except Exception as e:
         print(f's-timeout: {e}')

async def setup(core):
   await core.add_cog(Stimeout(core))

# Solved ECM (26-06-2025)