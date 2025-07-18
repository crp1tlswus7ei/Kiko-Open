import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_, pdesc_

class Ssoftban(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'softban',
      description = 'Temporary sanction. Useful for deleting messages from a user.'
   )
   @app_commands.describe(
      user = 'User to be sanctioned',
      reason = 'Reason for sanction.'
   )
   async def softban(self, interaction: discord.Interaction, user: discord.Member, reason: str):
      if not interaction.user.guild_permissions.ban_members:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: ban_members')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't ban yourself.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         await user.ban(reason = reason)
         await asyncio.sleep(1)
         await user.unban()
         softban_ = pdesc_(interaction, f'Soft-ban: {user.display_name}', f'**id:** {user.id}', discord.Color.dark_green())
         softban_.set_footer(text = f'Soft-ban by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = softban_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e:
         print(f's-soft_ban: {e}')

async def setup(core):
   await core.add_cog(Ssoftban(core))

# Solved ECM (26-06-2025)