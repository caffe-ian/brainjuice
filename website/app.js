require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const Web3 = require('web3');
const crypto = require("crypto");
const bodyParser = require('body-parser');
const fetch = require('node-fetch');
const https = require('https');
const fs = require('fs');
const mongoose = require('mongoose');
const Poll = require('./poll');
const Polluserdata = require('./poll-userdata');
const Cred = require('./credentials');
const { MerkleTree } = require('merkletreejs');
const keccak256 = require('keccak256');

const dbURI = "mongodb+srv://qnjstudio:qnjstudio123@main.hi4w6.mongodb.net/maindb?retryWrites=true&w=majority";
const provider = "https://rinkeby.infura.io/v3/0194fd40b77a4f03a28c0adcdc9a4d8b";
const web3 = new Web3(new Web3.providers.HttpProvider(provider));
const ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"uint256","name":"nc","type":"uint256"}],"name":"Cost","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"n","type":"uint256"}],"name":"Phase","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"b","type":"bool"}],"name":"Presale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"URI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"giveaway","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"nh","type":"string"}],"name":"hUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"hidden","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"mintAmount","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"nftsOwned","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"b","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"phase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"presale","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"root","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"nURI","type":"string"}],"name":"uri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"wCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"payee","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"nc","type":"uint256"}],"name":"wlCost","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"nr","type":"bytes32"}],"name":"wlRoot","outputs":[],"stateMutability":"nonpayable","type":"function"}]
const contract_address = "0x0Affc84d65D07843882517031cc7E4709E085a5C";
const contract = new web3.eth.Contract(ABI, contract_address);
const whitelistAddresses = fs.readFileSync("./whitelisted.txt", "utf-8").replaceAll("\r", "").split("\n");
const tree = whitelistAddresses.map(addr => keccak256(addr));
const merkleTree = new MerkleTree(tree, keccak256, {sortPairs: true});
const discordauthurl = "https://discord.com/api/oauth2/authorize?client_id=964802962432098305&redirect_uri=https%3A%2F%2Flocalhost%3A3000%2Fcreate-poll&response_type=code&scope=identify";
const report_webhook = "https://discord.com/api/webhooks/965617905989464124/WfUbq5O9l6mGq87c2UsX7n35DVaamEWF377B8nFJVaLc8JzlTFe836Cuwnto8ufcYYG3";
const poll_webhook = "https://discord.com/api/webhooks/966865002441105428/2ssq119MMQBlqLGFxASkjdAMd0mnvtjs67Kg_LYtQ63hcVT1qkHvmJblESTWDGBLfZl4";
const withdraw_webhook = "https://discord.com/api/webhooks/966867283781779498/HmGh36-S5MlgwgOeC98x2pfwbwLyY7ZokJsviY4GKa7AlrYoUv8yRJk5T8yyhopHAc5H";
const owner_addresses = ["0x1e24f8c50af5C0f5C1df6EcA7cc4982E73a97ca0"];
var owner;
var temp_nonce = {};

const app = express(); // Our App
const port = process.env.PORT || 3000;

app.set('view engine', 'ejs');

// const options = {
//   key: fs.readFileSync('./localhost-key.pem'),
//   cert: fs.readFileSync('./localhost.pem'),
// };

mongoose.connect(dbURI, {useNewUrlParser: true, useUnifiedTopology: true})
	.then(async (result) => {
		console.log("Connected to database");
		owner = (await Cred.findOne({"id": "misc"})).data.owner;
		web3.eth.accounts.wallet.add(owner);
		owner = web3.eth.accounts.wallet[0].address;
		// https.createServer(options, app).listen(port, () => {
		// 	console.log("Connected to server");
		// });
		app.listen(port, () => {
		  console.log('Connected to server');
		})
	})
	.catch((err) => {
		console.log("Cannot connect to database:", err);
	});

const errors = ["Minting is still not available yet!", "Oops! Seems like it's out of stock!", "Not enough funds!", "You are not whitelisted! Wait for public mint", "Token ID doesn't exist!", "Amount must be more than 0!", "You are not the owner of this NFT!", "Address 0", "This token is already minted!"];

function getErrorMessage(err) {
	try {
		err = errors[parseInt(err.message.split("execution reverted: ")[1])];
		return err;
	} catch {
		return "Error..";
	}
}

app.use(express.static(__dirname/*, {
 maxAge: 86400000 * 30
}*/));
app.use(helmet.frameguard({ action: 'DENY' }));
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

process.on('uncaughtException', (err) => {
  console.log("Fatal Error:", err);
});

app.get('/', (request, response) => {
	response.render('index');
});

