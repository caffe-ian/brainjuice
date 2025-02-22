import discord
from discord.ext import commands, tasks
import asyncio
import random
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

discord.http.API_VERSION = 9
intents = discord.Intents.default()
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix="0219309", help_command=None, case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False, roles=True))
# bot2 = commands.Bot(command_prefix="0192018", help_command=None, case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False, roles=True))
color = discord.Colour

# @bot2.event
@bot.event
async def on_ready():
	# await bot2.wait_until_ready()
	print(f"Logged in as {bot.user}")
	# print(f"Logged in as {bot2.user}")
	post.start()

@tasks.loop(seconds=610)
async def post():
	# await bot.get_channel(823193298663505931).trigger_typing()
	# bot logs 947747400557154314
	# await bot.get_channel(700824631673618504).trigger_typing()
	# await asyncio.sleep(random.uniform(4, 6))
	# await bot.get_channel(700824631673618504).send("# Summoning indra in PS for payment\nI have god chalice, NLF: paw grav phoenix spider love quake") # <:magma:590579368754020361> <:light:590579368724791310> <:point_trade:1024068331604553810> <:quake:590579368774991884>
	# await bot.get_channel(1058389530064982077).trigger_typing()
	# await asyncio.sleep(random.uniform(4, 6))
	# await bot.get_channel(1058389530064982077).send("\U00000033\U0000FE0F\U000020E3<:dough:660245025032241172> <:point_trade:1024068331604553810> \U00002753\n\U00000033\U0000FE0F\U000020E3<:dough:660245025032241172> <:point_trade:1024068331604553810> \U00002753\n\U00000033\U0000FE0F\U000020E3<:dough:660245025032241172> <:point_trade:1024068331604553810> \U00002753")
	# await asyncio.sleep(120)
	await bot.get_channel(1179661848199581726).trigger_typing()
	await asyncio.sleep(random.uniform(4, 6))
	await bot.get_channel(1179661848199581726).send("1 - Trading Golden Huge Graffiti Raccoon for low tier huges (Accept underpaying)\n2 - Trading Golden Huge Graffiti Raccoon for low tier huges (Accept underpaying)\n3 - Trading Golden Huge Graffiti Raccoon for low tier huges (Accept underpaying)\n4 - Trading Golden Huge Graffiti Raccoon for low tier huges (Accept underpaying)\n5 - Trading Golden Huge Graffiti Raccoon for low tier huges (Accept underpaying)")
	# await bot.get_channel(1058389530064982077).send("\U00000032\U0000FE0F\U000020E3<:dragon:791565779766083585> \U00000033\U0000FE0F\U000020E3<:dough:660245025032241172> \U00000032\U0000FE0F\U000020E3<:spirit:1056978177945247754> \U00000032\U0000FE0F\U000020E3<:control:709260359370014722> \U00000032\U0000FE0F\U000020E3<:venom:886279018104619019> <:point_trade:1024068331604553810> ❓")
	# await bot.get_channel(1058389530064982077).send("<:dragon:791565779766083585> <:dough:660245025032241172> <:point_trade:1024068331604553810> <:capacity:1024354034242560000>\n<:dragon:791565779766083585> <:dough:660245025032241172> <:point_trade:1024068331604553810> <:capacity:1024354034242560000>\n<:dragon:791565779766083585> <:dough:660245025032241172> <:point_trade:1024068331604553810> <:capacity:1024354034242560000>")
# 	await bot.get_channel(823193298663505931).send("""**Brain Juice NFT**\nHello fellow Brainiacs! We are a DAO and we have the **BEST** features and utilities out of every other projects!
# https://www.youtube.com/watch?v=hpBKf4yvdyU&list=RDPn28OiY_aw0&index=12
# ✅ Phase-based
# ✅ DAO
# ✅ Safe Staking
# ✅ ARG
# ✅ Voting System
# ✅ Tokenomics
# ✅ P2E Soon
# More features and utilities at our website.

# Join the Brainiacs now!: https://discord.gg/CPYXNpbmVz

# https://media.discordapp.net/attachments/947707834123030578/983870264297263164/Brain_Juice_GIF.gif""")
	# await asyncio.sleep(random.uniform(1800, 1820))
	# # await bot2.get_channel(823193298663505931).trigger_typing()
	# await bot2.get_channel(943186714707501056).trigger_typing()
	# await asyncio.sleep(random.uniform(4, 6))
	# await bot2.get_channel(943186714707501056).send("> **\U000026A0 NFT DEVELOPMENT SERVICES \U000026A0**\n> Need a developer for your NFT project?\n> We provide a complete development service for your project!\n> \n> **Discord shilling \U0001F7E2 No upfront payment required \U0001F7E2**\n> We will advertise your NFT project in Discord channels 24/7\n> \n> **Website with any kind of utilities**\n> Dashboard, Minting, Blog, Updates, Voting, Breeding, DAO\n> Fully maintained, comes with weekly maintenance fee (Optional)\n> **Does not include hosting and domain name**\n> \n> **Smart contract**\n> Customizable with any utilites, whitelist etc\n> Low gas for cheap deployment (Optional)\n> \n> **Art generation**\n> Draw you anything in your favour and generate a combination of NFTs\n> \n> **Custom Discord bot**\n> Create a custom Discord bot that can do anything you desire, minigames, AI moderation, tokenomics\n> Logs your NFT collection activity from Opensea (Optional)\n\n> **Interested? Send a friend request to Chock#6302**")
# 	await bot2.get_channel(823193298663505931).send("""**Brain Juice NFT**\nHello fellow Brainiacs! We are a DAO and we have the **BEST** features and utilities out of every other projects!

# ✅ Phase-based
# ✅ DAO
# ✅ Safe Staking
# ✅ ARG
# ✅ Voting System
# ✅ Tokenomics
# ✅ P2E Soon
# More features and utilities at our website.

# Join the Brainiacs now!: https://discord.gg/CPYXNpbmVz

# https://media.discordapp.net/attachments/947707834123030578/983870264297263164/Brain_Juice_GIF.gif""")

loop = asyncio.get_event_loop()
loop.create_task(bot.start("***", bot=False))
# loop.create_task(bot2.start("***", bot=False))
loop.run_forever()