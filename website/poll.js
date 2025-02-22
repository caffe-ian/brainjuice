const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const pollSchema = new Schema({
	id: {
		type: Number,
		required: true
	},
	discord_id: {
		type: String,
		required: true
	},
	type: {
		type: String,
		required: true
	},
	cost: {
		type: Number,
		default: 0
	},
	title: {
		type: String,
		required: true
	},
	description: {
		type: String,
		required: true
	},
	dope: {
		type: Number,
		default: 0
	},
	nope: {
		type: Number,
		default: 0
	},
	address : {
		type: String,
		required: true
	},
	pinned: {
		type: Boolean,
		default: false
	},
	verified: {
		type: Boolean,
		default: false
	},
	discarded: {
		type: Boolean,
		default: false
	},
	claimed: {
		type: Boolean,
		default: false
	},
	createdAt: {
		type: Number,
		required: true
	}
}, { collection: "polls", versionKey: false });

const Poll = mongoose.model('Poll', pollSchema);
module.exports = Poll;