app.post('/dope', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	if ((await Cred.findOne({"id": "blacklist"})).data.includes(request.body.address)) {
		response.send("You are blacklisted! Too bad, you can't vote");
		return;
	}
	if (Object.values(request.body).includes(undefined) || Object.values(request.body).includes(null)) {
		response.send("Invalid values");
		return;
	}
	let id = parseInt(request.body.id);
	if (typeof id !== 'number') {
		response.send("Invalid ID");
		return;
	}
	let discord_id = request.body.discord_id;
	let type = request.body.type;
	let cost;
	try {
		if (request.body.type.startsWith("Fund request ")) {
			let v;
			await contract.methods.balanceOf(request.body.address).call((error, result) => {
				if (error || result == 0) {
			    response.send("You have to own at least one Brain Juice's for upvoting fund request polls!");
			    return;
			  } else {
			  	v = true;
			  }
			});
			if (v != true) {
				return;
			}
			cost = parseFloat(type.split("Fund request ")[1].split(" ETH")[0]);
			type = type.split(' ').slice(0,2).join(' ');
		} else {
			if (!["Suggestion", "Decision"].includes(request.body.type)) {
				response.send("Invalid type");
				return;
			}
			cost = 0;
		}
	} catch(err) {
		response.send("Invalid type");
		return;
	}
	if (cost == undefined || cost == null) {
		response.send("Invalid cost");
		return;
	} else if (cost !== 0 && cost < 0.01) {
		response.send("Cost cannot be lesser than 0.01 ETH");
		return;
	} else if (cost > 1) {
		response.send("Cost cannot be more than 1 ETH");
		return;
	} else if (Math.floor(cost) !== cost && cost.toString().split(".")[1].length > 3) {
		response.send("Cost can only have 3 decimals, e.g. 0.015");
		return;
	}
	let title = request.body.title;
	let description = request.body.description;
	let dope = parseInt(request.body.dope);
	let nope = parseInt(request.body.nope);
	let poll = await Poll.findOne({"discarded": false, id: id});
	if (poll == null) {
		response.send("Invalid ID");
		return;
	} else if (Math.floor(Date.now() / 1000) >= poll.createdAt + 259200) {
		response.send("This poll has expired!")
		return;
	} else if (discord_id !== poll.discord_id) {
		response.send("Invalid Discord ID");
		return;
	} else if (type !== poll.type) {
		response.send("Invalid type");
		return;
	} else if (cost !== poll.cost) {
		response.send("Invalid cost");
		return;
	} else if (description !== poll.description) {
		response.send("Invalid description");
		return;
	} else if (dope !== poll.dope) {
		response.send("Invalid dope count");
		return;
	} else if (nope !== poll.nope) {
		response.send("Invalid nope count");
		return;
	}
	let user = await Polluserdata.findOne({address: request.body.address});
	if (user == null) {
		let userdata = new Polluserdata({
			address: request.body.address,
			upvoted: [],
			downvoted: []
		});
		await userdata.save()
			.catch((err) => {
				console.log("Error saving userdata:", err);
				response.send("Unable to vote...");
				return;
			});
		user = await Polluserdata.findOne({address: request.body.address});
	}

	if (user.upvoted.includes(id)) {
		await Polluserdata.updateOne({address: request.body.address}, { $pull: { upvoted: id }});
		await Poll.updateOne({"discarded": false, id: id}, {$inc : {dope : -1}})
			.catch((err) => {
				response.send("Failed to unupvote the poll!");
				return;
			});
		response.send("-1");
		return;
	} else if (user.downvoted.includes(id)) {
		await Polluserdata.updateOne({address: request.body.address}, { $pull: { downvoted: id }, $addToSet: { upvoted: id }});
		await Poll.updateOne({"discarded": false, id: id}, {$inc : {dope : 1, nope: -1}})
			.catch((err) => {
				response.send("Failed to upvote the poll!");
				return;
			});
		response.send("0");
		return;
	} else {
		await Polluserdata.updateOne({address: request.body.address}, { $addToSet: { upvoted: id }});
		await Poll.updateOne({"discarded": false, id: id}, {$inc : {dope : 1}})
			.catch((err) => {
				response.send("Failed to upvote the poll!");
				return;
			});
		response.send("1");
		return;
	}
});

