import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_

load_dotenv()
PASS = str(os.getenv('CORE_AUTH'))

class Load(commands.Cog):
   def __init__(self, core):
      self.core = core

   @app_commands.command(
      name = 'load',
      description = 'Load new Bot extension.',
      nsfw = False
   )
   @app_commands.describe(
      extension = 'Extension name to load.',
      password = 'auth'
   )
   async def load(self, interaction: discord.Interaction, extension: str, password: str):
      if password == PASS:
         pass
      else:
         no_auth = embed_(interaction, 'Autorization required: 401', discord.Color.dark_red())
         await interaction.response.send_message(embed = no_auth, ephemeral = True)
         print(f'z-load: Authorization failed by: {interaction.user.id} in {interaction.guild_id}: {interaction.guild.name}')
         return

      try:
         await self.core.load_extension(f'commands.`{extension}`')
         load_ = embed_(interaction, f'Load: `{extension}`', discord.Color.light_gray())
         await interaction.response.send_message(embed = load_, ephemeral = True)
         print(f'z-load: New load by: {interaction.user.id}: {interaction.user.name} aka: {interaction.user.display_name}')
      except commands.ExtensionAlreadyLoaded:
         alr_load = embed_(interaction, f'Already loaded: `{extension}`', discord.Color.orange())
         await interaction.response.send_message(embed = alr_load, ephemeral = True)
      except commands.ExtensionNotFound:
         n_found = embed_(interaction, f'Not found: `{extension}`', discord.Color.dark_red())
         n_found.set_footer(text = 'Extension not exist.')
         await interaction.response.send_message(embed = n_found, ephemeral = True)
      except Exception as e:
         print(f'z-load: {e}')

async def setup(core):
   await core.add_cog(Load(core))