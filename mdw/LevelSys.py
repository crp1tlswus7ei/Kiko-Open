import time
import asyncio
import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

class LevelSys(commands.Cog):
   def __init__(self, core: commands.Bot, mongo_uri: str):
      self.core = core
      self.client = AsyncIOMotorClient(mongo_uri)
      self.db = self.client['kiko']
      self.w_coll = self.db['levels']
      self.cooldowns = {}

   async def add_xp(self, user_id: int, guild_id: int, xp: int):
      query = {'user_id': user_id, 'guild_id': guild_id}
      user = await self.w_col.find_one(query)

      if not user:
         user = {'user_id': user_id, 'guild_id': guild_id, 'xp': 0, 'level': 1}
         await self.w_coll.insert_one(user)

      new_xp = user['xp'] + xp
      new_lvl = user['level']

      if new_xp >= new_lvl * 100:
         new_xp = 0
         new_lvl += 1
         print(f'LevelSys: Active')

      await self.w_coll.update_one(query, {'$set': {'xp': new_xp, 'level': new_lvl}})

   async def get_level(self, user_id: int, guild_id: int):
      user = await self.w_col.find_one({'user_id': user_id, 'guild_id': guild_id})
      if not user:
         return {'level': 1, 'xp': 0}
      return user

   @commands.Cog.listener()
   async def on_message(self, message: discord.Message):
      if message.author.bot:
         return

      now = time.time()
      cooldown = 0
      last_use = self.cooldowns.get(message.author.id, 0)

      if now - last_use >= cooldown:
         self.cooldowns[message.author.id] = now
         await self.add_xp(message.author.id, message.guild.id, xp = 10)

async def setup(core):
   await core.add_cog(LevelSys(core, mongo_uri))