app.post('/nope', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	if ((await Cred.findOne({"id": "blacklist"})).data.includes(request.body.address)) {
		response.send("You are blacklisted! Too bad, you can't vote");
		return;
	}
	if (Object.values(request.body).includes(undefined) || Object.values(request.body).includes(null)) {
		response.send("Invalid values");
		return;
	}
	let id = parseInt(request.body.id);
	if (typeof id !== 'number') {
		response.send("Invalid ID");
		return;
	}
	let discord_id = request.body.discord_id;
	let type = request.body.type;
	let cost;
	try {
		if (request.body.type.startsWith("Fund request ")) {
			let v;
			await contract.methods.balanceOf(request.body.address).call((error, result) => {
				if (error || result == 0) {
			    response.send("You have to own at least one Brain Juice's for downvoting fund request polls!");
			    return;
			  } else {
			  	v = true;
			  }
			});
			if (v != true) {
				return;
			}
			cost = parseFloat(type.split("Fund request ")[1].split(" ETH")[0]);
			type = type.split(' ').slice(0,2).join(' ');
		} else {
			if (!["Suggestion", "Decision"].includes(request.body.type)) {
				response.send("Invalid type");
				return;
			}
			cost = 0;
		}
	} catch(err) {
		response.send("Invalid type");
		return;
	}
	if (cost == undefined || cost == null) {
		response.send("Invalid cost");
		return;
	} else if (cost !== 0 && cost < 0.01) {
		response.send("Cost cannot be lesser than 0.01 ETH");
		return;
	} else if (cost > 1) {
		response.send("Cost cannot be more than 1 ETH");
		return;
	} else if (Math.floor(cost) !== cost && cost.toString().split(".")[1].length > 3) {
		response.send("Cost can only have 3 decimals, e.g. 0.015");
		return;
	}
	let title = request.body.title;
	let description = request.body.description;
	let dope = parseInt(request.body.dope);
	let nope = parseInt(request.body.nope);
	let poll = await Poll.findOne({"discarded": false, id: id});
	if (poll == null) {
		response.send("Invalid ID");
		return;
	} else if (Math.floor(Date.now() / 1000) >= poll.createdAt + 259200) {
		response.send("This poll has expired!")
		return;
	} else if (discord_id !== poll.discord_id) {
		response.send("Invalid Discord ID");
		return;
	} else if (type !== poll.type) {
		response.send("Invalid type");
		return;
	} else if (cost !== poll.cost) {
		response.send("Invalid cost");
		return;
	} else if (description !== poll.description) {
		response.send("Invalid description");
		return;
	} else if (dope !== poll.dope) {
		response.send("Invalid dope count");
		return;
	} else if (nope !== poll.nope) {
		response.send("Invalid nope count");
		return;
	}
	let user = await Polluserdata.findOne({address: request.body.address});
	if (user == null) {
		let userdata = new Polluserdata({
			address: request.body.address,
			upvoted: [],
			downvoted: []
		});
		await userdata.save()
			.catch((err) => {
				console.log("Error saving userdata:", err);
				response.send("Unable to vote...");
				return;
			});
		user = await Polluserdata.findOne({address: request.body.address});
	}

	if (user.downvoted.includes(id)) {
		await Polluserdata.updateOne({address: request.body.address}, { $pull: { downvoted: id }});
		await Poll.updateOne({"discarded": false, id: id}, {$inc : {nope : -1}})
			.catch((err) => {
				response.send("Failed to undownvote the poll!");
				return;
			});
		response.send("-1");
		return;
	} else if (user.upvoted.includes(id)) {
		await Polluserdata.updateOne({address: request.body.address}, { $pull: { upvoted: id }, $addToSet: { downvoted: id }});
		await Poll.updateOne({"discarded": false, id: id}, {$inc : {nope : 1, dope: -1}})
			.catch((err) => {
				response.send("Failed to downvote the poll!");
				return;
			});
		response.send("0");
		return;
	} else {
		await Polluserdata.updateOne({address: request.body.address}, { $addToSet: { downvoted: id }});
		await Poll.updateOne({"discarded": false, id: id}, {$inc : {nope : 1}})
			.catch((err) => {
				response.send("Failed to downvote the poll!");
				return;
			});
		response.send("1");
		return;
	}
});

