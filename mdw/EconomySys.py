import os
import random
import discord
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI')
shot = MongoClient(MONGO_URI)
db = shot["kiko"]
b_coll = db["levels"]

def open_acc(self, user_id):
   if not self.b.coll.find_one({"_id": user_id}):
      self.b.coll.insert_one({"_id": user_id, wallet: 0, bank: 0})

def get_bal(self, user_id):
   self.open_acc(user_id)
   usr = self.b.coll.find_one({"_id": user_id})
   return user["wallet"], user["bank"]

def deposit(self, user_id, amount):
   self.open_acc(user_id)
   usr = self.b.coll.find_one({"_id": user_id})
   if user["wallet"] >= amount:
      self.b_coll.update_one({"_id": user_id}, {"$inc": {"wallet": -amount, "bank": amount}})
      return True
   return False

def withdraw(self, user_id, amount):
   self.open_acc(user_id)
   usr = self.b.coll.find_one({"_id": user_id})
   if user["bank"] >= amount:
      self.b_coll.update_one({"_id": user_id}, {"%inc" : {"wallet": amount, "bank": -amount}})
      return True
   return False

def work(self, user_id):
   self.open_acc(user_id)
   earn = random.randint(50, 200)
   self.b_coll.update_one({"_id": user_id}, {"$inc": {"wallet": earn}})
   return earn