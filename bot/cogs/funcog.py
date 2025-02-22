import functions
import random
import discord
from discord.ext import commands
import asyncio
import time
import lists
import re
import interaction
import requests, lxml, json
from bs4 import BeautifulSoup
import math
lxml = lxml

color = discord.Colour

class FunCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Guess the number!", usage=".guess")
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def guess(self, ctx):
		await ctx.reply("Guess a number between 1-10! You have 3 chances")
		r = random.randint(1, 10)
		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel
		chances = 3
		while chances != 0:
			try:
				chances != 3 and await ctx.reply(f"You have {chances} {'chances' if chances > 1 else 'chance'} left!")
				chances -= 1
				msg = await self.bot.wait_for('message', check=check, timeout=30)
				if msg.content.isdigit() is False:
					await ctx.reply("It's not a number!")
					continue
				elif int(msg.content) < 1 or int(msg.content) > 10:
					await ctx.reply("You can only give numbers between 1-10!")
					continue

				if int(msg.content) == r:
					userp = await functions.finduser(ctx.author.id)
					rc = random.randint(3, 4)
					await ctx.reply(f"How lucky, you guessed the correct number {r} and earned <:braincoin:976109339414790184> {rc} BRC!")
					await functions.updateinc(ctx.author.id, "coin", rc)
					await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} + <:braincoin:976109339414790184> {functions.money(rc)} = <:braincoin:976109339414790184> {functions.money(userp['coin']+rc)} {ctx.message.jump_url}")
					return
				if chances:
					await ctx.reply("Higher!") if int(msg.content) < r else int(msg.content) > r and await ctx.reply("Smaller!")

			except asyncio.TimeoutError:
				await ctx.reply("You didn't respond, no prize 4 you")
				return
		await ctx.reply(f"No luck. The correct number is {r}, no prize 4 you")

	@commands.cooldown(1, 300, commands.BucketType.user)
	@commands.command(description=f"Guess the word!\nAvailable categories `{', '.join(lists.hangman_category)}`", usage=".hangman [category]")
	async def hangman(self, ctx, category = None):
		if category is None:
			category = random.choice(lists.hangman_category)
		else:
			try:
				category = [x for x in lists.hangman_category if x.lower().replace(" ", "") == category.lower().replace(" ", "") or category.lower().replace(" ", "") in x.lower().replace(" ", "")]
				category = category[0]
			except:
				await ctx.reply(f"Cannot find this category. You can only type one of these `{', '.join(lists.hangman_category)}`")
				return
		word = random.choice(lists.hangman_category_dispatcher[category]).replace("-", " ")
		guess = re.sub("[a-zA-Z]", "\_ ", word)
		chances = 6
		dispatcher = {6: "_____\n|	 |\n|\n|\n|\n|_______", 5: "_____\n|	 |\n|	 O\n|\n|\n|_______", 4: "_____\n|	 |\n|	 O\n|	 |\n|\n|_______", 3: "_____\n|	 |\n|	 O\n|	/|\n|\n|_______", 2: "_____\n|	 |\n|	 O\n|	/|\\\n|\n|_______", 1: "_____\n|	 |\n|	 O\n|	/|\\\n|	/\n|_______", 0: "_____\n|	 |\n|	 O\n|	/|\\\n|	/ \\\n|_______"}
		embed = discord.Embed(title="Hangman!", description=f"Guess the word!\n**Category** {category}\n**{guess.replace('	', ' ⠀')}**", color=color.blurple()).set_footer(text="Send letters one by one")
		embed.add_field(name="Chances", value=f"```\n{dispatcher[chances]}\n```")
		m = await ctx.reply(embed=embed)
		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel
		timeout = 30
		while chances:
			try:
				start = round(time.time())
				message = await self.bot.wait_for('message', check=check, timeout=timeout)
				msg = message.content
				if len(msg) > 1:
					await ctx.reply("Send letters one by one!")
					timeout -= (round(time.time())-start)
					timeout = 0 if timeout < 0 else timeout
					continue
				elif not msg.isalpha():
					await ctx.reply("Only ABC letters are allowed")
					timeout -= (round(time.time())-start)
					timeout = 0 if timeout < 0 else timeout
					continue

				if msg.lower() in list(guess.lower()):
					await ctx.reply("You already guessed this letter!")
					continue
				if msg.lower() in list(word.lower()):
					guess = guess.split(" ")
					guess = guess[:-1] if guess[-1] == "" else guess
					for i in [index.start() for index in re.finditer(msg.lower(), word.lower())]:
						guess[i] = list(word)[i]
					guess = " ".join(guess)
					await ctx.reply(f"The letter `{msg.lower()}` is right!", delete_after=5)
					await message.delete()
					embed.description = f"Guess the word!\n**Category** {category}\n**{guess.replace('	', ' ⠀')}**"
					await m.edit(embed=embed)
					if "_" not in list(guess.lower()):
						userp = await functions.finduser(ctx.author.id)
						rc = random.randint(8, 12)
						await ctx.reply(f"You guessed the word **{word}** and earned <:braincoin:976109339414790184> {rc} BRC!")
						await functions.updateinc(ctx.author.id, "coin", rc)
						await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} + <:braincoin:976109339414790184> {functions.money(rc)} = <:braincoin:976109339414790184> {functions.money(userp['coin']+rc)} {ctx.message.jump_url}")
						return
					continue
				chances -= 1
				await ctx.reply(f"The letter `{msg.lower()}` is incorrect!", delete_after=5)
				await message.delete()
				embed.set_field_at(0, name="Chances", value=f"```\n{dispatcher[chances]}\n```")
				await m.edit(embed=embed)
			except asyncio.TimeoutError:
				await ctx.reply("You didn't respond, no prize 4 you")
				return
		await ctx.reply(f"Too bad! You ran out of chances\nThe correct word is **{word}**!")

	@commands.cooldown(1, 20, commands.BucketType.user)
	@commands.command(aliases=["ttt"], description="Play Tic-Tac-Toe with an AI or another user", usage=".tictactoe", )
	async def tictactoe(self, ctx, user: discord.Member = None, bet = None):
		userp = await functions.finduser(ctx.author.id)
		if user is None:
			matrix = [[0,0,0], [0,0,0], [0,0,0]]
			turn = random.randint(0, 1)
			prerow, precol = [None, None]
			prematrix = None
			if turn == 0:
				embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
				embed.add_field(name=f"It's {ctx.author.name}'s turn!", value=await functions.tttdisplay(matrix))

				view = interaction.ttt(ctx, ctx.author, matrix, turn)
				view.message = msg = await ctx.reply(embed=embed, view=view)

			while True:
				if turn == 0:
					await view.wait()

					if view.value is None:
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
						embed.add_field(name=f"{ctx.author.name}'s did not respond", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed)
						await ctx.reply("You did not respond in time")
						return

					row, col = [view.value[0], view.value[1]]

					matrix[row][col] = 2

					if await functions.checkwin(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
						embed.add_field(name=f"{ctx.author.name} won the game!", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed, view=None)

						if prerow is not None or precol is not None or prematrix is not None:
							# Blacklist the previous AI move because the AI lost after that move
							try:
								lists.tttlose[repr(prematrix)].append([prerow, precol])
							except KeyError:
								lists.tttlose[repr(prematrix)] = [[prerow, precol]]

						return
					elif await functions.checktie(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
						embed.add_field(name=f"{ctx.author.name} and AI both tied!", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed, view=None)

						if prerow is not None and precol is not None and prematrix is not None:
							try:
								if [prerow, precol] not in lists.ttttie[repr(prematrix)] and [prerow, precol] not in lists.tttlose[repr(prematrix)]:
									lists.ttttie[repr(prematrix)].append([prerow, precol])
							except KeyError:
								lists.ttttie[repr(prematrix)] = [[prerow, precol]]

						return

					turn = 1

				elif turn == 1:
					embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
					embed.add_field(name="It's the AI's turn! Thinking...", value=await functions.tttdisplay(matrix))

					try:
						await msg.edit(embed=embed, view=None)
					except:
						msg = await ctx.send(embed=embed, view=None)

					await asyncio.sleep(2)

					if repr(matrix) in list(lists.tttwin):
						choices = []
						row, col = random.choice(lists.tttwin[repr(matrix)])
					else:
						# Provide all possible moves
						choices = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
						row, col = random.choice(choices)

					# While this block is occupied or will lead to lost or will lead to tie
					while matrix[row][col] != 0 or (repr(matrix) in list(lists.tttlose) and [row, col] in lists.tttlose[repr(matrix)]) or (repr(matrix) in list(lists.ttttie) and [row, col] in lists.ttttie[repr(matrix)]):
						# Remove this move from all possible moves
						choices.remove([row, col])
						# If no possible moves left
						if not len(choices):
							if prerow is not None and precol is not None and prematrix is not None:
								# Blacklist the previous move because no current move can prevent tying
								try:
									if [prerow, precol] not in lists.ttttie[repr(prematrix)]:
										lists.ttttie[repr(prematrix)].append([prerow, precol])
								except KeyError:
									lists.ttttie[repr(prematrix)] = [[prerow, precol]]
							# Provide all possible moves again
							choices = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
							row, col = random.choice(choices)
							# While this block is occupied or will lead to lost
							while matrix[row][col] != 0 or (repr(matrix) in list(lists.tttlose) and [row, col] in lists.tttlose[repr(matrix)]):
								# Remove this move from all possible moves
								choices.remove([row, col])
								# If no possible moves left
								if not len(choices):
									if prerow is not None and precol is not None and prematrix is not None:
										# Blacklist the previous move because no current move can prevent losing
										try:
											if [prerow, precol] not in lists.tttlose[repr(prematrix)]:
												lists.tttlose[repr(prematrix)].append([prerow, precol])
										except KeyError:
											lists.tttlose[repr(prematrix)] = [[prerow, precol]]
									# Provide all possible moves again
									choices = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
									row, col = random.choice(choices)
									# While this block is occupied
									while matrix[row][col] != 0:
										# Remove this move from all possible moves
										choices.remove([row, col])
										row, col = random.choice(choices)
									break
								else:
									row, col = random.choice(choices)
							break
						else:
							row, col = random.choice(choices)

					prerow, precol = [row, col]
					prematrix = __import__('copy').deepcopy(matrix) # Before AI place

					matrix[row][col] = 3

					if await functions.checkwin(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
						embed.add_field(name="AI won the game! Too bad 4 you", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed, view=None)

						try:
							if [prerow, precol] not in lists.tttwin[repr(prematrix)]:
								lists.tttwin[repr(prematrix)].append([prerow, precol])
						except KeyError:
							lists.tttwin[repr(prematrix)] = [[prerow, precol]]

						return
					elif await functions.checktie(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
						embed.add_field(name=f"{ctx.author.name} and AI both tied!", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed, view=None)

						try:
							if [prerow, precol] not in lists.ttttie[repr(prematrix)] and [prerow, precol] not in lists.tttlose[repr(prematrix)]:
								lists.ttttie[repr(prematrix)].append([prerow, precol])
						except KeyError:
							lists.ttttie[repr(prematrix)] = [[prerow, precol]]

						return

					turn = 0

					embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs AI", color=color.embed_background())
					embed.add_field(name=f"It's {ctx.author.name}'s turn!", value=await functions.tttdisplay(matrix))

					view = interaction.ttt(ctx, ctx.author, matrix, turn)
					view.message = await msg.edit(embed=embed, view=view)

		elif user is not None:
			user2 = await functions.finduser(user.id)
			if user2 is None:
				await ctx.send("This user haven't start playing yet!")
				return
			if bet is not None:
				if bet < 1:
					await ctx.send("You must bet at least <:braincoin:976109339414790184> 1 BRC")
					return
				if userp['coin'] < bet:
					await ctx.send("You don't even have that much coin")
					return
				elif user2['coin'] < bet:
					await ctx.send("The user is too poor to afford the bet")
					return
				try:
					functions.ac(bet)
				except:
					try:
						bet = int(bet)
					except:
						await ctx.send("You have to give a number!")
						return

			view = interaction.Confirm(ctx, user)
			if bet is None:
				view.message = msg = await ctx.send(f"{user.mention}, {ctx.author.name} challenged you to a Tic-Tac-Toe game!\nDo you want to accept it?", view=view)
			else:
				view.message = msg = await ctx.send(f"{user.mention}, {ctx.author.name} challenged you to a <:braincoin:976109339414790184> {bet} BRC Tic-Tac-Toe game!\nDo you want to accept it?", view=view)

			await view.wait()
			if view.value is None:
				await ctx.reply(f"{user.name} ignored you")
				return
			elif view.value is False:
				await ctx.reply(f"{user.name} is too afraid to accept your challenge")
				return

			if bet is not None:
				await functions.updateinc(ctx.author.id, 'coin', -bet)
				await functions.updateinc(user.id, 'coin', -bet)
				await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sub) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} - <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(userp['coin']-bet)} {ctx.message.jump_url}")
				await self.bot.get_channel(977556272666787860).send(f"{user} ({user.id} sub) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user2['coin'])} - <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user2['coin']-bet)} {ctx.message.jump_url}")

			matrix = [[0,0,0], [0,0,0], [0,0,0]]
			turn = random.randint(0, 1)

			if turn == 0:
				embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
				embed.add_field(name=f"It's {ctx.author.name}'s turn!", value=await functions.tttdisplay(matrix))

				view = interaction.ttt(ctx, ctx.author, matrix, turn)
				view.message = await msg.edit(embed=embed, view=view)
			elif turn == 1:
				embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
				embed.add_field(name=f"It's {user.name}'s turn!", value=await functions.tttdisplay(matrix))

				view = interaction.ttt(ctx, ctx.author, matrix, turn)
				view.message = await msg.edit(embed=embed, view=view)

			while True:
				if turn == 0:
					await view.wait()

					if view.value is None:
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
						if bet is not None:
							embed.add_field(name=f"{ctx.author.name}'s did not respond so {user.name} won <:braincoin:976109339414790184> {bet} BRC", value=await functions.tttdisplay(matrix))
							await functions.updateinc(user.id, 'coin', round(bet*2))
							await self.bot.get_channel(977556272666787860).send(f"{user} ({user.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user2['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user2['coin']+bet)} {ctx.message.jump_url}")
						else:
							embed.add_field(name=f"{ctx.author.name}'s did not respond so {user.name} won", value=await functions.tttdisplay(matrix))
						await msg.edit(embed=embed)
						await ctx.reply(f"{ctx.author.mention} You did not respond in time")
						return

					row, col = [view.value[0], view.value[1]]

					matrix[row][col] = 2

					if await functions.checkwin(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
						if bet is None:
							embed.add_field(name=f"{ctx.author.name} won the game!", value=await functions.tttdisplay(matrix))
						else:
							embed.add_field(name=f"{ctx.author.name} won the game and earned <:braincoin:976109339414790184> {bet} BRC!", value=await functions.tttdisplay(matrix))
							await functions.updateinc(ctx.author.id, 'coin', round(bet*2))
							await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(userp['coin']+bet)} {ctx.message.jump_url}")

						await msg.edit(embed=embed, view=None)

						return
					elif await functions.checktie(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
						embed.add_field(name=f"{ctx.author.name} and {user.name} both tied!", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed, view=None)

						if bet is not None:
							await functions.updateinc(ctx.author.id, 'coin', bet)
							await functions.updateinc(user.id, 'coin', bet)
							await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(userp['coin']+bet)} {ctx.message.jump_url}")
							await self.bot.get_channel(977556272666787860).send(f"{user} ({user.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user2['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user2['coin']+bet)} {ctx.message.jump_url}")

						return

					turn = 1

					embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
					embed.add_field(name=f"It's {user.name}'s turn!", value=await functions.tttdisplay(matrix))

					view = interaction.ttt(ctx, ctx.author, matrix, turn)
					view.message = await msg.edit(embed=embed, view=view)

				elif turn == 1:
					await view.wait()

					if view.value is None:
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
						if bet is not None:
							embed.add_field(name=f"{user.name}'s did not respond so {ctx.author.name} won <:braincoin:976109339414790184> {bet} BRC", value=await functions.tttdisplay(matrix))
							await functions.updateinc(ctx.author.id, 'coin', round(bet*2))
							await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(userp['coin']+bet)} {ctx.message.jump_url}")
						else:
							embed.add_field(name=f"{user.name}'s did not respond so {ctx.author.name} won", value=await functions.tttdisplay(matrix))
						await msg.edit(embed=embed)
						await ctx.reply(f"{user.mention} You did not respond in time")
						return

					row, col = [view.value[0], view.value[1]]

					matrix[row][col] = 3

					if await functions.checkwin(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
						if bet is None:
							embed.add_field(name=f"{user.name} won the game!", value=await functions.tttdisplay(matrix))
						else:
							embed.add_field(name=f"{user.name} won the game and earned <:braincoin:976109339414790184> {bet} BRC!", value=await functions.tttdisplay(matrix))
							await functions.updateinc(user.id, 'coin', round(bet*2))
							await self.bot.get_channel(977556272666787860).send(f"{user} ({user.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user2['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user2['coin']+bet)} {ctx.message.jump_url}")

						await msg.edit(embed=embed, view=None)

						return
					elif await functions.checktie(matrix):
						embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
						embed.add_field(name=f"{ctx.author.name} and {user.name} both tied!", value=await functions.tttdisplay(matrix))

						await msg.edit(embed=embed, view=None)

						if bet is not None:
							await functions.updateinc(ctx.author.id, 'coin', bet)
							await functions.updateinc(user.id, 'coin', bet)
							await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(userp['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(userp['coin']+bet)} {ctx.message.jump_url}")
							await self.bot.get_channel(977556272666787860).send(f"{user} ({user.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user2['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user2['coin']+bet)} {ctx.message.jump_url}")
						return

					turn = 0

					embed = discord.Embed(title="Tic Tac Toe", description=f"{ctx.author.name} vs {user.name}", color=color.embed_background())
					embed.add_field(name=f"It's {ctx.author.name}'s turn!", value=await functions.tttdisplay(matrix))

					view = interaction.ttt(ctx, ctx.author, matrix, turn)
					view.message = await msg.edit(embed=embed, view=view)

	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command(description="Find the definition of a word", usage=".define <word>")
	async def define(self, ctx, *, query: str = None):
		if query is None:
			await ctx.send("Provide a word to define!")
			return
		r = requests.get(f"https://www.google.com/search?q=define+{query.replace(' ', '+')}", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/91.0.864.59"})
		soup = BeautifulSoup(r.text, 'lxml')
		word = soup.find('span', {"data-dobid": "hdw"})
		if not word:
			embed = discord.Embed(title=f"Definition for {query}", description=f"Hmmm, couldn't find a definition for this word `{query}`", color=color.red()).set_footer(text="Powered by Google\nDefinitions from Oxford Languages")
			await ctx.send(embed=embed)
			return
		embed = discord.Embed(title=f"Definition for {query}", description=f"**{word.text}**", color=color.blurple()).set_footer(text="Powered by Google\nDefinitions from Oxford Languages")
		i = 0
		for parts_of_speech in soup.find_all('div', {"jsname": "r5Nvmf"}):
			if parts_of_speech.find('span', {'class': 'YrbPuc'}) is None:
				break
			embed.add_field(name=parts_of_speech.find('span', {'class': 'YrbPuc'}).text, value="", inline=False)
			index = 1
			for definitions in parts_of_speech.find_all("li", {"jsname": "gskXhf"}):
				for definition in definitions.find_all("div", {"data-dobid": "dfn"}):
					embed._fields[i]['value'] += f"**{index}.** {definition.span.text}\n"
					index += 1
				for example in definitions.find_all("div", {"class": "ubHt5c"}):
					embed._fields[i]['value'] += f"**Example** {example.text}\n"
				embed._fields[i]['value'] += "\n"
			i += 1
		html = requests.get(f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/91.0.864.59"})
		soup = BeautifulSoup(html.text, 'lxml')
		all_script_tags = soup.select('script')
		matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
		matched_images_data_fix = json.dumps(matched_images_data)
		matched_images_data_json = json.loads(matched_images_data_fix)
		matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)
		removed_matched_google_images_thumbnails = re.sub(
				r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '', str(matched_google_image_data))
		matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)
		img_link = []
		for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
			original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
			if not bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape').endswith(".svg"):
				img_link.append(bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape'))
		page = 1
		embed.set_image(url=img_link[page-1])
		view = interaction.Page(ctx, ctx.author, True, False)
		view.message = msg = await ctx.send(embed=embed, view=view)
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
			elif view.value	== "end":
				page = len(img_link)
			embed.set_image(url=img_link[page-1])
			view = interaction.Page(ctx, ctx.author, page == 1, page == len(img_link))
			view.message = await msg.edit(embed=embed, view=view)

	@commands.command(aliases=['russianroulette', 'rr'], description="Play Russian roulette with another user", usage=".roulette <user> <bet>")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def roulette(self, ctx, user2: discord.Member = None, bet = None):
		if user2 == None:
			await ctx.reply("Who do you want to play with?")
			ctx.command.reset_cooldown(ctx)
			return
		if bet == None:
			await ctx.reply("You have to give a bet!")
			ctx.command.reset_cooldown(ctx)
			return
		try:
			bet = int(bet)
		except:
			if not bet == 'max':
				await ctx.reply("Give a valid amount of bet!")
				ctx.command.reset_cooldown(ctx)
				return
			pass
		user = await functions.finduser(ctx.author.id)
		usercoin = user['coin']
		try:
			if bet.lower() == 'max':
				bet = math.floor(usercoin)
			if bet > 5000:
				bet = 5000
		except:
			pass
		target = await functions.finduser(user2.id)
		if bet <= 0:
			await ctx.reply("You must bet at least <:braincoin:976109339414790184> 1 BRC")
			ctx.command.reset_cooldown(ctx)
			return
		elif usercoin < bet:
			await ctx.reply("You don't even have enough coin poor guy")
			ctx.command.reset_cooldown(ctx)
			return
		elif target['coin'] < bet:
			await ctx.reply("The user doesn't even have enough coin to play with you")
			ctx.command.reset_cooldown(ctx)
			return

		view = interaction.Confirm(ctx, ctx.author)
		view.message = await ctx.reply(f"{user2.mention} challenged you to a <:braincoin:976109339414790184> {bet} BRC Russian roulette game!", view=view)

		await view.wait()

		if view.value is None:
			await ctx.reply(f"{user2.name} ignored you")
			ctx.command.reset_cooldown(ctx)
			return
		elif view.value is False:
			await ctx.reply(f"{user2.name} is too afraid to accept your challenge")
			ctx.command.reset_cooldown(ctx)
			return

		await functions.updateinc(user2.id, 'coin', -bet)
		await functions.updateinc(ctx.author.id, 'coin', -bet)
		await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sub) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user['coin'])} - <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user['coin']-bet)} {ctx.message.jump_url}")
		await self.bot.get_channel(977556272666787860).send(f"{user2} ({user2.id} sub) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(target['coin'])} - <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(target['coin']-bet)} {ctx.message.jump_url}")

		msg = await ctx.reply(f"Russian Roulette battle {ctx.author.name} against {user2.name} is starting!")
		bullet = 0
		while True:
			bullet += 1
			await asyncio.sleep(2)
			await msg.edit(content=f"{ctx.author.name} loaded {bullet} bullet into the revolver")
			randomchance = random.randint(1,6)
			randomchance2 = random.random()
			if bullet == 6:
				if randomchance2 <= 0.05:
					await functions.updateinc(ctx.author.id, 'coin', round(bet))
					await asyncio.sleep(2)
					await msg.edit(content=f"{ctx.author.name} pulled the trigger but the gun jammed! {ctx.author.name} won <:braincoin:976109339414790184> {bet} BRC against {user2.name}!")
					await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user['coin']+bet)} {ctx.message.jump_url}")
					return
			if randomchance <= bullet:
				await functions.updateinc(user2.id, 'coin', round(bet))
				await asyncio.sleep(2)
				await msg.edit(content=f"{ctx.author.name} pulled the trigger and BANG! {ctx.author.name} lost <:braincoin:976109339414790184> {bet} BRC against {user2.name}")
				await self.bot.get_channel(977556272666787860).send(f"{user2} ({user2.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(target['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(target['coin']+bet)} {ctx.message.jump_url}")
				return
			else:
				await asyncio.sleep(2)
				await msg.edit(content=f"{ctx.author.name} pulled the trigger and nothing happens! Its now {user2.name}'s turn")

			bullet += 1
			await asyncio.sleep(2)
			await msg.edit(content=f"{user2.name} loaded {bullet} bullet into the revolver")
			randomchance = random.randint(1,6)
			randomchance2 = random.random()
			if bullet == 6:
				if randomchance2 <= 0.05:
					await functions.updateinc(user2.id, 'coin', round(bet))
					await asyncio.sleep(2)
					await msg.edit(content=f"{user2.name} pulled the trigger but the gun jammed! {user2.name} won <:braincoin:976109339414790184> {bet} BRC against {ctx.author.name}!")
					await self.bot.get_channel(977556272666787860).send(f"{user2} ({user2.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(target['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(target['coin']+bet)} {ctx.message.jump_url}")
					return
			if randomchance <= bullet:
				await functions.updateinc(ctx.author.id, 'coin', round(bet))
				await asyncio.sleep(2)
				await msg.edit(content=f"{user2.name} pulled the trigger and BANG! {user2.name} lost <:braincoin:976109339414790184> {bet} BRC against {ctx.author.name}")
				await self.bot.get_channel(977556272666787860).send(f"{ctx.author} ({ctx.author.id} sum) used `{ctx.command}` command: <:braincoin:976109339414790184> {functions.money(user['coin'])} + <:braincoin:976109339414790184> {functions.money(bet)} = <:braincoin:976109339414790184> {functions.money(user['coin']+bet)} {ctx.message.jump_url}")
				return
			else:
				await asyncio.sleep(2)
				await msg.edit(content=f"{user2.name} pulled the trigger and nothing happens! Its now {ctx.author.name}'s turn")

	@commands.command(description="Snipe the latest deleted message in the current channel", usage=".snipe")
	@commands.cooldown(1, 10)
	async def snipe(self, ctx):
		message = self.bot.snipe[ctx.channel.id]
		embed = discord.Embed(title="Latest message deleted in this channel", description=f"Sent by {message['mention']}", color=color.random()).add_field(name="Message content", value=message['content'].replace('https://', '').replace('http://', '')).set_thumbnail(url=message['avatar'])
		embed.timestamp = message["created_at"]

		if "attachment_proxy_url" in list(message.keys()):
			embed.add_field(name="Message attachment", value=message["attachment_filename"])
			if message["attachment_proxy_url"] != "":
				if message["attachment_proxy_url"].endswith(".png") or message["attachment_proxy_url"].endswith(".jpg") or message["attachment_proxy_url"].endswith(".jpeg") or message["attachment_proxy_url"].endswith(".gif"):
					embed.set_image(url=message["attachment_proxy_url"])

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(FunCog(bot))