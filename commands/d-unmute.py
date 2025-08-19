import discord
from discord import app_commands
from discord.ext import commands
from mdw.CreateRoles import CreateMuteRole, CreateHardMuteRole, hm_overMute, m_overMute
from utils.embeds import embed_, pdesc_
from utils.buttons import DocButton

class Sunmute(commands.Cog):
   def __init__(self, core):
        self.core = core

   @app_commands.command(
      name = 'unmute',
      description = 'Remove mute from a user',
      nsfw = False
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
      hm_role = discord.utils.get(interaction.guild.roles, name = 'Hard Mute')
      if not m_role:
         try:
            await CreateMuteRole(interaction)
            m_role = discord.utils.get(interaction.guild.roles, name = 'Mute')
            m_rolec = embed_(interaction, 'Mute role not found and was automatically created.', discord.Color.light_gray())
            m_rolec.set_footer(text = 'Check documentation for more information.')
            await interaction.response.send_message(embed = m_rolec, ephemeral = True)

            for channel in interaction.guild.channels:
               try:
                  await channel.set_permissions(m_role, overwrite = m_overMute)
               except discord.Forbidden:
                  noch_perms = embed_(interaction, 'Error modifying channel permissions.', discord.Color.dark_red())
                  noch_perms.set_footer(text = 'Check error documentation for more information.')
                  await interaction.response.send_message(embed = noch_perms, ephemeral = True)
               except Exception as e:
                  print(f'd-unmute: [channel.set_permissions]; ({e})')
                  return

         except discord.Forbidden:
            role_exc = embed_(interaction, 'Error creating or applying role.', discord.Color.dark_red())
            role_exc.set_footer(text = 'Check error documentation for more information.')
            await interaction.response.send_message(embed = role_exc, ephemeral = True)
         except Exception as e:
            print(f'd-unmute: [CreateMuteRole]; ({e})')
         return

      if not hm_role:
         try:
            await CreateHardMuteRole(interaction)
            hm_role = discord.utils.get(interaction.guild.roles, name = 'Hard Mute')
            hm_rolec = embed_(interaction, 'Hard Mute role not found and was automatically created.', discord.Color.light_gray())
            hm_rolec.set_footer(text = 'Check documentation for more information.')
            await interaction.response.send_message(embed = hm_rolec, ephemeral = True)

            for channel in interaction.guild.channels:
               try:
                  await channel.set_permissions(hm_role, overwrite = hm_overMute)
               except discord.Forbidden:
                  noch_perms = embed_(interaction, 'Error modifying channel permissions.', discord.Color.dark_red())
                  noch_perms.set_footer(text = 'Check error documentation for more information.')
                  await interaction.response.send_message(embed = noch_perms, ephemeral = True)
               except Exception as e:
                  print(f'd-unmute: [channel.set_permissions]; ({e})')
               return

         except discord.Forbidden:
            role_exc = embed_(interaction, 'Error creating or applying role.', discord.Color.dark_red())
            role_exc.set_footer(text = 'CHeck error documentation for more information.')
            await interaction.response.send_message(embed = role_exc, ephemeral = True)
         except Exception as e:
            print(f'd-unmute: [CreateHardMuteRole]; ({e})')
         return

      docs_button = DocButton()
      try:
         if m_role in user.roles:
            await user.remove_roles(m_role, reason = reason)
            m_unmute_ = embed_(interaction, f'Unmute: {user.display_name}', discord.Color.dark_green())
            m_unmute_.set_footer(text = f'Unmute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = m_unmute_, ephemeral = False)
         else:
            if hm_role in user.roles:
               await user.remove_roles(hm_role, reason = reason)
               hm_unmute = embed_(interaction, f'Unmute: {user.display_name}', discord.Color.dark_green())
               hm_unmute.set_footer(text = f'Unmute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
               await interaction.response.send_message(embed = hm_unmute, ephemeral = False)
            else:
               no_mute = embed_(interaction, f'{user.display_name} is not muted.', discord.Color.light_gray())
               await interaction.response.send_message(embed = no_mute, ephemeral = True)
               return

      except discord.Forbidden:
         no_perms = embed_(interaction, 'Error removing roles.', discord.Color.dark_red())
         no_perms.set_footer(text = 'Check error documentation for more information.')
         await interaction.response.send_message(embed = no_perms, ephemeral = True, view = docs_button)
      except Exception as e:
         print(f'd-unmute: [user.remove_roles]; ({e})')

async def setup(core):
   await core.add_cog(Sunmute(core))