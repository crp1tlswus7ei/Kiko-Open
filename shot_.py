import os
import discord
import asyncio
from discord import PartialEmoji
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
# from mdw.SpamSys import SpamSystem

load_dotenv()
class Shot:
   def __init__(self):
      self.token = os.getenv('CORE_TOKEN')
      self.mongo_uri = os.getenv('MONGO_URI')
      self.ints = discord.Intents.all() # 2253890690350838
      self.core = commands.Bot(
         command_prefix = '!!',
         intents = self.ints,
         help_command = None
      )

      @self.core.event
      async def on_ready():
         print(f'Core: Online... as {self.core.user}')
         await self.core.change_presence(
            activity = discord.CustomActivity(
               name = 'In maintenance'
            ),
            status = discord.Status('dnd')
         )
         try:
            sync_cmds = await self.core.tree.sync()
            print(f'Shot: Sync; {len(sync_cmds)} commands.')
         except Exception as e:
            print(f'Shot: (on_ready); {e}')

   async def load_(self):
      for filename in os.listdir('./commands'):
         if filename.endswith('.py'):
            await self.core.load_extension(f'commands.{filename[:-3]}')

   async def connect_(self):
      shot = MongoClient(self.mongo_uri)
      try:
         shot.admin.command('ping')
         print(f'Shot: Database Online.')
      except Exception as e:
         print(f'Shot: (connect_); {e}')

   async def shot_(self):
      async with self.core:
         await self.connect_()
         await self.load_()
         # self.core.add_listener(SpamSystem.on_message)
         await self.core.start(self.token)

asyncio.run(Shot().shot_())