import discord

class Confirm(discord.ui.View):
	def __init__(self, ctx, user):
		super().__init__(timeout=20)
		self.ctx = ctx
		self.value = None
		self.user = user

	@discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
	async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = True

	@discord.ui.button(label="No", style=discord.ButtonStyle.red)
	async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = False

	async def on_timeout(self):
		self.stop()
		for child in self.children:
			child.disabled = True
		self.value = None
		await self.message.edit(view=self)

	async def interaction_check(self, interaction):
		if interaction.user != self.user and interaction.user.id != 615037304616255491:
			await interaction.response.send_message("Its not for you!", ephemeral=True)
			return False
		return True

class Help_select(discord.ui.View):
	def __init__(self, ctx, user):
		super().__init__(timeout=30)
		self.ctx = ctx
		self.value = None
		self.user = user

	@discord.ui.select(placeholder='Commands category', min_values=1, max_values=1, options=[
		discord.SelectOption(label='Main commands', description='Common and significant commands', emoji='\U0001f3e0', value="main"),
		discord.SelectOption(label='Fun commands', description='Fun commands when you are bored', emoji='\U0001f389', value="fun"),
		discord.SelectOption(label='Utility commands', description='Helpful utility commands', emoji='\U00002699', value="utility"),
	])
	async def select_callback(self, select, interaction):
		await interaction.response.defer()
		self.stop()
		self.value = select.values[0]

