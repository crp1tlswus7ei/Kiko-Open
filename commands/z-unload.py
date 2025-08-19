import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_

load_dotenv()
PASS = str(os.getenv("CORE_AUTH"))

class Unload(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'unload',
      description = 'Unload an extension.',
      nsfw = False
   )
   @app_commands.describe(
      extension = 'Extension name to unload.',
      password = 'auth'
   )
   async def unload(self, interaction: discord.Interaction, extension: str, password: str):
      if password == PASS:
         pass
      else:
         no_auth = embed_(interaction, 'Authorization required: 401', discord.Color.dark_red())
         await interaction.response.send_message(embed = no_auth, ephemeral = True)
         print(f'z-unload: Authorization failed by: {interaction.user.id} in {interaction.guild_id}: {interaction.guild.name}')
         return

      try:
         await self.core.unload_extension(f'commands.{extension}')
         unload_ = embed_(interaction, f'Unload: `{extension}`', discord.Color.light_gray())
         await interaction.response.send_message(embed = unload_, ephemeral = True)
         print(f'z-unload: New unload by: {interaction.user.id}: {interaction.user.name} aka: {interaction.user.display_name}')
      except command.ExtensionNotLoaded:
         n_loaded = embed_(interaction, f'Not loaded: `{extension}`', discord.Color.orange())
         await interaction.response.send_message(embed = n_loaded, ephemeral = True)
      except commands.ExtensionNotFound:
         n_found = embed_(interaction, f'Not found: `{extension}`', discord.Color.dark_red())
         n_found.set_footer(text = 'Extension not exist.')
         await interaction.response.send_message(embed = n_found, ephemeral = True)
      except Exception as e:
         print(f'z-unload: {e}')

async def setup(core):
   await core.add_cog(Unload(core))