import os
import discord
from discord.ext import commands
import functions
from dotenv import load_dotenv
from datetime import datetime, timezone
import asyncio
import interaction

load_dotenv()

discord.http.API_VERSION = 9
dakey = os.getenv("TOKEN")
commandprefix = ["."]
prefix = "."
intents = discord.Intents.default()
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(*commandprefix), help_command=None, case_insensitive=True,intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False, roles=True))
color = discord.Colour

errors = ["Minting is still not available yet!", "Oops! Seems like it's out of stock!", "Not enough funds!", "You are not whitelisted! Wait for public mint", "Token ID doesn't exist!", "Amount must be more than 0!", "You are not the owner of this NFT!", "Address 0", "This token is already minted!"]
bot.errors = errors
# Rarity:Count | 1000 600 300 100 || Rarity:Rewards | 100 120 140 150 * 2.86
# Daily expenses if all 2000 staked
# 654940 coins given out everyday, 0.005 ETH for 57200 coins * 12 = 0.06 ETH $180
# Daily trades requirement 0.1 ETH 5% 0.005 ETH $15 | $180/$15 12 Trades needed everyday
# Daily trade volume requirement 0.1 * 12 = 1.2 ETH
bot.rewards = {"Common": 286, "Rare": 343, "Mythical": 400, "Legendary": 429}

extensions = ["cogs.devcog", "cogs.maincog", "cogs.funcog", "cogs.utilitycog", "cogs.ticketcog"]
bot.extension = extensions
bot.snipe = {}
bot.pending = {}

print(__name__)
if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)
		print(f"Loaded {extension[5:].capitalize()} extension")

async def delete_channel(ctx, seconds):
	await asyncio.sleep(seconds)
	await ctx.channel.delete(reason=f"Ticket {ctx.channel.name} closed by {ctx.author}.")
	
	user = bot.get_user(int(ctx.channel.topic.split(" ")[-1]))

	log = discord.Embed(title="Ticket closed",description=f"Ticket for **{user} ({user.id})** was closed by **{ctx.author}**", color=color.red())
	log.timestamp = datetime.now()

	await botlogs.send(embed=log)

	del bot.pending[ctx.author.id]

bot.delete_channel = delete_channel

@bot.check
async def new_user(ctx):
	if str(ctx.author.id) in (await functions.ccllfinddoc("blacklist"))["data"]:
		await ctx.reply(f"You are blacklisted! DM {bot.user.mention} to make a blacklist appeal")
		return False
	if await functions.finduser(ctx.author.id) is None and ctx.command.name not in ["setup", "help", "define", "mute", "kick", "suggest", "snipe"]:
		await ctx.reply("Type `.setup` to setup your profile to use the bot!")
		return False
	return True

@bot.check
async def perm(ctx):
	role = ctx.author.get_role(ticket_permission_role)
	if role is None:
		await ctx.reply("You don't have the permission to use ticket commands!")
		return False
	return True

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")
	await asyncio.sleep(3)
	await bot.wait_until_ready()
	await bot.change_presence(activity=discord.Game("DM for support!"))
	global mainserver
	global server
	global botlogs
	global ticket_category
	global ticket_permission_role
	mainserver = bot.get_guild(947688785565589584)
	server = bot.get_guild(947688785565589584)
	mainserver = mainserver or server
	botlogs = bot.get_channel(947747400557154314)
	ticket_category = 983921677727580160
	ticket_permission_role = 982240058318942228

	bot.mainserver = mainserver
	bot.server = server
	bot.botlogs = botlogs
	bot.ticket_category = ticket_category
	bot.ticket_permission_role = ticket_permission_role
	print("Setup completed")

# @bot.event
# async def on_command(ctx):