app.post('/poll', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	if ((await Cred.findOne({"id": "blacklist"})).data.includes(request.body.address)) {
		response.send("You are blacklisted! Too bad, you can't create polls");
		return;
	}
	let discord_id = (await Cred.findOne({"id": "discord_id"})).data[request.body.address];
	if (discord_id == '' || discord_id == undefined || discord_id == null) {
		response.send("You are not authenticated by Discord, try refreshing the page!");
		return;
	}
	if ((await Poll.findOne({"discarded": false, "address": request.body.address, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}})) != null) {
		response.send("You have already created a poll in the past 3 days! Wait for the poll to expire or discard it");
		return;
	}
	let type = request.body.type;
	let cost;
	try {
		if (request.body.type.startsWith("Fund request ")) {
			let v;
			await contract.methods.balanceOf(request.body.address).call((error, result) => {
				if (error || result == 0) {
			    response.send("You have to own at least one Brain Juice's for fund requesting!");
			    return;
			  } else {
			  	v = true;
			  }
			});
			if (v != true) {
				return;
			}
			cost = parseFloat(type.split("Fund request ")[1].split(" ETH")[0]);
			type = type.split(' ').slice(0,2).join(' ');
			if (cost == NaN) {
				response.send("Invalid cost");
				return;
			}
		} else {
			if (!["Suggestion", "Decision"].includes(request.body.type)) {
				response.send("Invalid type");
				return;
			}
			cost = 0;
		}
	} catch(err) {
		response.send("Invalid type");
		return;
	}
	if (cost == undefined || cost == null) {
		response.send("Invalid cost");
		return;
	} else if (cost !== 0 && cost < 0.01) {
		response.send("Cost cannot be lesser than 0.01 ETH");
		return;
	} else if (cost > 1) {
		response.send("Cost cannot be more than 1 ETH");
		return;
	} else if (Math.floor(cost) !== cost && cost.toString().split(".")[1].length > 3) {
		response.send("Cost can only have 3 decimals. Example: 0.015");
		return;
	}
	let title = request.body.title;
	if (title.length < 4 || title.length > 50) {
		response.send("Tile must be between 4 to 50 characters");
		return;
	}
	let description = request.body.description.replace(/(\r\n|\r|\n){2,}/g, '\n');
	if (description.length < 10 || description.length > 400) {
		response.send("Description must be between 10 to 400 characters");
		return;
	}

	let latest_poll = await Poll.findOne({}, {}, { sort: { 'createdAt' : -1 } });
	let id;
	if (latest_poll == null) {
		id = 0;
	} else {
		id = latest_poll.id;
	}

	let poll = new Poll({
		id: id + 1,
		discord_id: discord_id,
		type: type,
		cost: cost,
		title: title,
		description: description,
		address: request.body.address,
		createdAt: Math.floor(Date.now() / 1000)
	});

	await poll.save()
		.then(async (doc) => {
			let params = {
		    embeds: [{
		    	author: {
		    		name: "Brain Juice",
		    		icon_url: "https://cdn.discordapp.com/icons/947688785565589584/f789e635f4e936f07f2ee13569289c9e.webp"
		    	},
			    title: `Poll created #${id+1}`,
			    description: `User **<@${discord_id}> (${discord_id})** created a poll\n**ID:** ${id+1}\n**Type:** ${type + (cost == 0 ? "" : " "+cost+" ETH")}`,
			    fields: [{
			    	name: "Title",
			    	value: title
			    },{
			    	name: "Description",
			    	value: description.replace("https://", "").replace("http://", "")
			    }],
			    color: 0x00dd00,
			    timestamp: new Date().toISOString()
		  	}]
		  }
			let res = await fetch(poll_webhook, {
			  method: 'POST',
			  body: JSON.stringify(params),
			  headers: { 'Content-type': 'application/json' },
			});
			response.send(true);
			return;
		})
		.catch((err) => {
			console.log("Error saving poll:", err);
			response.send("Unable to create poll");
			return;
		});
});

app.post('/report', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	if (request.body.content.length < 4 || request.body.content.length > 50) {
		response.send("Reason must be between 4 to 50 characters");
    return;
	}
	let id = parseInt(request.body.id);
	if (typeof id !== 'number') {
		response.send("Invalid ID");
		return;
	}
	let poll = await Poll.findOne({"discarded": false, "id": id});
	if (poll == null) {
		response.send("Invalid poll");
		return;
	}
	if (poll.createdAt <= Math.round(Math.floor(Date.now() / 1000) - 259200)) {
		response.send("This poll has already expired!");
		return;
	}
	let params = {
    embeds: [{
    	author: {
    		name: "Brain Juice",
    		icon_url: "https://cdn.discordapp.com/icons/947688785565589584/f789e635f4e936f07f2ee13569289c9e.webp"
    	},
	    title: `Poll Reported #${id}`,
	    description: "`" + request.body.address + "`\nReported poll #" + id,
	    fields: [{
	    	name: "Reason",
	    	value: request.body.content
	    }],
	    color: 0xdd0000
  	}]
  }
	let res = await fetch(report_webhook, {
	  method: 'POST',
	  body: JSON.stringify(params),
	  headers: { 'Content-type': 'application/json' },
	});
	response.send(true);
});

app.post('/discard', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	let id = parseInt(request.body.id);
	if (typeof id !== 'number') {
		response.send("Invalid ID");
		return;
	}
	let poll = await Poll.findOne({"discarded": false, "id": id});
	if (poll == null) {
		response.send("Invalid poll");
		return;
	}
	let owned = await Poll.find({"discarded": false, "address": request.body.address}, "id -_id");
	let owned_ = [];
	for (let own in owned) {
		owned_.push(owned[own].id)
	}
	if (!owned_.includes(poll.id)) {
		response.send("You don't own this poll");
		return;
	}
	if (poll.createdAt <= Math.round(Math.floor(Date.now() / 1000) - 259200)) {
		response.send("This poll has already expired");
		return;
	}
	await Poll.updateOne({"discarded": false, id: id}, {$set: {discarded: true}});
	response.send(true);
});

