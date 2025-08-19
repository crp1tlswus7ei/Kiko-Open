import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_

load_dotenv()
PASS = str(os.getenv('CORE_AUTH'))

class Reload(commands.Cog):
    def __init__(self, core):
       self.core = core

    @app_commands.command(
       name = "reload",
       description = "Reload an extension.",
       nsfw = False
    )
    @app_commands.describe(
       extension = 'Extension name to reload.',
       password = 'auth'
    )
    async def reload(self, interaction: discord.Interaction, extension: str, password: str):
        if password == PASS:
           pass
        else:
           no_auth = embed_(interaction, 'Authorization required: 401', discord.Color.dark_red())
           await interaction.response.send_message(embed = no_auth, ephemeral = True)
           print(f'z-reload: Authorization failed by: {interaction.user.id} in {interaction.guild_id}: {interaction.guild.name}')
           return

        try:
           await self.core.reload_extension(f"commands.{extension}")
           reload_ = embed_(interaction, f"Reload: `{extension}`", discord.Color.light_gray())
           await interaction.response.send_message(embed = reload_, ephemeral = True)
           print(f'z-reload: New reload by: {interaction.user.id}: {interaction.user.name} aka: {interaction.user.display_name}')
        except commands.ExtensionNotLoaded:
           n_reload = embed_(interaction, f"Not loaded: `{extension}`", discord.Color.orange())
           n_reload.set_footer(text = f'Extension not synced.')
           await interaction.response.send_message(embed = n_reload, ephemeral = True)
        except commands.ExtensionNotFound:
           n_found = embed_(interaction, f"Not found: `{extension}`", discord.Color.dark_red())
           n_found.set_footer(text = f'Extension not exist.')
           await interaction.response.send_message(embed = n_found, ephemeral = True)
        except Exception as e:
           print(f'z-reload: {e}')

async def setup(core):
    await core.add_cog(Reload(core))

# Solved ECM (12-08-2025)