@bot.event
async def on_command_error(ctx, error):
	if not isinstance(error, commands.CommandOnCooldown):
		try:
			ctx.command.reset_cooldown(ctx)
		except:
			pass
	if isinstance(error, commands.CommandOnCooldown):
		cdembed = discord.Embed(title="Command on cooldown!", color=color.gold())
		cdembed.add_field(name="You have to wait before typing the command again!", value=f"Try again after `{functions.time2text(error.retry_after)}`!\nCooldown for this command is `{functions.time2text(error.cooldown.per)}`")
		cdembed.set_footer(text="Chill!")

		await ctx.reply(embed=cdembed)
	elif isinstance(error, commands.UserNotFound):
		await ctx.reply("Cannot find this user!")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.reply("Cannot find this member!")
	elif isinstance(error, commands.BadArgument) or isinstance(error, commands.BadUnionArgument):
		await ctx.reply("Enter something valid")
	elif isinstance(error, commands.CommandInvokeError):
		error = error.original
		if isinstance(error, discord.HTTPException):
			if error.code == 50035:
				await ctx.reply("Embed error")
				return
			elif error.code == 50015 or error.code == 50013:
				await ctx.reply("I don't have the permission to do that!")
				return
	if not any([isinstance(error, commands.CommandNotFound), isinstance(error, commands.CommandOnCooldown), isinstance(error, commands.CheckFailure)]):
		print(f"{ctx.author}: {ctx.command} | {ctx.message.content} | " + str(error)[:200])
		await bot.get_channel(947747400557154314).send(f"**Error from {ctx.author} ({ctx.author.id})**: Command `{ctx.command}` | {ctx.message.content} | {str(error)[:200]}")

