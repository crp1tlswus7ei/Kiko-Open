import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_

class Sunban(commands.Cog):
   def __init__(self, core):
        self.core = core

   @app_commands.command(
      name = 'unban',
      description = 'Remove ban of a user.'
   )
   @app_commands.describe(
      user_id = 'ID of the user to remove ban.'
   )
   async def unban(self, interaction: discord.Interaction, user_id: int):
      if not interaction.user.guild_permissions.ban_members:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: ban_members')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user_id is None:
         no_user = embed_(interaction, 'The ID cannot be empty.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user_id:
         ys = embed_(interaction, "You can't unban yourself.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      try:
         user_id = int(user_id)
      except ValueError:
         w_e = embed_(interaction, 'Invalid ID.', discord.Color.light_gray())
         await interaction.response.send_message(embed = w_e, ephemeral = True)
      except discord.Forbidden:
         nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e:
         print(f's-unban: {e}')

      banned_users = interaction.guild.bans()
      async for ban_entry in banned_users:
         user = ban_entry.user
         if user.id == user_id:
            await interaction.guild.unban(user)
            unban_ = embed_(interaction, f'Unban: {user_id}', discord.Color.dark_green())
            unban_.set_footer(text = f'Unban by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = unban_, ephemeral = False)
            return

      no_user = embed_(interaction, 'This ID does no exist.', discord.Color.light_gray())
      no_user.set_footer(text = 'Make sure the ID is correct')
      await interaction.response.send_message(embed = no_user, ephemeral = True)
      return

async def setup(core):
   await core.add_cog(Sunban(core))

# Solved (26-06-2025)