import discord
import web3
from db import db

cll = db['userdata']
pcll = db['polls-userdata']
ccll = db['credentials']

import os
from dotenv import load_dotenv

load_dotenv()

color = discord.Colour

w3 = web3.Web3(web3.HTTPProvider(os.getenv("PROVIDER")))
contract_address = os.getenv("CONTRACTADDRESS")
abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"uint256","name":"nc","type":"uint256"}],"name":"Cost","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"n","type":"uint256"}],"name":"Phase","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"b","type":"bool"}],"name":"Presale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"URI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"giveaway","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"nh","type":"string"}],"name":"hUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"hidden","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"mintAmount","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"nftsOwned","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"b","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"phase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"presale","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"root","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"nURI","type":"string"}],"name":"uri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"wCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"payee","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"nc","type":"uint256"}],"name":"wlCost","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"nr","type":"bytes32"}],"name":"wlRoot","outputs":[],"stateMutability":"nonpayable","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=abi)

async def is_linked(ctx):
	if (str(ctx.author.id) not in list((await ccll.find_one({"id": "discord_id"}))["data"].values())):
		embed = discord.Embed(title="Wait!", description="**This command requires linkage**\nPlease link your wallet address to your Discord before using any bot commands!", color=color.gold()).add_field(name="Steps", value="**1.** Proceed to our website **https://brainjuicenft.me**\n**2.** Connect your wallet on the top right corner\n**3.** Go to your dashboard on the top right corner\n**4.** Click **Link Discord**\n**5.** And you are done! Enjoy using the bot!")
		await ctx.reply(embed=embed)
		return False
	return True

def money(n):
	return str("{:,}".format(n))

def time2text(seconds):
	if seconds == None or seconds == "":
		return ""
	if seconds >= 60:
		minutes = seconds // 60
		seconds -= (minutes*60)
		if minutes >= 60:
			hours = minutes // 60
			minutes -= (hours*60)
			if hours >= 24:
				days = hours // 24
				hours -= (days*24)
				return f"{round(days)}d {round(hours)}h {round(minutes)}m {round(seconds, 1)}s"
			else:
				return f"{round(hours)}h {round(minutes)}m {round(seconds, 1)}s"
		else:
			return f"{round(minutes)}m {round(seconds, 1)}s"
	else:
		return str(round(seconds, 1))+"s"

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def conv(str):
	seconds = 0
	try:
		for s in str.split(" "):
			seconds += int(s[:-1]) * seconds_per_unit[s[-1].lower()]
		return seconds
	except:
		return "error"

async def finduser(id):
	return await cll.find_one({"id": id})

async def pcllfinduser(address):
	return await pcll.find_one({"address": address})

async def ccllfinddoc(id):
	return await ccll.find_one({"id": id})

async def updateset(id, key: str, value):
	return await cll.update_one({"id": id}, {"$set": {key: value}})

async def updateinc(id, key: str, value):
	return await cll.update_one({"id": id}, {"$inc": {key: value}})

async def insertdict(dic):
	return await cll.insert_one(dic)
