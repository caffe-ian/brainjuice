import discord
from discord.ext import commands
import functions
import os
import json
import interaction
import datetime

color = discord.Colour

class UtilityCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Create a giveaway", usage=".giveaway")
	async def giveaway(self, ctx, channel, time, prize, desc="Click the button below to join the giveaway!"):
		if ctx.author.id != 

	@commands.command(description="Set up your profile to start using the bot", usage=".setup")
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def setup(self, ctx):
		if await functions.finduser(ctx.author.id) is not None:
			await ctx.reply("You have already set up your profile!")
			return
		await functions.insertdict({"id": ctx.author.id, "coin": 0, "daily": 0})
		embed = discord.Embed(title=f"Welcome, {ctx.author}!", description="Type `.help` to look at all the available commands\nType `.checkin` every 24 hours if you own any Brain Juices to earn Braincoins!\n\nBraincoins <:braincoin:976109339414790184> can be used to purchase **ETH** <:ethereum:977198783479808060> or other items from the shop", color=color.green())
		await ctx.send(embed=embed)

	@commands.command(aliases=["reward"], description="Check safe staking rewards", usage=".rewards")
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def rewards(self, ctx):
		embed = discord.Embed(title="Safe staking rewards", color=color.blurple()).add_field(name="Rewards", value=f"**Common** <:braincoin:976109339414790184> {self.bot.rewards['Common']} BRC\n**Rare** <:braincoin:976109339414790184> {self.bot.rewards['Rare']} BRC\n**Mythical** <:braincoin:976109339414790184> {self.bot.rewards['Mythical']} BRC\n**Legendary** <:braincoin:976109339414790184> {self.bot.rewards['Legendary']} BRC", inline=False).add_field(name="Multipliers", value="**10% -** Have `Brain Juice` or `BrainJuice` in your **username**\n**10% -** Own 2 or more Brain Juices\n**10% -** Own 4 or more Brain Juices\n**10% -** Own 6 or more Brain Juices\n**10% -** Own 11 or more Brain Juices", inline=False).set_footer(text="Type '.checkin' to claim your reward!")
		address = [k for k, v in (await functions.ccllfinddoc("discord_id"))["data"].items() if v == str(ctx.author.id)]
		if address != []:
			address = address[0]
			nfts = functions.contract.functions.nftsOwned(address).call()
			if nfts != []:
				coin = 0
				for nft in nfts:
					with open(f"{os.getcwd()}\\metadata\\{nft}.json", 'r') as f:
						coin += self.bot.rewards[json.loads(f.read())["attributes"][-2]["value"]]
				multiplier = 1
				multiplier += (0.4 if len(nfts) >= 11 else 0.3 if len(nfts) >= 6 else 0.2 if len(nfts) >= 4 else 0.1 if len(nfts) >= 2 else 0)
				multiplier += (0.1 if "brain juice" in ctx.author.name.lower() or "brainjuice" in ctx.author.name.lower() else 0)
				embed.add_field(name="Your check in reward", value=f"**<:braincoin:976109339414790184> {functions.money(round(coin*multiplier))} BRC** (x{multiplier} Multiplier)", inline=False)
		await ctx.send(embed=embed)

	@commands.command(description="Mute someone through voting", usage=".mute <user> [duration in seconds] [reason]")
	@commands.cooldown(1, 600, commands.BucketType.user)
	async def mute(self, ctx, user: discord.Member = None, duration: int = 600, reason: str = "No reason"):
		if user is None:
			await ctx.reply("Who do you want to mute?")
			ctx.command.reset_cooldown(ctx)
			return
		elif user == ctx.author:
			await ctx.reply("You cannot poll to mute yourself idiot")
			ctx.command.reset_cooldown(ctx)
			return
		elif user.bot:
			await ctx.reply("Haha nice try, you can't mute a bot :P")
			ctx.command.reset_cooldown(ctx)
			return
		elif duration < 1:
			await ctx.reply("Minimum duration is 1 second")
			ctx.command.reset_cooldown(ctx)
			return
		elif duration > 86400:
			await ctx.reply("Maximum duration is 24 hours (86400 seconds)")
			ctx.command.reset_cooldown(ctx)
			return
		if ctx.author.get_role(982240058318942228) is not None:
			await user.timeout_for(datetime.timedelta(seconds=duration), reason=reason)
			await ctx.reply(f"Muted {user} for {functions.time2text(duration)} with the reason: {reason}")
			await self.bot.get_channel(947747400557154314).send(f"{ctx.author} muted {user} with the reason: {reason}")
			ctx.command.reset_cooldown(ctx)
			return
		voted = []
		votes = 0
		req = -(-duration // 60) if duration < 3600 else 10 if duration < 7200 else 15 if duration < 21600 else 20
		embed = discord.Embed(title=f"Poll for muting {user}", description=f"**Mute duration** {functions.time2text(duration)}\n**Mute reason** {reason}\n\n**Votes required** {req}\n**Current votes** {votes}", color=color.random()).set_footer(text="Expires in 10 minutes")

		view = interaction.Vote(ctx, voted, req)
		view.message = msg = await ctx.send(embed=embed, view=view)

		await view.wait()

		if view.value == None:
			await ctx.reply("Poll has expired because no one voted")
			await msg.edit(content="This poll has **expired**")
		elif view.value == "success":
			await ctx.reply(f"Poll consented, {user} has been muted for {functions.time2text(duration)}")
			await user.timeout_for(datetime.timedelta(seconds=duration), reason=reason)
			await msg.edit(content="This poll has been **consented**")
			await self.bot.get_channel(947747400557154314).send(discord.Embed(title="Muting poll consented", description=f"Poll created by {ctx.author} muting {user} for {functions.time2text(duration)} has been consented with {req} votes and the reason: {reason}\n\n**Users voted** {', '.join(voted)}\n\n[Jump to message]({ctx.message.jump_url})"), color=color.gold())
		elif view.value == "revoke":
			await ctx.reply("This poll has been revoked")
			await msg.edit(content="This poll has been **revoked**")

	@commands.command(description="Kick someone through voting", usage=".kick <user> [reason]")
	@commands.cooldown(1, 21600, commands.BucketType.user)
	async def kick(self, ctx, user: discord.Member = None, reason: str = "No reason"):
		if user is None:
			await ctx.reply("Who do you want to kick?")
			ctx.command.reset_cooldown(ctx)
			return
		elif user == ctx.author:
			await ctx.reply("You cannot poll to kick yourself idiot")
			ctx.command.reset_cooldown(ctx)
			return
		elif user.bot:
			await ctx.reply("Haha nice try, you can't kick a bot :P")
			ctx.command.reset_cooldown(ctx)
			return
		if ctx.author.get_role(982240058318942228) is not None:
			await user.kick(reason=reason)
			await ctx.reply(f"Kicked {user} with the reason: {reason}")
			await self.bot.get_channel(947747400557154314).send(f"{ctx.author} kicked {user} with the reason: {reason}")
			ctx.command.reset_cooldown(ctx)
			return
		voted = []
		votes = 0
		req = 10
		embed = discord.Embed(title=f"Poll for kicking {user}", description=f"**Kick reason** {reason}\n\n**Votes required** {req}\n**Current votes** {votes}", color=color.random()).set_footer(text="Expires in 10 minutes")

		view = interaction.Vote(ctx, voted, req)
		view.message = msg = await ctx.send(embed=embed, view=view)

		await view.wait()

		if view.value == None:
			await ctx.reply("Poll has expired because no one voted")
			await msg.edit(content="This poll has **expired**")
		elif view.value == "success":
			await ctx.reply(f"Poll consented, {user} has been kicked")
			await user.kick(reason=reason)
			await msg.edit(content="This poll has been **consented**")
			await self.bot.get_channel(947747400557154314).send(discord.Embed(title="Kicking poll consented", description=f"Poll created by {ctx.author} kicking {user} has been consented with {req} votes and the reason: {reason}\n\n**Users voted** {', '.join(voted)}\n\n[Jump to message]({ctx.message.jump_url})"), color=color.gold())
		elif view.value == "revoke":
			await ctx.reply("This poll has been revoked")
			await msg.edit(content="This poll has been **revoked**")

	@commands.command(description="Make a suggestion", usage=".suggest <suggestion>")
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def suggest(self, ctx, suggestion: str = None):
		if suggestion is None:
			await ctx.reply("You have to give a suggestion!")
			ctx.command.reset_cooldown(ctx)
			return
		elif len(suggestion < 8):
			await ctx.reply("Suggestion must be at least 8 letters long")
			ctx.command.reset_cooldown(ctx)
			return
		elif "https://" in suggestion or "http://" in suggestion:
			await ctx.reply("Links are not allowed in suggestions")
			ctx.command.reset_cooldown(ctx)
			return
		msg = await self.bot.get_channel(982582724198006794).send(embed=discord.Embed(title=f"Suggestion by {ctx.author}", description=suggestion, color=color.blurple()))
		await msg.add_reaction("\U00002b06")
		await msg.add_reaction("\U00002b07")
		await ctx.send(embed=discord.Embed(title="Suggestion posted", description=f"Your suggestion has been succesfully posted\n\n[Jump to post]({msg})"))

def setup(bot):
	bot.add_cog(UtilityCog(bot))