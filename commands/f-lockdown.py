import discord
from discord import app_commands
from discord.ext import commands
from mdw.CreateRoles import f_overLockdown
from utils.embeds import embed_
from utils.buttons import DocButton

class Slockdown(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'lockdown',
      description = 'Lock channel',
      nsfw = False
   )
   @app_commands.describe(
      channel = 'Default channel: actual'
   )
   async def lockdown(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
      if not interaction.user.guild_permissions.administrator:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: `administrator`')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      docs_button = DocButton()
      channel = channel or interaction.channel
      try:
         await channel.set_permissions(interaction.guild.default_role, overwrite = f_overLockdown)
         lockdown_ = embed_(interaction, f'Lockdown: {channel.mention}', discord.Color.light_gray())
         lockdown_.set_footer(text = f'Lockdown by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = lockdown_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f'f-lockdown: {e}')

async def setup(core):
   await core.add_cog(Slockdown(core))
