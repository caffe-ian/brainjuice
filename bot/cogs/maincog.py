import os
import discord
from discord.ext import commands
import interaction
import functions
import time
import json

color = discord.Colour

class MainCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Shows a list of command and usage", usage='.help [command_name]')
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def help(self, ctx, *, command = None):
		if command is None:
			view = interaction.Help_select(ctx, ctx.author)
			helpembed = discord.Embed(title="Help command", description="Choose a command category", color=color.blue())
			view.message = hembed = await ctx.reply(embed=helpembed, view=view)

			while True:
				await view.wait()
				if view.value is None:
					return
				command = view.value
				if command == 'main':
					view = interaction.Help_select(ctx, ctx.author)
					helpembed = discord.Embed(title="Main commands", description="`.help <command>` for more information of a specific command", color = color.blue())
					helpembed.add_field(name = 'Main important commands', value = f"`{'`, `'.join(sorted([command.name for command in self.bot.get_cog('MainCog').walk_commands() if command.hidden is False]))}`", inline=True)
					helpembed.set_footer(text="Type '.help <command name>' to read the details!")
					view.message = await hembed.edit(embed=helpembed, view=view)
				elif command == 'fun':
					view = interaction.Help_select(ctx, ctx.author)
					helpembed = discord.Embed(title="Fun commands", description="`.help <command>` for more information of a specific command", color = color.blue())
					helpembed.add_field(name = 'Fun commands when you are bored', value = f"`{'`, `'.join(sorted([command.name for command in self.bot.get_cog('FunCog').walk_commands() if command.hidden is False]))}`", inline=True)
					helpembed.set_footer(text="Type '.help <command name>' to read the details!")
					view.message = await hembed.edit(embed=helpembed, view=view)
				elif command == 'utility':
					view = interaction.Help_select(ctx, ctx.author)
					helpembed = discord.Embed(title="Utility commands", description="`.help <command>` for more information of a specific command", color = color.blue())
					helpembed.add_field(name = 'Utility helpful commands', value = f"`{'`, `'.join(sorted([command.name for command in self.bot.get_cog('UtilityCog').walk_commands() if command.hidden is False]))}`", inline=True)
					helpembed.set_footer(text="Type '.help <command name>' to read the details!")
					view.message = await hembed.edit(embed=helpembed, view=view)
			return
		cmd = self.bot.get_command(command)
		if not cmd or (ctx.author.id != 615037304616255491 and cmd.hidden is True):
			await ctx.reply(f"Couldn't find this command: `{command}`")
			return
		try:
			helpembed = discord.Embed(title=f"{cmd.name}", color = color.blue())
			helpembed.add_field(name = 'Description', value = f"{cmd.description}", inline=False)
			helpembed.add_field(name = 'Usage', value = f"`{cmd.usage}`", inline=False)
			helpembed.add_field(name = 'Aliases', value = f"{', '.join(cmd.aliases if cmd.aliases else ['No aliases'])}", inline=False)
			helpembed.set_footer(text="<> = Necessary | [] = Unnecessary")
			await ctx.reply(embed=helpembed)
			return
		except:
			await ctx.reply(f"Couldn't find this command: `{command}`")
			return

	@commands.command(aliases=['bal', 'coin', 'coins', 'brc'], description="Remind oneself of your poverty", usage='.balance [user]')
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def balance(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author

		userp = await functions.finduser(user.id)

		embed = discord.Embed(title=f"{ctx.author}'s balance", description = f"**Braincoin** <:braincoin:976109339414790184> {functions.money(round(userp['coin']))} BRC", color=0xf801fc)
		embed.set_footer(text="poor")

		await ctx.reply(embed=embed)

	@commands.command(description="Check your ETH balance in your personal bank, can be withdrawed in our website", usage=".bank")
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.check(functions.is_linked)
	async def bank(self, ctx):
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(ctx.author.id)][0]
		user = await functions.pcllfinduser(address)
		if user is not None:
			eth = user["bank"]
		else:
			eth = 0
		embed = discord.Embed(title=f"{ctx.author}'s bank", description=f"**Ethereum** <:ethereum:977198783479808060> {eth} ETH", color=color.blurple()).set_footer(text="Purchase ETH from the shop using Braincoins!")
		await ctx.reply(embed=embed)

	@commands.command(aliases=['check-in'], description="Safe Staking. Check in every 24 hours to get free Braincoins for Brain Juices you own", usage=".checkin")
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.check(functions.is_linked)
	async def checkin(self, ctx):
		user = await functions.finduser(ctx.author.id)
		if user["daily"] > round(time.time()):
			embed = discord.Embed(title="Command on cooldown!", color=color.gold()).add_field(name="You have to wait before checking in again!", value=f"Try again after `{functions.time2text(user['daily']-round(time.time()))}`!\nCooldown for this checking in is `{functions.time2text(86400)}`").set_footer(text="Chill!")
			await ctx.reply(embed=embed)
			return
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(ctx.author.id)][0]
		nfts = functions.contract.functions.nftsOwned(address).call()
		if nfts == []:
			await ctx.reply("Too bad! You don't own any Brain Juices hence there is nothing for you :(")
			return
		coin = 0
		for nft in nfts:
			with open(f"{os.getcwd()}\\metadata\\{nft}.json", 'r') as f:
				coin += self.bot.rewards[json.loads(f.read())["attributes"][-2]["value"]]
		multiplier = 1
		multiplier += (0.4 if len(nfts) >= 11 else 0.3 if len(nfts) >= 6 else 0.2 if len(nfts) >= 4 else 0.1 if len(nfts) >= 2 else 0)
		multiplier += (0.1 if "brain juice" in ctx.author.name.lower() or "brainjuice" in ctx.author.name.lower() else 0)
		coin = round(coin*multiplier)
		await functions.cll.update_one({"id": ctx.author.id}, {"$set": {"daily": round(time.time())+86400}, "$inc": {"coin": coin}})
		embed = discord.Embed(title="Checked in", description=f"Welcome back, {ctx.author.mention} how was your day? :grin:\n<:braincoin:976109339414790184> **{functions.money(coin)} BRC (x{multiplier} Multiplier)** has been added to your balance!", color=color.green()).set_footer(text="Come back every 24 hours!")
		await ctx.reply(embed=embed)
		await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} add) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user['coin'])} + <:braincoin:976109339414790184> {functions.money(coin)} = <:braincoin:976109339414790184> {functions.money(user['coin']+coin)} {ctx.message.jump_url}")

	@commands.command(description="Gallery for Brain Juices you own", usage=".gallery")
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.check(functions.is_linked)
	async def gallery(self, ctx):
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(ctx.author.id)][0]
		nfts = functions.contract.functions.nftsOwned(address).call()
		if nfts == []:
			await ctx.reply(embed=discord.Embed(title=f"{ctx.author}'s gallery", description="You don't have own Brain Juices! That's devastating :(", color=color.blurple()))
			return
		page = 1
		with open(f"{os.getcwd()}\\metadata\\{nfts[page-1]}.json", 'r') as f:
			data = json.loads(f.read())
			background = data["attributes"][0]["value"]
			flesh = data["attributes"][1]["value"]
			eye = data["attributes"][2]["value"]
			accessory = data["attributes"][3]["value"]
			rarity = data["attributes"][4]["value"]
			phase = data["attributes"][5]["value"]
			image = data["image"]
		embed = discord.Embed(title=f"{ctx.author}'s gallery", description=f"**Brain Juice #{nfts[page-1]-1:04}**", color=color.random()).add_field(name="Traits", value=f"**Background** {background}\n**Flesh** {flesh}\n**Eye** {eye}\n**Accessory** {accessory}\n**Rarity** {rarity}\n**Phase** {phase}").set_image(url=image).set_footer(text=f"Brain Juice {page} of {len(nfts)}")
		view = interaction.Page(ctx, ctx.author, page == 1, page == len(nfts))
		view.message = msg = await ctx.reply(embed=embed, view=view)

		while True:
			await view.wait()
			if view.value is None:
				return
			elif view.value == "left":
				page -= 1
			elif view.value == "right":
				page += 1
			elif view.value == "begin":
				page = 1
			elif view.value  == "end":
				page = len(nfts)

			with open(f"{os.getcwd()}\\metadata\\{nfts[page-1]}.json", 'r') as f:
				data = json.loads(f.read())
				background = data["attributes"][0]["value"]
				flesh = data["attributes"][1]["value"]
				eye = data["attributes"][2]["value"]
				accessory = data["attributes"][3]["value"]
				rarity = data["attributes"][4]["value"]
				phase = data["attributes"][5]["value"]
				image = data["image"]
			embed = discord.Embed(title=f"{ctx.author}'s gallery", description=f"**Brain Juice #{nfts[page-1]-1:04}**", color=color.random()).add_field(name="Traits", value=f"**Background** {background}\n**Flesh** {flesh}\n**Eye** {eye}\n**Accessory** {accessory}\n**Rarity** {rarity}\n**Phase** {phase}").set_image(url=image).set_footer(text=f"Brain Juice {page} of {len(nfts)}")
			view = interaction.Page(ctx, ctx.author, page == 1, page == len(nfts))
			view.message = await msg.edit(embed=embed, view=view)

	@commands.command(aliases=["wal"], description="Shows a list of Brain Juices you own", usage=".wallet")
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.check(functions.is_linked)
	async def wallet(self, ctx):
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(ctx.author.id)][0]
		nfts = functions.contract.functions.nftsOwned(address).call()
		if nfts == []:
			await ctx.reply(discord.Embed(title=f"{ctx.author}'s Brain Juices", description="You don't have own Brain Juices! That's devastating :(", color=color.random()))
			return
		page = 1
		embed = discord.Embed(title=f"{ctx.author}'s Brain Juices", description="", color=color.random()).set_footer(text=f"Page {page} of {-(-len(nfts)//10)}")
		for nft in nfts[(page-1)*10:(page-1)*10+10]:
			with open(f"{os.getcwd()}\\metadata\\{nft}.json", 'r') as f:
				embed.description += f"**Brain Juice #{nft-1:04}** | **Rarity** {json.loads(f.read())['attributes'][4]['value']}\n"
		view = interaction.Page(ctx, ctx.author, page == 1, page == -(-len(nfts)//10))
		view.message = msg = await ctx.reply(embed=embed, view=view)

		while True:
			await view.wait()
			if view.value is None:
				return
			elif view.value == "left":
				page -= 1
			elif view.value == "right":
				page += 1
			elif view.value == "begin":
				page = 1
			elif view.value  == "end":
				page = len(nfts)

			embed = discord.Embed(title=f"{ctx.author}'s Brain Juices", description="", color=color.random()).set_footer(text=f"Page {page} of {-(-len(nfts)//10)}")
			for nft in nfts[(page-1)*10:(page-1)*10+10]:
				with open(f"{os.getcwd()}\\metadata\\{nft}.json", 'r') as f:
					embed.description += f"**Brain Juice #{nft-1:04}** | **Rarity** {json.loads(f.read())['attributes'][4]['value']}\n"
			view = interaction.Page(ctx, ctx.author, page == 1, page == -(-len(nfts)//10))
			view.message = await msg.edit(embed=embed, view=view)

	@commands.command(aliases=["store"], description="Visit the Brain Shop", usage=".wallet")
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def shop(self, ctx):
		user = await functions.finduser(ctx.author.id)
		items = ["Whitelist"]
		item_price = {"Whitelist": 500}
		item_description = {"Whitelist": "Whitelist spot for minting during presale!"}
		page = 1
		item_stock = (await functions.ccll.find_one({"id": "stock"}))["data"]
		embed = discord.Embed(title="Shop", description=f"**{items[page-1]}**\n{item_description[items[page-1]]}\n<:braincoin:976109339414790184> {item_price[items[page-1]]} BRC\n\n**Stock left** {item_stock[items[page-1]]}", color=color.random()).set_footer(text=f"Page {page} of {len(items)}")
		view = interaction.Shop(ctx, ctx.author, user["coin"] < item_price[items[page-1]], item_stock[items[page-1]] <= 0, page == 1, page == len(items))
		view.message = msg = await ctx.reply(embed=embed, view=view)

		while True:
			await view.wait()
			if view.value is None:
				return
			elif view.value == "left":
				page -= 1
			elif view.value == "right":
				page += 1
			elif view.value == "begin":
				page = 1
			elif view.value  == "end":
				page = len(items)
			elif view.value == "buy":
				item_stock = (await functions.ccll.find_one({"id": "stock"}))["data"]
				if items[page-1] in list(item_stock.keys()) and item_stock[items[page-1]] <= 0:
					await ctx.reply("This item ran out of stock!")
				else:
					if items[page-1] == "Whitelist":
						if ctx.author.get_role(981556857355272242) is not None:
							await ctx.reply("You are already whitelisted!")
							return
						await functions.ccll.update_one({"id": "stock"}, {"$inc": {f"data.{items[page-1]}": -1}})
						await functions.updateinc(ctx.author.id, "coin", -item_price[items[page-1]])
						await ctx.author.add_roles(ctx.guild.get_role(981556857355272242))
						await ctx.reply(f"You paid <:braincoin:976109339414790184> {item_price[items[page-1]]} BRC and have been successfully whitelisted!")
					# await ctx.reply(f"You have successfully purchased a **{items[page-1]}** for <:braincoin:976109339414790184> {item_price[items[page-1]]} BRC!")

			item_stock = (await functions.ccll.find_one({"id": "stock"}))["data"]
			embed = discord.Embed(title="Shop", description=f"**{items[page-1]}**\n{item_description[items[page-1]]}\n<:braincoin:976109339414790184> {item_price[items[page-1]]} BRC\n\n**Stock left** {item_stock[items[page-1]]}", color=color.random()).set_footer(text=f"Page {page} of {len(items)}")
			view = interaction.Shop(ctx, ctx.author, user["coin"] < item_price[items[page-1]], item_stock[items[page-1]] <= 0, page == 1, page == len(items))
			view.message = await msg.edit(embed=embed, view=view)

	# @commands.command(description="Check the metadata of a Brain Juice", usage=".info <ID>")
	# @commands.cooldown(1, 2, commands.BucketType.user)
	async def info(self, ctx, id: int = None):
		if id is None:
			await ctx.reply("You have to provide a Brain Juice ID!")
			return
		try:
			with open(f"{os.getcwd()}\\metadata\\{id}.json", 'r') as f:
				data = json.loads(f.read())
				background = data["attributes"][0]["value"]
				flesh = data["attributes"][1]["value"]
				eye = data["attributes"][2]["value"]
				accessory = data["attributes"][3]["value"]
				rarity = data["attributes"][4]["value"]
				phase = data["attributes"][5]["value"]
				image = data["image"]
		except:
			await ctx.reply("No Brain Juices with this ID found!")
			return
		embed = discord.Embed(title=f"Brain Juice #{id:04}", color=color.random()).add_field(name="Traits", value=f"**Background** {background}\n**Flesh** {flesh}\n**Eye** {eye}\n**Accessory** {accessory}\n**Rarity** {rarity}\n**Phase** {phase}").set_image(url=image)
		await ctx.reply(embed=embed)

def setup(bot):
	bot.add_cog(MainCog(bot))
