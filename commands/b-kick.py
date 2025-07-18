import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_, pdesc_

class Skick(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'kick',
      description = 'Temporary sanction.'
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
      if not interaction.user.guild_permissions.kick_members:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: kick_members')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't kick yourself.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         await user.kick(reason = reason)
         kick_ = pdesc_(interaction, f'Kick: {user.display_name}', f'**id:** {user.id}', discord.Color.dark_green())
         kick_.set_footer(text = f'Kick by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = kick_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e:
         print(f's-kick: {e}')

async def setup(core):
   await core.add_cog(Skick(core))

# Solved ECM (26-06-2025)