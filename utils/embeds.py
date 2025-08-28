import discord

def embed_(
        interaction: discord.Interaction,
        title: str,
        color: discord.Color) -> discord.Embed:
   embed = discord.Embed(
      title = title,
      color = color
   )
   return embed

def pdesc_(
        interaction: discord.Interaction,
        title: str,
        description: str,
        color: discord.Color) -> discord.Embed:
   embed = discord.Embed(
      title = title,
      description = description,
      color = color
   )
   return embed

def odesc_(
        interaction: discord.Interaction,
        description: str,
        color: discord.Color) -> discord.Embed:
   embed = discord.Embed(
      description = description,
      color = color
   )
   return embed

def noembed_(
        title: str,
        description: str,
        color: discord.Color) -> discord.Embed:
   embed = discord.Embed(
      title = title,
      description = description,
      color = color
   )
   return embed