import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_
from utils.buttons import DocButton

class Suntimeout(commands.Cog):
   def __init(self, core):
      self.core = core

   @app_commands.command(
      name = 'untimeout',
      description = 'Remove mute from timeout command.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to remove sanction.'
   )
   async def untimeout(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.mute_members:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: mute_members')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't remove your own mute.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      docs_button = DocButton()
      try:
         await user.timeout(None) # !
         untimeout_ = embed_(interaction, f'Untimeout: {user.display_name}', discord.Color.dark_green())
         untimeout_.set_footer(text = f'Untimeout by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = untimeout_, ephemeral = False)
      except discord.errors.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-untimeout: {e}')

async def setup(core):
   await core.add_cog(Suntimeout(core))

# Solved ECM (30-06-2025)