import discord
from discord.ext import commands
import asyncio
import random
from pymongo import MongoClient
from config import settings

class econ(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.clus = MongoClient(settings["mongo_token"])
		self.coll = self.clus.YOUR_MONGODB_DATABASE_NAME.YOUR_MONGODB_COLLECTION_NAME

	@commands.command(aliases = ['work'])
	@commands.cooldown(1, 3600, commands.BucketType.member)
	async def __work(self, ctx):
		place = [
			'на заводе',
			'в шахтах',
			'на кассе'
		]

		num = random.randint(1, 4)

		if num == 1:
			newcash = random.randint(100, 200)
		elif num == 2:
			newcash = random.randint(450, 750)
		elif num == 3:
			newcash = random.randint(950, 1200)
		elif num == 4:
			newcash = random.randint(1250, 1750)

		self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : ctx.author.id}, {"$inc" : {"cash" : newcash}})
		await ctx.send(embed = discord.Embed(description = 'Ты молодец, поработал __{}__ и заработал `{}` монет...'.format(random.choice(place), newcash), color = 0xeb7826).set_footer(text = f'Работал: {ctx.author.display_name}', icon_url = ctx.author.avatar_url))


	@commands.command(aliases = ['crime'])
	@commands.cooldown(1, 7200, commands.BucketType.member)
	async def __crime(self, ctx):
		place = [
			'бабушку, которая переходила дорогу',
			'доставщика пиццы',
			'игрушечный банкомат',
			'заброшеный полицейский участок'
		]

		num = random.randint(1, 4)

		if num == 1:
			newcash = random.randint(40, 60)
		elif num == 2:
			newcash = random.randint(70, 120)
		elif num == 3:
			newcash = random.randint(130, 200)
		elif num == 4:
			newcash = random.randint(250, 450)

		self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : ctx.author.id}, {"$inc" : {"cash" : newcash}})
		await ctx.send(embed = discord.Embed(description = 'Ты молодец, ограбил __{}__ и заработал `{}` монет...'.format(random.choice(place), newcash), color = 0xeb7826).set_footer(text = f'Ограбил: {ctx.author.display_name}', icon_url = ctx.author.avatar_url))

	@commands.command(aliases = ['casino'])
	@commands.cooldown(1, 10800, commands.BucketType.member)
	async def cas(self, ctx, amount:int = None):
		if not amount:
			await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите вашу ставку...```\n`[число]` - поставить определённую сумму денег, ставка не может быть меньше 100', color = discord.Color.red()).set_footer(text = f'Связь с разработчиком - {database.find_prefix(ctx.guild.id)}разработчик'), delete_after = 15)
			self.cas.reset_cooldown(ctx)
		else:
			if int(amount) > database.find_cash(ctx.guild.id, ctx.author.id):
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите ставку правильно...```', color = discord.Color.red()).set_footer(text = f'Связь с разработчиком - {database.find_prefix(ctx.guild.id)}разработчик'), delete_after = 15)
				self.cas.reset_cooldown(ctx)
			elif int(amount) < 100:
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите ставку выше чем 100...```', color = discord.Color.red()).set_footer(text = f'Связь с разработчиком - {database.find_prefix(ctx.guild.id)}разработчик'), delete_after = 15)
				self.cas.reset_cooldown(ctx)
			else:
				num = random.randint(1, 2)

				if num == 1:
					self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : ctx.author.id}, {"$inc" : {"cash" : -amount}})
					await ctx.send(embed = discord.Embed(description = f'Печально, ты проиграл {amount} монет, иди работай...', color = discord.Color.red()).set_footer(text = f'Играл: {ctx.author.display_name}', icon_url = ctx.author.avatar_url))
				elif num == 2:
					self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : ctx.author.id}, {"$inc" : {"cash" : amount}})
					await ctx.send(embed = discord.Embed(description = f'Молодец, ты выйграл {amount} монет, можешь взять выходной...', color = discord.Color.green()).set_footer(text = f'Играл: {ctx.author.display_name}', icon_url = ctx.author.avatar_url))

	@commands.group()
	async def cash(self, ctx):
		pass

	@cash.command(aliases = ['add'])
	@commands.has_permissions(administrator = True)
	async def __add_cash(self, ctx, user: discord.Member = None, amount:int = None):
		if not user:
			await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите участника которому хотите добавить монеты...```', color = discord.Color.red()), delete_after = 15)
		else:
			if not amount:
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите число желаемых монет...```', color = discord.Color.red()), delete_after = 15)
			elif amount < 10:
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите число большее 10...```', color = discord.Color.red()), delete_after = 15)
			elif amount > 100000000:
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите число меньше 100000000...```', color = discord.Color.red()), delete_after = 15)
			else:
				try:
					self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : user.id}, {"$inc" : {"cash" : amount}})
					await ctx.send('Вы добавили __{}__ монет участнику `{}`'.format(amount, user.display_name))
				except:
					return

	@cash.command(aliases = ['remove'])
	@commands.has_permissions(administrator = True)
	async def __remove_cash(self, ctx, user: discord.Member = None, amount:int = None):
		if not user:
			await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите участника у которого хотите отнять монеты...```', color = discord.Color.red()), delete_after = 15)
		else:
			if not amount:
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите число удаляемых монет...```', color = discord.Color.red()), delete_after = 15)
			elif amount > database.find_cash(ctx.guild.id, user.id):
				await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'```Укажите число большее 10...```', color = discord.Color.red()), delete_after = 15)
			else:
				try:
					self.coll.update_one({"guild_id" : ctx.guild.id, "user_id" : user.id}, {"$inc" : {"cash" : -amount}})
					await ctx.send('Вы отняли __{}__ монет у участника `{}`'.format(amount, user.display_name))
				except:
					return

	@commands.command(aliases = ['rank', 'bal', 'balance'])
	async def __rank(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author

		if user.colour == discord.Colour.default():
			color = 0x2F3136
		else:
			color = user.colour

		await ctx.send("Баланс __{}__ - `{}` монет".format(user.display_name, self.coll.find_one({"guild_id" : ctx.guild.id, "user_id" : user.id})["cash"]))

def setup(client):
	client.add_cog(econ(client))