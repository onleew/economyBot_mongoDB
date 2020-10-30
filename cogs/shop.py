import discord
from discord.ext import commands
import asyncio
import random
from pymongo import MongoClient
from config import settings

class shop(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.clus = MongoClient(settings["mongo_token"])
		self.coll = self.clus.YOUR_MONGODB_DATABASE_NAME.YOUR_MONGODB_COLLECTION_SHOP_NAME
		self.collec = self.clus.YOUR_MONGODB_DATABASE_NAME.YOUR_MONGODB_COLLECTION_CASH_NAME

	@commands.group()
	async def shop(self, ctx):
		pass

	@shop.command()
	@commands.has_permissions(administrator = True)
	async def add(self, ctx, role:discord.Role = None, cost:int = None):
		if not role:
			await ctx.send('[ERROR] - missing argument "role"')
		elif not cost:
			await ctx.send('[ERROR] - missing argument "cost"')
		elif not cost and role:
			await ctx.send('[ERROR] - missing arguments "cost" and "role"')
		else:
			if self.coll.count_documents({"guild_id" : ctx.guild.id, "role_id" : role.id}) == 0:
				post = {
					"guild_id" : ctx.guild.id,
					"role_id" : role.id,
					"cost" : cost
				}

				self.coll.insert_one(post)

				await ctx.send('Good! Role added to shop...')
			else:
				await ctx.send('[ERROR] - indicated role has already in guild shop')

	@shop.command()
	@commands.has_permissions(administrator = True)
	async def remove(self, ctx, role:discord.Role = None):
		if not role:
			await ctx.send('[ERROR] - missing argument "role"')
		else:
			if self.coll.count_documents({"guild_id" : ctx.guild.id, "role_id" : role.id}) == 0:
				await ctx.send("[ERROR] - indicated role hasn't in guild shop")
			else:
				self.coll.delete_one({"guild_id":ctx.guild.id, "role_id":role.id})
				await ctx.send('Good! Role deleted from shop...')

	@shop.command()
	async def place(self, ctx):
		docount = self.coll.count_documents({"guild_id" : ctx.guild.id})
		place = discord.Embed(title = 'Shop place', color = discord.Color.green())

		for role in ctx.guild.roles:
			if self.coll.count_documents({"guild_id" : ctx.guild.id, "role_id" : role.id}) == 0:
				continue
			else:
				place.add_field(name = 'Cost: {}'.format(self.coll.find_one({"guild_id" : ctx.guild.id, "role_id" : role.id})["cost"]), value = '`Role:` {}\n`Role ID:` {}'.format(role.mention, role.id), inline = False)

		await ctx.send(embed = place)

	@shop.command()
	async def buy(self, ctx, role:discord.Role = None):
		if not role:
			await ctx.send('[ERROR] - missing argument "role"')
		elif self.coll.count_documents({"guild_id" : ctx.guild.id, "role_id" : role.id}) == 0:
			await ctx.send("[ERROR] - indicated role hasn't in guild shop")
		else:
			if self.collec.find_one({"guild_id" : ctx.guild.id, "user_id" : ctx.author.id})["cash"] < self.coll.find_one({"guild_id" : ctx.guild.id, "role_id" : role.id})["cost"]:
				await ctx.send("[ERROR] - you don't have any money to buy role")
			else:
				self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : ctx.author.id}, {"$inc" : {"cash" : -self.coll.find_one({"guild_id" : ctx.guild.id, "role_id" : role.id})["cost"]}})
				await ctx.author.add_roles(role)
				await ctx.send("Well, you bought the indicated role")

def setup(client):
	client.add_cog(shop(client))