import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_
from utils.buttons import DocButton

class Sclear(commands.Cog):
   def __init__(self, core):
        self.core = core

   @app_commands.command(
      name = 'clear',
      description = 'Clear messages from a channel.',
   )
   @app_commands.describe(
      amount = 'Number of messages to clear.'
   )
   async def clear(self, interaction: discord.Interaction, amount: int):
      if not interaction.user.guild_permissions.manage_messages:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_messages')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if amount is None or amount <= 0:
         no_amount = embed_(interaction, 'Enter a valid amount.', discord.Color.light_gray())
         no_amount.set_footer(text = 'The amount must be greater than 0.')
         await interaction.response.send_message(embed = no_amount, ephemeral = True)
         return

      docs_button = DocButton()
      await interaction.response.defer(ephemeral = True)
      try:
         await interaction.channel.purge(limit = amount)
         clear_ = embed_(interaction, f'{amount} message(s) deleted.', discord.Color.dark_green())
         clear_.set_footer(text = f'Clear by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.followup.send(embed = clear_, ephemeral = True)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-clear: {e}')

async def setup(core):
   await core.add_cog(Sclear(core))

# Solved ECM (26-06-2025)