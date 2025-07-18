import discord
from discord import app_commands
from discord.ext import commands
from mdw.CreateRoles import CreateMuteRole, overMute
from utils.embeds import embed_

class Smute(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'mute',
      description = 'Mutes a user indefinitely.'
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def mute(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
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
         ys = embed_(interaction, "You can't mute yourself.", discord.Color.light_gray())
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
            cmrole_ = embed_(interaction, 'Role was not found and was created automatically.', discord.Color.light_gray())
            cmrole_.set_footer(text = 'Check documentation for more info.')
            await interaction.response.send_message(embed = cmrole_, ephemeral = True)

            for channel in interaction.guild.channels:
               await channel.set_permissions(m_role, overwrite = overMute)

         except discord.Forbidden:
            nobot_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
            nobot_perms.set_footer(text = 'Check the error documentation.')
            await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
         except Exception as e:
            print(f's-mute: {e}')

      if m_role in user.roles:
         alrm = embed_(interaction, 'User already muted.', discord.Color.light_gray())
         await interaction.response.send_message(embed = alrm, ephemeral = True)
         return

      await user.add_roles(m_role, reason = reason)
      mute_ = embed_(interaction, f'Mute: {user.display_name}', discord.Color.light_gray())
      mute_.set_footer(text = f'Mute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
      await interaction.response.send_message(embed = mute_, ephemeral = False)

async def setup(core):
   await core.add_cog(Smute(core))

# Solved ECM (26-06-2025)