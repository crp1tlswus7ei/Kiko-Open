import discord
from discord import app_commands
from discord.ext import commands
from mdw.CreateRoles import f_overUnlock
from utils.embeds import embed_
from utils.buttons import DocButton

class Sunlock(commands.Cog):
   def __inni__(self, core):
      self.core = core

   @app_commands.command(
      name = 'unlockdown',
      description = 'Unlock channel',
      nsfw = False
   )
   @app_commands.describe(
      channel = 'Default channel: actual'
   )
   async def unlockdown(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
      if not interaction.user.guild_permissions.administrator:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: `administrator`')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      docs_button = DocButton()
      channel = channel or interaction.channel
      try:
         await channel.set_permissions(interaction.guild.default_role, overwrite = f_overUnlock)
         unlock_ = embed_(interaction, f'Unlock: {channel.mention}', discord.Color.light_gray())
         unlock_.set_footer(text = f'Unlock by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = unlock_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.light_gray())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f'f-unlockdown: {e}')

async def setup(core):
   await core.add_cog(Sunlock(core))