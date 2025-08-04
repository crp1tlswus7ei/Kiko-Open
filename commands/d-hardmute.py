import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from mdw.CreateRoles import CreateHardMuteRole, hm_overMute
from utils.embeds import embed_

class Shardmute(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'hardmute',
      description = 'Remove all roles from user and applies mute.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def hardmute(self, interaction: discord.Interaction, user: discord.Member, reason: str):
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
      hm_role = discord.utils.get(interaction.guild.roles, name = 'Hard Mute')

      if m_role in user.roles:
         alr = embed_(interaction, f'{user.display_name} already muted.', discord.Color.light_gray())
         await interaction.response.send_message(embed = alr, ephemeral = True)
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
                  await channel.set_permissions(target = hm_role, overwrite = hm_overMute)
               except discord.Forbidden:
                  noch_perms = embed_(interaction, 'Error modifying channel permissions.', discord.Color.dark_red())
                  noch_perms.set_footer(text = 'Check error documentation for more information.')
                  await interaction.response.send_message(embed = noch_perms, ephemeral = True)
               except Exception as e:
                  print(f'd-hardmute: [channel.set_permissions]; ({e})')
                  return

         except discord.Forbidden:
            role_exc = embed_(interaction, 'Error creating or applying role.', discord.Color.dark_red())
            role_exc.set_footer(text = 'Check error documentation for more information.')
            await interaction.response.send_message(embed = role_exc, ephemeral = True)
         except Exception as e:
            print(f'd-hardmute: [CreateHardMuteRole]; ({e})')
         return

      rm_ = [r for r in user.roles if r != interaction.guild.default_role]
      try:
         if hm_role not in user.roles:
            await user.remove_roles(*rm_, reason = 'Hard Mute')
            await user.add_roles(hm_role, reason = reason)
            hm_mute_ = embed_(interaction, f'{hm_role.name}: {user.display_name}', discord.Color.dark_green())
            hm_mute_.set_footer(text = f'Hard Mute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = hm_mute_, ephemeral = False)
         else:
            alr = embed_(interaction, f'{user.display_name} already muted.', discord.Color.light_gray())
            await interaction.response.send_message(embed = alr, ephemeral = True)
            return

      except discord.Forbidden:
         no_perms = embed_(interaction, 'Error executing command.', discord.Color.dark_red())
         no_perms.set_footer(text = 'Check error documentation for more information.')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
      except Exception as e:
         print(f'd-hardmute: [user.add_roles]; ({e})')

async def setup(core):
   await core.add_cog(Shardmute(core))