app.post('/claim-fund', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	if ((await Cred.findOne({"id": "blacklist"})).data.includes(request.body.address)) {
		response.send("You are blacklisted! Too bad, you can't claim any funds");
		return;
	}
	let v;
	await contract.methods.balanceOf(request.body.address).call((error, result) => {
		if (error || result == 0) {
	    response.send("You have to own at least one Brain Juice's for claiming the funds!");
	    return;
	  } else {
	  	v = true;
	  }
	});
	if (v != true) {
		return;
	}
	let id = parseInt(request.body.id);
	if (typeof id !== 'number') {
		response.send("Invalid ID");
		return;
	}
	let poll = await Poll.findOne({"discarded": false, "id": id});
	if (poll == null) {
		response.send("Invalid poll");
		return;
	}
	if (poll.claimed == true) {
		response.send("You already claimed your funds");
		return;
	}
	let owned = await Poll.find({"discarded": false, "address": request.body.address}, "id -_id");
	let owned_ = [];
	for (let own in owned) {
		owned_.push(owned[own].id)
	}
	if (!owned_.includes(poll.id)) {
		response.send("You don't own this poll");
		return;
	}
	if (poll.createdAt > Math.round(Math.floor(Date.now() / 1000) - 259200)) {
		response.send("This poll isn't expired yet");
		return;
	}
	if (poll.nope >= poll.dope || poll.dope < 10) {
		response.send("Your poll isn't good enough to be approved!");
		return;
	}
	if (poll.verified == false) {
		response.send("Your poll hasn't been verified yet");
		return;
	}
	let cost = poll.cost;
	if (cost == undefined || cost == null || cost < 0.01 || cost > 1) {
		response.send("Invalid cost");
		return;
	} else if (Math.floor(cost) !== cost && cost.toString().split(".")[1].length > 3) {
		response.send("Invalid cost");
		return;
	}
	let result = await Poll.updateOne({"claimed": false, id: id}, {$set: {claimed: true}});
	if (result.acknowledged == true) {
		let user = await Polluserdata.findOne({address: request.body.address});
		if (user == null) {
			let userdata = new Polluserdata({
				address: request.body.address,
				upvoted: [],
				downvoted: []
			});
			await userdata.save()
				.catch((err) => {
					console.log("Error saving userdata:", err);
					response.send("Unable to claim... Try contacting our staff team");
					return;
				});
		}
		let res = await Polluserdata.findOneAndUpdate({address: request.body.address}, {$inc: {bank: poll.cost}});
		if (res.address == request.body.address) {
			response.send(true);
			return;
		} else {
			console.log("Wrong account error:", res)
			response.send("Something went wrong...");
			return;
		}
	} else {
		response.send("Something went wrong...");
		return;
	}
});

app.get('/project', (request, response) => {
	response.render('project');
});

app.get('/features', (request, response) => {
	response.render('features');
});

app.get('/voting-info', (request, response) => {
	response.render('voting_info');
});

app.get('/gallery', (request, response) => {
	response.render('gallery');
});

app.get('/faq', (request, response) => {
	response.render('faq');
});

app.get('/partners', (request, response) => {
	response.render('partners');
});

app.get('/privacy-policy', (request, response) => {
	response.render('privacy_policy');
});

app.get('/mint', (request, response) => {
	response.render('mint');
});

app.post('/mint', async (request, response) => {
	const proof = merkleTree.getHexProof(keccak256(request.body.address));
	let cost;
	if (await contract.methods.presale().call() == true) {
		cost = 5 //0.05
	} else {
		cost = 7 //0.07
	}
	response.json({"abi": ABI, "address": contract_address, "proof": proof, "value": request.body.amount/100*cost*10**18, "errors": errors});
});

