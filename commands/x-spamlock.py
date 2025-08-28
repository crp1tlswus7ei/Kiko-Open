import time
import discord
from datetime import timedelta
from typing import Literal
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_, noembed_

class SpamSystem(commands.Cog):
   def __init__(self, core):
      self.core = core
      self.spamlock_on = {}
      self.spamlock_off = {}
      self.last_messages = {}

   @app_commands.command(
      name = 'spam_lock',
      description = 'Enable or disable automatic spam detection',
      nsfw = False
   )
   @app_commands.describe(
      status = 'enable/disable'
   )
   async def spam_lock(self, interaction: discord.Interaction, status: Literal['Enabled', 'Disabled']):
      if interaction.user.guild_permissions.administrator:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permissions required: `administrator`')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      docs_button = DocButton()
      guild_id = interaction.guild_id
      try:
         if status.lower() == 'Enable':
            self.spamlock_on[guild_id] = True
            spamlock_ = embed_(interaction, 'Spamlock: Enable', discord.Color.orange())
            spamlock_.set_footer(text = f'Enable by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = spamlock_, ephemeral = False)
         else:
            if status.lower() == 'Disable':
               self.spamlock_off[guild_id] = False
               no_spamlock = embed_(interaction, 'Spamlock: Disable', discord.Color.orange())
               no_spamlock.set_footer(text = f'Disable by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
               await interaction.response.send_message(embed = no_spamlock, ephemeral = False)

      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f'x-spamlock: {e}')

async def setup(core):
   await core.add_cog(SpamSystem(core))