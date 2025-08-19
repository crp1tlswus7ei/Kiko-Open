import os
import random
import asyncio
import discord
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
ints = discord.Intents.all() # Change later
core = commands.Bot(command_prefix = '', intents = ints, help_command = None)
token = os.getenv('CORE_TOKEN')

async def connect_():
   mongo_uri = os.getenv('MONGO_URI')
   shot = MongoClient(mongo_uri)
   try:
      await shot.admin.command('ping')
      print('db connect.')
   except Exception as e:
      print(f'DB error: {e}')

async def load_():
   for filename in os.listdir('commands'):
      if filename.endswith('.py'):
         await core.load_extension(f'commands.{filename[:-3]}')

@core.event
async def on_ready():
   print('Status: Online')
   try:
      sync_cmds = await core.tree.sync()
      print(f'Synced commands: {len(sync_cmds)} commands.')
   except Exception as e:
      print(f'Sync error: {e}')

async def shot_():
   async with core:
      await load_()
      await core.start(token)

asyncio.run(shot_())