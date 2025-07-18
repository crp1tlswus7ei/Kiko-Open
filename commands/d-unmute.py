import discord
from discord import app_commands
from discord.ext import commands
from mdw.CreateRoles import CreateMuteRole
from utils.embeds import embed_, pdesc_

class Sunmute(commands.Cog):
   def __init__(self, core):
        self.core = core

   @app_commands.command(
      name = 'unmute',
      description = 'Remove mute from a user'
   )
   @app_commands.describe(
      user = 'User to remove mute.',
      reason = 'Reason for remove mute.'
   )
   async def unmute(self, interaction: discord.Interaction, user: discord.Member, reason: str):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_(interaction, 'You must mention a user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.id == user.id:
         ys = embed_(interaction, "You can't unmute yourself.", discord.Color.light_gray())
         await interaction.response.send_message(embed = ys, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      m_role = discord.utils.get(interaction.guild.roles, name = 'Mute')
      if not m_role:
         try:
            await CreateMuteRole(interaction)
            create_role_ = embed_(interaction, 'Role not found and was automatically created.', discord.Color.dark_grey())
            create_role_.set_footer(text = 'Check the documentation for more details.')
            await interaction.response.send_message(embed = create_role_, ephemeral = True)

            for channel in interaction.guild.channels:
               await channel.set_permissions(m_role)

         except discord.Forbidden:
            nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
            nobot_perms.set_footer(text = 'Check the error documentation.')
            await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
            return
         except Exception as e:
            print(f's-unmute: {e}')

      if m_role not in user.roles:
         no_mute = embed_(interaction, f'{user.display_name} is not muted.', discord.Color.light_gray())
         await interaction.response.send_message(embed = no_mute, ephemeral = True)
         return

      await user.remove_roles(m_role, reason = reason)
      unmute_ = pdesc_(interaction, f'Unmute: {user.display_name}', f'**id:** {user.id}', discord.Color.dark_green())
      unmute_.set_footer(text = f'Unmute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
      await interaction.response.send_message(embed = unmute_, ephemeral = False)

async def setup(core):
   await core.add_cog(Sunmute(core))

# Solved ECM (26-06-2025)