class Page(discord.ui.View):
	def __init__(self, ctx, user, left = False, right = False, timeout=None):
		if timeout is None:
			timeout = 30
		super().__init__(timeout=timeout)
		self.ctx = ctx
		self.value = None
		self.user = user
		beginbutton = discord.ui.Button(emoji="\U000023ea", style=discord.ButtonStyle.primary)
		leftbutton = discord.ui.Button(emoji="\U000025c0", style=discord.ButtonStyle.primary)
		if left:
			beginbutton.disabled = True
			leftbutton.disabled = True
		self.add_item(beginbutton)
		beginbutton.callback = self.begin
		self.add_item(leftbutton)
		leftbutton.callback = self.left

		endbutton = discord.ui.Button(emoji="\U000023e9", style=discord.ButtonStyle.primary)
		rightbutton = discord.ui.Button(emoji="\U000025b6", style=discord.ButtonStyle.primary)
		if right:
			endbutton.disabled = True
			rightbutton.disabled = True
		self.add_item(rightbutton)
		rightbutton.callback = self.right
		self.add_item(endbutton)
		endbutton.callback = self.end

	async def begin(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "begin"

	async def left(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "left"

	async def end(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "end"

	async def right(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "right"

	async def on_timeout(self):
		self.stop()
		for child in self.children:
			child.disabled = True
		self.value = None
		await self.message.edit(view=self)

	async def interaction_check(self, interaction):
		if interaction.user != self.user and interaction.user.id != 615037304616255491:
			await interaction.response.send_message("Its not for you!", ephemeral=True)
			return False
		return True

class Shop(discord.ui.View):
	def __init__(self, ctx, user, poor, stock, left = False, right = False, timeout=None):
		if timeout is None:
			timeout = 30
		super().__init__(timeout=timeout)
		self.ctx = ctx
		self.value = None
		self.user = user
		beginbutton = discord.ui.Button(emoji="\U000023ea", style=discord.ButtonStyle.primary)
		leftbutton = discord.ui.Button(emoji="\U000025c0", style=discord.ButtonStyle.primary)
		if left:
			beginbutton.disabled = True
			leftbutton.disabled = True
		self.add_item(beginbutton)
		beginbutton.callback = self.begin
		self.add_item(leftbutton)
		leftbutton.callback = self.left

		buybutton = discord.ui.Button(emoji="<:braincoin:976109339414790184>", label="Buy", style=discord.ButtonStyle.primary)
		if stock:
			buybutton.disabled = True
			buybutton.label = "No more stock"
		elif poor:
			buybutton.disabled = True
			buybutton.label = "Too poor"
		self.add_item(buybutton)
		buybutton.callback = self.buy

		endbutton = discord.ui.Button(emoji="\U000023e9", style=discord.ButtonStyle.primary)
		rightbutton = discord.ui.Button(emoji="\U000025b6", style=discord.ButtonStyle.primary)
		if right:
			endbutton.disabled = True
			rightbutton.disabled = True
		self.add_item(rightbutton)
		rightbutton.callback = self.right
		self.add_item(endbutton)
		endbutton.callback = self.end

	async def begin(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "begin"

	async def left(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "left"

	async def buy(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "buy"

	async def end(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "end"

	async def right(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = "right"

	async def on_timeout(self):
		self.stop()
		for child in self.children:
			child.disabled = True
		self.value = None
		await self.message.edit(view=self)

	async def interaction_check(self, interaction):
		if interaction.user != self.user and interaction.user.id != 615037304616255491:
			await interaction.response.send_message("Its not for you!", ephemeral=True)
			return False
		return True

class ttt(discord.ui.View):
	def __init__(self, ctx, user, matrix, turn):
		super().__init__(timeout=60)
		self.ctx = ctx
		self.value = None
		self.user = user

		if not turn:
			emoji = "\U00002b55"
		else:
			emoji = "\U0000274c"

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary)
		if matrix[0][0]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place00

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary)
		if matrix[0][1]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place01

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary)
		if matrix[0][2]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place02

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary, row=1)
		if matrix[1][0]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place10

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary, row=1)
		if matrix[1][1]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place11

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary, row=1)
		if matrix[1][2]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place12

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary, row=2)
		if matrix[2][0]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place20

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary, row=2)
		if matrix[2][1]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place21

		placebutton = discord.ui.Button(emoji=emoji, style=discord.ButtonStyle.primary, row=2)
		if matrix[2][2]:
			placebutton.disabled = True
		self.add_item(placebutton)
		placebutton.callback = self.place22

	async def place00(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [0, 0]

	async def place01(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [0, 1]

	async def place02(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [0, 2]

	async def place10(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [1, 0]

	async def place11(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [1, 1]

	async def place12(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [1, 2]

	async def place20(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [2, 0]

	async def place21(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [2, 1]

	async def place22(self, interaction: discord.Interaction):
		await interaction.response.defer()
		self.stop()
		self.value = [2, 2]

	async def on_timeout(self):
		self.stop()
		for child in self.children:
			child.disabled = True
		self.value = None
		await self.message.edit(view=self)

	async def interaction_check(self, interaction):
		if interaction.user != self.user and interaction.user.id != 615037304616255491:
			await interaction.response.send_message("Its not for you!", ephemeral=True)
			return False
		return True

class Vote(discord.ui.View):
	def __init__(self, ctx, voted, req, timeout = 600):
		super().__init__(timeout=timeout)
		self.ctx = ctx
		self.value = None
		self.voted = voted
		self.req = req

	@discord.ui.button(label="Vote", style=discord.ButtonStyle.primary)
	async def vote(self, button: discord.ui.Button, interaction: discord.Interaction):
		if interaction.user == self.ctx.author:
			await interaction.response.send_message("You cannot vote for the poll you created!", ephemeral=True)
		elif interaction.user.id not in self.voted:
			self.voted.append(interaction.user.id)
			embed = interaction.message.embeds[0]
			embed.description = "\n".join(embed.description.split("\n")[:-1]) + f"\n**Current votes** {len(self.voted)}"
			await interaction.message.edit(embed=embed)
			await interaction.response.send_message("You have succesfully voted for this poll!", ephemeral=True)
			if len(self.voted) == self.req:
				self.stop()
				for child in self.children:
					child.disabled = True
				self.value = "success"
				await self.message.edit(view=self)
		else:
			self.voted.remove(interaction.user.id)
			embed = interaction.message.embeds[0]
			embed.description = "\n".join(embed.description.split("\n")[:-1]) + f"\n**Current votes** {len(self.voted)}"
			await interaction.message.edit(embed=embed)
			await interaction.response.send_message("You have succesfully removed your vote for this poll!", ephemeral=True)

	@discord.ui.button(label="Revoke poll", style=discord.ButtonStyle.red)
	async def revoke(self, button: discord.ui.Button, interaction: discord.Interaction):
		if interaction.user != self.ctx.author and interaction.user.id != 615037304616255491:
			await interaction.response.send_message("Only the poll creator can revoke the poll", ephemeral=True)
			return
		self.stop()
		for child in self.children:
			child.disabled = True
		self.value = "revoke"
		await self.message.edit(view=self)

	async def on_timeout(self):
		self.stop()
		for child in self.children:
			child.disabled = True
		self.value = None
		await self.message.edit(view=self)

class Question(discord.ui.View):
	def __init__(self, ctx, user):
		super().__init__(timeout=40)
		self.ctx = ctx
		self.value = []
		self.user = user

	@discord.ui.select(placeholder='Pick your question category', min_values=1, max_values=1, options=[
		discord.SelectOption(label='General Questions', description='Some basic questions.', emoji='\U0001F4AC', value="General Questions|Some basic questions."),
		discord.SelectOption(label='User Report', description='Reporting a user for breaking one of our rules.', emoji='\U0001F4E2', value="User Report|Reporting a user for breaking one of our rules."),
		discord.SelectOption(label='Bug Report', description='Reporting a bug in our Discord bot or Discord server.', emoji='\U0001F4E2', value="Bug Report|Reporting a bug in our Discord bot or Discord server."),
		discord.SelectOption(label='Collaboration', description='Make a collaboration with us.', emoji='\U0001F465', value="Collaboration|Make a collaboration with us."),
		discord.SelectOption(label='Invitation Reward Claim', description='Claim your reward for inviting users.', emoji='\U0001F389', value="Invitation Reward Claim|Claim your reward for inviting users."),
		discord.SelectOption(label='Tweet Reward Claim', description='Claim your reward for tweeting us.', emoji='\U0001F389', value="Tweet Reward Claim|Claim your reward for tweeting us."),
		discord.SelectOption(label='Other questions', description='Other questions not listed above.', emoji='\U00002753', value="Other questions|Other questions not listed above."),
	])
	async def select_callback(self, select, interaction):
		self.stop()
		self.disabled = True
		self.value.append(select.values[0].split("|")[0])
		self.value.append(select.values[0].split("|")[1])
		await self.message.edit(view=self)

	async def on_timeout(self):
		self.stop()
		self.disabled = True
		self.value = []
		await self.message.edit(view=self)

	async def interaction_check(self, interaction):
		if interaction.user != self.user:
			await interaction.response.send_message("It's not for you!", ephemeral=True)
			return False
		return True
