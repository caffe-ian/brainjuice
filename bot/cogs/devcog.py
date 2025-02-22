import os
from discord.ext import commands
from importlib import reload
import functions, interaction
import asyncio
asyncio = asyncio
import discord
import copy

class DevCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True, description="Reload cogs", usage=".rcog [cog]", aliases=['rcogs'])
	async def rcog(self, ctx, cog = None):
		if not ctx.author.id == 615037304616255491:
			return
		if cog is None:
			await ctx.send("Reloading cogs")
			for extension in self.bot.extension:
				try:
					self.bot.reload_extension(extension)
				except:
					raise
			await ctx.send("Reloaded all cogs")
		else:
			await ctx.send(f"Reloading `{cog.lower()}` cog")
			if not os.path.isfile(f"cogs/{cog.lower()}.py"):
				await ctx.send(f"Could not find this cog `{cog}`")
				return
			try:
				self.bot.reload_extension(f"cogs.{cog.lower()}")
			except:
				raise
			await ctx.send(f"Reloaded `{cog.lower()}` cog")

	@commands.command(hidden=True, description="Reload modules", usage=".rmod [module]", aliases=['rmods'])
	async def rmod(self, ctx, module = None):
		if not ctx.author.id == 615037304616255491:
			return
		if module is None:
			await ctx.send("Reloading all modules")
			for mod in [functions, interaction]:
				try:
					reload(mod)
				except:
					raise
			await ctx.send("Reloaded all modules")
		else:
			await ctx.send(f"Reloading {module.lower()} module")
			if module.lower() not in ["lists", "functions", "interclass", "codes", "slash"]:
				await ctx.send(f"Cannot find this module `{module}`")
			dictionary = {"functions": functions, "interaction": interaction}
			try:
				reload(dictionary[module.lower()])
			except:
				raise
			await ctx.send(f"Reloaded {module.lower()} module")

	@commands.command(hidden=True, description="Execute code", usage="ov execute <code>")
	async def execute(self, ctx, *, code: str = None):
		if not ctx.author.id == 615037304616255491:
			return
		if code is None:
			await ctx.send("Cannot execute nothing!")
			return
		if "```" not in code or code.count("`") < 6:
			await ctx.send("Code must be wrapped in triple backticks!")
			return
		code = ''.join(code.split('```')).strip().replace("self.bot.http.token", "'Nice try'")
		exec(f"""
async def _ex(ctx):
	try:
		{code}
		await ctx.message.add_reaction("\U00002705")
	except Exception as e:
		await ctx.message.add_reaction("\U0000274c")
		await ctx.send("`[*] Error: " + str(e) + "`")

asyncio.ensure_future(_ex(ctx))
		""", locals(), globals())

	@execute.error
	async def executeerror(self, ctx, error):
		await ctx.message.add_reaction("\U0000274c")
		await ctx.send("`[*] Error: " + str(error.original) + "`")

	@commands.command(hidden=True, description="Sudo a user do invoke a command", usage="ov sudo <user> <command> [args]")
	async def sudo(self, ctx, user: discord.User = None, *, command: str):
		if not ctx.author.id == 615037304616255491:
			await ctx.send("Only the Chosen can use this command")
			return
		if user is None:
			await ctx.reply("Who is your sudo target?")
			return
		if user == ctx.author:
			await ctx.reply("You can't sudo yourself")
			return
		if command is None:
			await ctx.reply("Provide a command")
			return
		msg = copy.copy(ctx.message)
		msg.channel = ctx.channel
		msg.author = user
		msg.content = ctx.prefix + command
		new_ctx = await self.bot.get_context(msg, cls=type(ctx))
		await self.bot.invoke(new_ctx)

	@commands.command(hidden=True, description="Ban a user and Discord blacklist and wallet blacklist a user, if available", usage=".ban <user> [reason]")
	async def ban(self, ctx, user: discord.Member = None, reason: str = "No reason"):
		if not ctx.author.id == 615037304616255491:
			return
		if user is None:
			await ctx.reply("Who do you want to ban?")
			return
		await user.ban(delete_message_days=0, reason=reason)
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(user.id)]
		if address != []:
			await functions.ccll.update_one({"id": "blacklist"}, {"$addToSet": {"data": {"$each": [str(ctx.author.id), address]}}})
		else:
			await functions.ccll.update_one({"id": "blacklist"}, {"$addToSet": {"data": str(ctx.author.id)}})
		await ctx.reply(f"Successfully banned and blacklisted {user}")

	@commands.command(hidden=True, description="Unban a user and Discord unblacklist and wallet unblacklist a user, if available", usage=".unban <user> [reason]")
	async def unban(self, ctx, user: discord.User = None, reason: str = "No reason"):
		if not ctx.author.id == 615037304616255491:
			return
		if user is None:
			await ctx.reply("Who do you want to unban?")
			return
		await user.unban(reason=reason)
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(user.id)]
		if address != []:
			if address in (await functions.ccllfinddoc("blacklist")).data:
				await functions.ccll.update_one({"id": "blacklist"}, {"$pull": {"data": {"$each": [str(ctx.author.id), address]}}})
			else:
				await functions.ccll.update_one({"id": "blacklist"}, {"$pull": {"data": str(ctx.author.id)}})
		else:
			await functions.ccll.update_one({"id": "blacklist"}, {"$pull": {"data": str(ctx.author.id)}})

		await ctx.reply(f"Successfully unbanned and unblacklisted {user}")

	@commands.command(hidden=True, description="Blacklist a user Discord ID or wallet address", usage=".blacklist <Discord ID or wallet address>")
	async def blacklist(self, ctx, id_or_address = None):
		if not ctx.author.id == 615037304616255491:
			return
		if id_or_address is None:
			await ctx.reply("Provide a Discord ID or wallet address to blacklist!")
			return
		await functions.ccll.update_one({"id": "blacklist"}, {"$addToSet": {"data": id_or_address}})
		await ctx.reply(f"Successfully blacklisted **{id_or_address}**")

	@commands.command(hidden=True, description="Unblacklist a user Discord ID or wallet address", usage=".unblacklist <Discord ID or wallet address>")
	async def unblacklist(self, ctx, id_or_address = None):
		if not ctx.author.id == 615037304616255491:
			return
		if id_or_address is None:
			await ctx.reply("Provide a Discord ID or wallet address to blacklist!")
			return
		await functions.ccll.update_one({"id": "blacklist"}, {"$pull": {"data": id_or_address}})
		await ctx.reply(f"Successfully blacklisted **{id_or_address}**")

	@commands.command(hidden=True, description="Prune members joined between a specific period of time", usage=".prune <from> <to>")
	async def prune(self, ctx, fr, to):
		if not ctx.author.id == 615037304616255491:
			return

def setup(bot):
	bot.add_cog(DevCog(bot))