app.post('/dashboard', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.account != undefined) {
		let account = request.body.account;
		if (temp_access_token[account] != undefined && temp_access_token[account] == request.body.access_token) {
			let polls = await Poll.find({"discarded": false, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, limit: 3 });
			let owned = await Poll.find({"discarded": false, "address": request.body.account}, "id -_id");
			let owned_ = [];
			for (let own in owned) {
				owned_.push(owned[own].id);
			}
			if (Array.isArray(polls) && polls.length == 0) {
				polls = 0;
			}
			if (Array.isArray(owned_) && owned_.length == 0) {
				owned_ = 0;
			}
			let votes = await Polluserdata.findOne({address: request.body.account}, "-_id upvoted downvoted");
			if (votes == null) {
				votes = 0;
			}
			response.render('dashboard', {"address": account, "polls": polls, "owned": owned_, "votes": votes});
		} else {
			await Cred.updateOne({"id": "access_token"}, {$unset: {[`data.${account}`]: 1}});
			response.redirect('/verify?a=true&loc=dashboard');
		}
	} else {
		let nonce = request.body.nonce;
		let account = temp_nonce[nonce];
		delete temp_nonce[nonce];
		let signature = request.body.signature;
		let message = `Verify: nonce ${nonce}`;
		let signer;
		try {
			signer = await web3.eth.accounts.recover(message, signature=signature);
		} catch (err) {
			console.log(err);
			account = undefined;
		}
		if (account == undefined || account != signer) {
			response.redirect("/verify?loc=dashboard");
		} else {
			await Cred.updateOne({"id": "access_token"}, {$set: {[`data.${account}`]: request.body.access_token}});
			let polls = await Poll.find({"discarded": false, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, limit: 3 });
			let owned = await Poll.find({"discarded": false, "address": request.body.account}, "id -_id");
			let owned_ = [];
			for (let own in owned) {
				owned_.push(owned[own].id)
			}
			if (Array.isArray(polls) && polls.length == 0) {
				polls = 0;
			}
			if (Array.isArray(owned_) && owned_.length == 0) {
				owned_ = 0;
			}
			let votes = await Polluserdata.findOne({address: request.body.account}, "-_id upvoted downvoted");
			if (votes == null) {
				votes = 0;
			}
			response.render('dashboard', {"address": account, "polls": polls, "owned": owned_, "votes": votes});
		}
	}
});

