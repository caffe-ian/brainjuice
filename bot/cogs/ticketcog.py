import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import functions
import interaction

color = discord.Colour

class TicketCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['r'], description="Reply to the user", usage="reply <message>")
	async def reply(self, ctx, *, message = ""):
		if len(ctx.channel.name.split("-")[-1]) != 4 or ctx.channel.name.split("-")[-1].isdigit() == False or len(ctx.channel.name) <= 4 or ctx.channel.topic == None or not ctx.channel.name.startswith("ticket"):
			await ctx.send("This is not a Ticket!")
			return
		if not ctx.channel.topic == None:
			try:
				user = self.bot.get_user(int(ctx.channel.topic.split(" ")[-1]))
			except:
				await ctx.send("This is not a Ticket!")
				return
		
		if message == "" and ctx.message.attachments == []:
			await ctx.send("You cannot send empty messages")
			return

		await ctx.channel.purge(limit=1)

		membed = discord.Embed(description=message,color=color.green())
		membed.set_author(name=f"{ctx.author}",icon_url=ctx.author.display_avatar.url)
		membed.set_footer(text="Brain Juice Staff Team")
		membed.timestamp = datetime.now()

		if ctx.message.attachments != []:
			file = ctx.message.attachments[0]
			message += "\n"
			if file.content_type.startswith("text/plain"):
				membed.description = message + f"**File attached:** [{file.filename}]({file.url})"
				msg = await user.send(embed=membed)
				msg2 = await user.send(f"**Text file sent by {ctx.author}**",file=await file.to_file())
				membed.set_footer(text=f"Message ID: {msg.id}, File message ID: {msg2.id}")
				await ctx.send(embed=membed)
				await ctx.send(f"**Text file sent by {ctx.author}**",file=await file.to_file())
			else:
				membed.description = message + f"**Image attached:** [{file.filename}]({file.url})"
				membed.set_image(url=file.url)
				msg = await user.send(embed=membed)
				membed.set_footer(text=f"Message ID: {msg.id}")
				await ctx.send(embed=membed)
		else:
			msg = await user.send(embed=membed)
			membed.set_footer(text=f"Message ID: {msg.id}")
			await ctx.send(embed=membed)

		if self.bot.pending.get(user.id) is not None:
			self.bot.pending[user.id].cancel()
			del self.bot.pending[user.id]

			reopen = discord.Embed(title="Ticket reopened", description=f"Ticket reopened due to **{ctx.author}** sent a message to {user}", color=color.green())
			reopen.timestamp = datetime.now()
			reopen.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
			pin = await ctx.channel.send(embed=reopen)
			await pin.pin(reason="Ticket reopened")
			await ctx.channel.purge(limit=1)

			reopen = discord.Embed(title="Ticket reopened", description=f"Ticket reopened because {ctx.author} sent you a message", color=color.green())
			reopen.timestamp = datetime.now()

			await user.send(embed=reopen)

			log = discord.Embed(title="Ticket reopened",description=f"Ticket for **{user} ({user.id})** has been reopened due to {ctx.author} sent a message to {user}.\n[Click here to jump to the ticket]({pin.jump_url})", color=color.green())
			log.timestamp = datetime.now()

			await self.bot.botlogs.send(embed=log)

	@commands.command(aliases=['ar','anonymousreply'], usage="areply <message>")
	async def areply(self, ctx, *, message = ""):
		"""Reply to the user anonymously"""
		if len(ctx.channel.name.split("-")[-1]) != 4 or ctx.channel.name.split("-")[-1].isdigit() == False or len(ctx.channel.name) <= 4 or ctx.channel.topic == None or not ctx.channel.name.startswith("ticket"):
			await ctx.send("This is not a Ticket!")
			return
		if not ctx.channel.topic == None:
			try:
				user = self.bot.get_user(int(ctx.channel.topic.split(" ")[-1]))
			except:
				await ctx.send("This is not a Ticket!")
				return

		if message == "" and ctx.message.attachments == []:
			await ctx.send("You cannot send empty messages")
			return

		await ctx.channel.purge(limit=1)

		membed = discord.Embed(description=message,color=color.green())
		membed.set_author(name=f"{[x for x in ctx.author.roles if x.color != color.default()][-1].name}",icon_url=self.bot.mainserver.icon.url)
		membed.set_footer(text="Brain Juice Staff Team")
		membed.timestamp = datetime.now()

		if ctx.message.attachments != []:
			file = ctx.message.attachments[0]
			message += "\n"
			if file.content_type.startswith("text/plain"):
				membed.description = message + f"**File attached:** [{file.filename}]({file.url})"
				msg = await user.send(embed=membed)
				msg2 = await user.send("**Text file sent by Brain Juice Staff Team**",file=await file.to_file())
				membed.set_footer(text=f"Message ID: {msg.id}, File message ID: {msg2.id}")
				await ctx.send(embed=membed)
				await ctx.send("**Text file sent by Brain Juice Staff Team**",file=await file.to_file())
			else:
				membed.description = message + f"**Image attached:** [{file.filename}]({file.url})"
				membed.set_image(url=file.url)
				msg = await user.send(embed=membed)
				membed.set_footer(text=f"Message ID: {msg.id}")
				await ctx.send(embed=membed)
		else:
			msg = await user.send(embed=membed)
			membed.set_footer(text=f"Message ID: {msg.id}")
			await ctx.send(embed=membed)

		if self.bot.pending.get(user.id) is not None:
			self.bot.pending[user.id].cancel()
			del self.bot.pending[user.id]

			reopen = discord.Embed(title="Ticket reopened", description=f"Ticket reopened due to **{ctx.author}** sent a message to {user}", color=color.green())
			reopen.timestamp = datetime.now()
			reopen.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
			pin = await ctx.channel.send(embed=reopen)
			await pin.pin(reason="Ticket reopened")
			await ctx.channel.purge(limit=1)

			reopen = discord.Embed(title="Ticket reopened", description="Ticket reopened because one of our Staff Team member sent you a message", color=color.green())
			reopen.timestamp = datetime.now()

			await user.send(embed=reopen)

			log = discord.Embed(title="Ticket reopened",description=f"Ticket for **{user} ({user.id})** has been reopened due to {ctx.author} sent a message to {user}.\n[Click here to jump to the ticket]({pin.jump_url})", color=color.green())
			log.timestamp = datetime.now()

			await self.bot.botlogs.send(embed=log)

	@commands.command(aliases=['closeticket','ct'], description="Close the Ticket", usage="close")
	async def close(self, ctx, *, delay = "10m"):
		"""Close the Ticket"""
		if len(ctx.channel.name.split("-")[-1]) != 4 or ctx.channel.name.split("-")[-1].isdigit() == False or len(ctx.channel.name) <= 4 or ctx.channel.topic == None or not ctx.channel.name.startswith("ticket"):
			await ctx.send("This is not a Ticket!")
			return
		if not ctx.channel.topic == None:
			try:
				user = self.bot.get_user(int(ctx.channel.topic.split(" ")[-1]))
			except:
				await ctx.send("This is not a Ticket!")
				return

		try:
			delay = delay.lower()
		except:
			pass

		if user == None:
			await ctx.send("This user left the server, delete this ticket manually instead")
			return
		if self.bot.pending.get(user.id) is not None:
			await ctx.send("This Ticket is already scheduled to close")
			return

		if ctx.author.id != 615037304616255491 and ctx.channel.permissions_for(ctx.author).administrator == False and delay != "3h":
			pass
			# await ctx.send("You don't have the permission to customize closing time")
			# return

		delay = functions.conv(delay)
		if delay == "error":
			await ctx.send("Invalid schedule time, Example: 2d 4h 3m 6s")
			return
		timedelay = functions.time2text(delay)

		view = interaction.Confirm(ctx, ctx.author)
		view.message = await ctx.reply(f"Are you sure you want to close this ticket in **{timedelay}**?", view=view)

		await view.wait()
		if view.value == True:
			cl = discord.Embed(description=f"ticket closing in **{timedelay}**", color=color.red())
			cl.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
			cl.timestamp = datetime.now()
			cl.set_footer(text="Reply to the user to reopen the current ticket")
			pin = await ctx.send(embed=cl)
			await pin.pin(reason="Ticket scheduled to close")
			await ctx.channel.purge(limit=1)

			um = discord.Embed(description=f"This Ticket is scheduled to close in **{timedelay}**", color=color.red())
			um.set_author(name="Brain Juice", icon_url=self.bot.mainserver.icon.url)
			um.timestamp = datetime.now()
			um.set_footer(text="Send a message before this ticket closed to reopen the current ticket")

			await user.send(embed=um)

			log = discord.Embed(title="Ticket scheduled to close",description=f"Ticket for **{user} ({user.id})** was scheduled to close in **{timedelay}** by **{ctx.author}**", color=color.red())
			log.timestamp = datetime.now()

			await self.bot.botlogs.send(embed=log)

			self.bot.pending[user.id] = asyncio.create_task(self.bot.delete_channel(ctx, delay))

		elif view.value == False:
			await ctx.send(embed=discord.Embed(description="Cancelled.", color=color.red()))
		else:
			await ctx.send(f"{ctx.author.mention} You did not respond so it cancelled automatically.")

def setup(bot):
	bot.add_cog(TicketCog(bot))
