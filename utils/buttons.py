import discord
from discord.ui import Button

class DocButton(Button):
   def __init__(self):
      super().__init__(
         label = 'Documentation',
         style = discord.Button.url,
         url = 'https://discordpy.readthedocs.io/en/stable/api.html?highlight=discord%20forbidden#discord.Forbidden'
      )