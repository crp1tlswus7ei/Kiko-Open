import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_
from utils.buttons import DocButton

class Spurge(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'purge',
      description = 'Clear all messages from a specific user.'
   )
   @app_commands.describe(
      user = 'User to purge messages.'
   )
   async def purge(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_messages:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_messages')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't clear your own messages.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      def c_user(msg):
         return msg.author.id == user.id

      docs_button = DocButton()
      await interaction.response.defer(ephemeral = True)
      try:
         await interaction.channel.purge(limit = 7049, check = c_user)
         purge_ = embed_(interaction, f'{user.display_name} messages deleted.', discord.Color.dark_green())
         purge_.set_footer(text = f'Purge by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.followup.send(embed = purge_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f's-purge: {e}')

async def setup(core):
   await core.add_cog(Spurge(core))

# Solved ECM (26-06-2025)