@bot.event
async def on_message(msg):
	if msg.author.bot:
		return

	if "how" in msg.content and "whitelist" in msg.content:
		await msg.reply("Check the <#948933476760027157> channel for whitelist information!")

	await bot.process_commands(msg)

	if msg.guild is None:
		member = mainserver.get_member(msg.author.id)

		channel = None

		for x in server.text_channels:
			if not x.topic is None and x.name.startswith("ticket"):
				if x.topic.split(" ")[-1] == str(member.id):
					channel = x
					break

		if channel is None:
			warn = discord.Embed(title="Warning!", description="You are currently requesting support from the the Brain Juice Staff Team, make sure you have any questions that is not answered in these channels <#983616882760351804> <#948933476760027157> <#983369003240132678> before continuing!\n\n**Are you sure you want to request for support from the Brain Juice Staff Team?**", color=color.gold())
			warn.set_author(name="Brain Juice", icon_url=mainserver.icon.url)
			warn.set_footer(text="Brain Juice Staff Team")
			warn.timestamp = datetime.now()
			view = interaction.Confirm(msg, msg.author)
			view.message = await member.send(embed=warn, view=view)

			await view.wait()

			if view.value == None:
				await member.send("Support requesting cancelled because you did not respond.")
				return
			elif view.value == False:
				await member.send("Support requesting cancelled.")
				return

			choose = discord.Embed(title="Choose your question category", description="Before continuing, our Staff Team would like to know what kind of questions are you requesting for?", color=color.gold())
			choose.set_author(name="Brain Juice", icon_url=mainserver.icon.url)
			choose.set_footer(text="Brain Juice Staff Team")
			choose.timestamp = datetime.now()
			view = interaction.Question(msg, msg.author)
			view.message = await member.send(embed=choose, view=view)
			await view.wait()

			if view.value == []:
				await member.send("Support requesting cancelled because you did not respond.")
				return
			
			complete = discord.Embed(title="Ticket created", description="What’s up!\n\nThanks for your response. You can now send message about your question. Our staff team will tackle your request as soon as possible. Thank you for your patience.\n\n> Cheers!\n> **Brain Juice Staff Team**", color=color.green())
			complete.set_author(name="Brain Juice", icon_url=mainserver.icon.url)
			complete.set_footer(text="Brain Juice Staff Team")
			complete.timestamp = datetime.now()

			await member.send(embed=complete)

			category = discord.utils.get(server.categories, id=ticket_category)
			channel = await category.create_text_channel(name=f"ticket-{msg.author.name.lower()}-{msg.author.discriminator}", topic=f"Not Claimed | User: {msg.author} {msg.author.id}")
			await channel.edit(category=category, sync_permissions=True)
			await channel.move(category=category, end=True)

			await member.create_dm()

			now = datetime.utcnow().replace(tzinfo=timezone.utc)
			user_created_at = msg.author.created_at
			try:
				created = int(str(now-user_created_at).split(" ")[0])
				if created == 1:
					created = str(created) + " day ago"
				else:
					created = str(created) + " days ago"
			except:
				created = "**today**"

			user_joined_at = member.joined_at
			if user_joined_at == None:
				joined = ""
				open = discord.Embed(title=f"{msg.author} requested for support",description=f"User **{msg.author}** ID **{msg.author.id}** account was created {created}, **This user did not join {mainserver.name}**.", color=color.gold())
			else:
				try:
					joined = int(str(now-user_joined_at).split(" ")[0])
					if joined == 1:
						joined = str(joined) + " day ago"
					else:
						joined = str(joined) + " days ago"
				except:
					joined = "**today**"
				open = discord.Embed(title=f"{msg.author} requested for support",description=f"User **{msg.author}** ID **{msg.author.id}** account was created at {created}, joined {mainserver.name} at {joined}.", color=color.green())

				open.add_field(name="Help category", value=f"{view.value[0]}\n\n**Description**\n{view.value[1]}")

			if member.nick:
				open.add_field(name="Server Nickname", value=member.nick)
			if member.premium_since:
				open.add_field(name="Server booster", value=f"Server booster since {member.premium_since.strftime('%Y-%m-%d')}")
			open.add_field(name="Roles", value=", ".join([x.name for x in member.roles[1:]]), inline=False)
			open.set_author(name=msg.author,icon_url=msg.author.display_avatar.url)
			open.set_thumbnail(url=msg.author.display_avatar.url)
			open.set_footer(text=f"DM Channel: {member.dm_channel.id}")
			open.timestamp = datetime.now()

			pin = await channel.send(f"<@&{ticket_permission_role}> **DO NOT EDIT THREAD TOPIC**", embed=open)
			await pin.pin(reason="Ticket user information")
			await channel.purge(limit=1)

			log = discord.Embed(title="Ticket created",description=f"Ticket for **{member} ({member.id})** has been created.\n[Click here to jump to the thread]({pin.jump_url})", color=color.green())
			log.timestamp = datetime.now()

			await botlogs.send(embed=log)
			return
		
		await msg.add_reaction("\U00002705")

		if bot.pending.get(msg.author.id) is not None:
			bot.pending[msg.author.id].cancel()
			del bot.pending[msg.author.id]

			reopen = discord.Embed(title="Ticket reopened", description=f"Ticket reopened due to user **{msg.author}** sent a message", color=color.green())
			reopen.timestamp = datetime.now()
			reopen.set_author(name=msg.author, icon_url=msg.author.display_avatar.url)
			pin = await channel.send(embed=reopen)
			await pin.pin(reason="Ticket reopened")
			await channel.purge(limit=1)

			reopen = discord.Embed(title="Ticket reopened", description="Ticket reopened because you sent a message", color=color.green())
			reopen.timestamp = datetime.now()

			if channel.topic.split(" ")[0] == "Claimed":
				await member.send(f"{bot.get_user(int(channel.topic.split(' | ')[0].split(' ')[-1])).mention}", embed=reopen)
			else:
				await member.send(f"<@&{ticket_permission_role}>", embed=reopen)

			log = discord.Embed(title="Ticket reopened",description=f"Ticket for **{member} ({member.id})** has been reopened due to {member} sent a message.\n[Click here to jump to the thread]({pin.jump_url})", color=color.green())
			log.timestamp = datetime.now()

			await botlogs.send(embed=log)

		claimer = None
		if channel.topic.split(" ")[0] == "Claimed":
			claimer = bot.get_user(int(channel.topic.split(" | ")[0].split(" ")[-1]))
		
		membed = discord.Embed(description=msg.content,color=color.gold())
		membed.set_author(name=f"{msg.author}",icon_url=msg.author.display_avatar.url)
		membed.set_footer(text=f"Message ID: {msg.id}")
		membed.timestamp = datetime.now()

		if msg.attachments != []:
			file = msg.attachments[0]
			msg.content += "\n"
			if file.content_type.startswith("text/plain"):
				membed.description = msg.content + f"**File attached:** [{file.filename}]({file.url})"
				await channel.send(content=claimer.mention if claimer else None, embed=membed)
				await channel.send(f"**Text file sent by {msg.author}**",file=await file.to_file())
			else:
				membed.description = msg.content + f"**Image attached:** [{file.filename}]({file.url})"
				membed.set_image(url=file.url)
				await channel.send(content=claimer.mention if claimer else None, embed=membed)
		else:
			await channel.send(content=claimer.mention if claimer else None, embed=membed)

@bot.event
async def on_message_delete(message):
	if message.attachments == []:
		bot.snipe[message.channel.id] = {"mention": message.author.mention, "content": message.content, "avatar": message.author.display_avatar.url, "created_at": message.created_at}
	else:
		bot.snipe[message.channel.id] = {"mention": message.author.mention, "content": message.content, "avatar": message.author.display_avatar.url, "created_at": message.created_at, "attachment_proxy_url": message.attachments[0].proxy_url, "attachment_filename": message.attachments[0].filename}

@bot.event
async def on_member_join(member):
	await bot.get_channel(947688786035376128).send(f"Welcome, {member.mention}! Remember to read <#983676718004961330> to get started, and have fun!")

bot.run(dakey)