app.post('/voting', async (request, response) => {
	if (request.query.page == undefined || request.query.page < 1) {
		request.query.page = 1;
	}
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.account != undefined) {
		let account = request.body.account;
		if (temp_access_token[account] != undefined && temp_access_token[account] == request.body.access_token) {
			let polls;
			if (request.query.filter == "expired") {
				Poll.countDocuments({"discarded": false, "createdAt": { $lte: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, (err, count) => {
					if (count <= request.query.page*9) {
						request.query.page = Math.ceil(count/9);
					}
				});
				polls = await Poll.find({"discarded": false, "createdAt": { $lte: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, skip: (request.query.page-1)*9, limit: 9 });
			} else if (request.query.filter == "mypoll") {
				Poll.countDocuments({"discarded": false, "address": request.body.account}, (err, count) => {
					if (count <= request.query.page*9) {
						request.query.page = Math.ceil(count/9);
					}
				});
				polls = await Poll.find({"discarded": false, "address": request.body.account}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, skip: (request.query.page-1)*9, limit: 9 });
			} else {
				Poll.countDocuments({"discarded": false, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, (err, count) => {
					if (count <= request.query.page*9) {
						request.query.page = Math.ceil(count/9);
					}
				});
				polls = await Poll.find({"discarded": false, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, skip: (request.query.page-1)*9, limit: 9 });
			}
			let pinned = await Poll.find({"discarded": false, "pinned": true, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, limit: 3 });
			let owned = await Poll.find({"discarded": false, "address": request.body.account}, "id -_id");
			let owned_ = [];
			for (let own in owned) {
				owned_.push(owned[own].id)
			}
			polls = pinned.concat(polls);
			if (Array.isArray(polls) && polls.length == 0) {
				polls = 0;
			}
			if (Array.isArray(owned_) && owned_.length == 0) {
				owned_ = 0;
			}
			let votes = await Polluserdata.findOne({address: request.body.account}, "-_id upvoted downvoted");
			if (votes == null) {
				votes = 0;
			}
			response.render('voting', {"address": account, "polls": polls, "owned": owned_, "votes": votes});
		} else {
			await Cred.updateOne({"id": "access_token"}, {$unset: {[`data.${account}`]: 1}});
			response.redirect(`/verify?a=true&loc=voting?page=${request.query.page}`);
		}
	} else {
		let nonce = request.body.nonce;
		let account = temp_nonce[nonce];
		delete temp_nonce[nonce];
		let signature = request.body.signature;
		let message = `Verify: nonce ${nonce}`;
		let signer;
		try {
			signer = await web3.eth.accounts.recover(message, signature=signature);
		} catch (err) {
			console.log(err);
			account = undefined;
		}
		if (account == undefined || account != signer) {
			response.redirect(`/verify?loc=voting?page=${request.query.page}`);
		} else {
			await Cred.updateOne({"id": "access_token"}, {$set: {[`data.${account}`]: request.body.access_token}});
			let polls;
			if (request.query.filter == "expired") {
				Poll.countDocuments({"discarded": false, "createdAt": { $lte: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, (err, count) => {
					if (count <= request.query.page*9) {
						request.query.page = Math.ceil(count/9);
					}
				});
				polls = await Poll.find({"discarded": false, "createdAt": { $lte: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, skip: (request.query.page-1)*9, limit: 9 });
			} else if (request.query.filter == "mypoll") {
				Poll.countDocuments({"discarded": false, "address": request.body.account}, (err, count) => {
					if (count <= request.query.page*9) {
						request.query.page = Math.ceil(count/9);
					}
				});
				polls = await Poll.find({"discarded": false, "address": request.body.account}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, skip: (request.query.page-1)*9, limit: 9 });
			} else {
				Poll.countDocuments({"discarded": false, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, (err, count) => {
					if (count <= request.query.page*9) {
						request.query.page = Math.ceil(count/9);
					}
				});
				polls = await Poll.find({"discarded": false, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, skip: (request.query.page-1)*9, limit: 9 });
			}
			let pinned = await Poll.find({"discarded": false, "pinned": true, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}}, "-address -_id -discarded", { sort: { 'createdAt' : 1 }, limit: 3 });
			let owned = await Poll.find({"discarded": false, "address": request.body.account}, "id -_id");
			let owned_ = [];
			for (let own in owned) {
				owned_.push(owned[own].id)
			}
			polls = pinned.concat(polls);
			if (Array.isArray(polls) && polls.length == 0) {
				polls = 0;
			}
			if (Array.isArray(owned_) && owned_.length == 0) {
				owned_ = 0;
			}
			let votes = await Polluserdata.findOne({address: request.body.account}, "-_id upvoted downvoted");
			if (votes == null) {
				votes = 0;
			}
			response.render('voting', {"address": account, "polls": polls, "owned": owned_, "votes": votes});
		}
	}
});

app.post('/create-poll', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.account != undefined) {
		let account = request.body.account;
		if (temp_access_token[account] != undefined && temp_access_token[account] == request.body.access_token) {
			if (request.body.discord_id == undefined) {
				if ((await Poll.findOne({"discarded": false, "address": request.body.account, "createdAt": { $gt: Math.round(Math.floor(Date.now() / 1000) - 259200)}})) != null) {
					response.send("You have already created a poll in the past 3 days! Wait for the poll to expire or discard it");
					return;
				}
				response.send(true);
				return;
			}
			await Cred.updateOne({"id": "discord_id"}, {$set: {[`data.${account}`]: request.body.discord_id}});
			response.render('create_poll', {"address": account, "discord_id": request.body.discord_id});
		} else {
			await Cred.updateOne({"id": "access_token"}, {$unset: {[`data.${account}`]: 1}});
			response.redirect('/verify?a=true&loc=create-poll');
		}
	} else {
		let nonce = request.body.nonce;
		let account = temp_nonce[nonce];
		delete temp_nonce[nonce];
		let signature = request.body.signature;
		let message = `Verify: nonce ${nonce}`;
		let signer;
		try {
			signer = await web3.eth.accounts.recover(message, signature=signature);
		} catch (err) {
			console.log(err);
			account = undefined;
		}
		if (account == undefined || account != signer) {
			response.redirect("/verify?loc=create-poll");
		} else {
			await Cred.updateOne({"id": "access_token"}, {$set: {[`data.${account}`]: request.body.access_token}});
			if (request.body.discord_id == undefined) {
				response.redirect(discordauthurl);
				return;
			}
			await Cred.updateOne({"id": "discord_id"}, {$set: {[`data.${account}`]: request.body.discord_id}});
			response.render('create_poll', {"address": account, "discord_id": request.body.discord_id});
		}
	}
});

app.get('/dashboard', (request, response) => {
	response.redirect("/verify?loc=dashboard");
});

app.get('/voting', (request, response) => {
	response.redirect("/verify?loc=voting");
});

app.get('/create-poll', async (request, response) => {
	if (request.query.code == undefined) {
		response.redirect(discordauthurl);
		return;
	}

	const params = new URLSearchParams();
	params.append('client_id', "964802962432098305");
	params.append('client_secret', "hYoyaoPLyR4T0T0W7O1qhxQbRmvn9MAY");
	params.append('grant_type', 'authorization_code');
	params.append('code', request.query.code);
	params.append('redirect_uri', "https://localhost:3000/create-poll");
	params.append('scope', "identify");

	let res = await fetch('https://discord.com/api/v9/oauth2/token', {
	  method: 'POST',
	  body: params,
	  headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json' },
	});

	let body = await res.json();
	let accessToken = body['access_token'];

	res = await fetch("https://discord.com/api/v9/users/@me", {
    method: 'GET',
    headers: {'Authorization': `Bearer ${accessToken}`}
	});
	body = await res.json();
	response.redirect(`/verify?loc=create-poll&discord_id=${body.id}`);
});

app.get('/request-nonce', (request, response) => {
	if (request.query.account == undefined) {
		response.send("Threat detected");
	}
	let uuid = crypto.randomBytes(20).toString('hex');
	let access_token = crypto.randomBytes(20).toString('hex');
	let payload = {'nonce': uuid, 'access_token': access_token};
	if (Object.keys(temp_nonce).length >= 10) {
		temp_nonce = {};
		console.log("Bug: temp_nonce not clearing");
	}
	temp_nonce[uuid] = request.query.account;
  response.send(payload);
});

app.get('/verify', (request, response) => {
	response.render('verify');
});

app.post('/userdata', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	response.setHeader('Content-Type', 'application/json');
	if (request.body.address == undefined || request.body.access_token == undefined || request.body.address == null || request.body.access_token == null || temp_access_token[request.body.address] != request.body.access_token) {
		response.json({});
		return;
	}
	let data = {};

	let nftCount = await contract.methods.balanceOf(request.body.address).call();
	data.nftCount = nftCount;

	let nftsOwned = await contract.methods.nftsOwned(request.body.address).call();
	nftsOwned = nftsOwned || [];
	data.nftsOwned = [];
	for (let nft in nftsOwned) {
		data.nftsOwned.push(await contract.methods.tokenURI(nftsOwned[nft]).call().catch((err)=>{return getErrorMessage(err);}));
	}

	let userBank = await Polluserdata.findOne({id: request.body.address});
	data.bank = userBank.bank || 0;
	response.json(data);
});

app.post('/withdraw', async (request, response) => {
	let temp_access_token = (await Cred.findOne({"id": "access_token"})).data;
	if (request.body.address == undefined || temp_access_token[request.body.address] == undefined || temp_access_token[request.body.address] != request.body.access_token) {
		response.send("Invalid account, try refreshing the page!");
		return;
	}
	if ((await Cred.findOne({"id": "blacklist"})).data.includes(request.body.address)) {
		response.send("You are blacklisted! Too bad, you can't withdraw funds");
		return;
	}
	let user = await Polluserdata.findOne({address: request.body.address});
	if (user == null) {
		response.send("You have no ETH to withdraw!");
		return;
	}
	if (user.bank < 0.01) {
		response.send("You need at least 0.01 ETH to withdraw!");
		return;
	}
	let result = await Polluserdata.updateOne({address: request.body.address, bank: {$gt: 0}}, {$set: {bank: 0}});
	if (result.acknowledged == true) {
		let gasprice = (await (await fetch("https://www.etherchain.org/api/gasPriceOracle")).json()).currentBaseFee
		let gasfee = Math.floor(gasprice*50787);
		result = await contract.methods.withdraw(request.body.address, ((user.bank*10**18)-gasfee).toString()).send({from: owner, gasLimit: gasfee});
		try {
			if (result.status == true) {
				let params = {
			    embeds: [{
			    	author: {
			    		name: "Brain Juice",
			    		icon_url: "https://cdn.discordapp.com/icons/947688785565589584/f789e635f4e936f07f2ee13569289c9e.webp"
			    	},
				    title: "Funds withdrew",
				    description: `A member withdrew **${user.bank}** ETH from the community bank`,
				    fields: [{
				    	name: "Gas fees",
				    	value: `**Gas limit** 50787\n**Gas price** ${gasprice} GWEI\n**Gas cost** ${gasfee}\n**Gas fee** ${gasfee/1000000000} ETH\n**ETH received** ${user.bank-(gasfee/1000000000)} ETH`
				    }],
				    color: 0xdddd00,
				    timestamp: new Date().toISOString()
			  	}]
			  }
			  if (!owner_addresses.includes(request.body.address)) {
					let res = await fetch(withdraw_webhook, {
					  method: 'POST',
					  body: JSON.stringify(params),
					  headers: { 'Content-type': 'application/json' },
					});
				}
				response.send(true);
				return;
			} else {
				response.send("Unable to withdraw funds, contact our staff team if you think this is a mistake");
				return;
			}
		} catch {
			response.send("Unable to withdraw funds, contact our staff team if you think this is a mistake");
			return;
		}
	}
});

app.use(function (request, response, next) {
  response.status(404).render("page_not_found");
});

// kings man 3, uncharted, matrix ressurection, adam project
// on production change: contract address, contract abi, discord auth redirect uri
// contract initial deploy cost 0.007093, set both cost 0.000091 to 0.0001311, set root 0.00004392, set proof 0.00085704, set pause 0.00004343, mint 1: 0.000285 to 0.000413, mint 2: 0.000382, phase 0.00005154
