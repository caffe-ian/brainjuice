const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const userdataSchema = new Schema({
	address: {
		type: String,
		required: true
	},
	upvoted: {
		type: [Number],
		required: true
	},
	downvoted: {
		type: [Number],
		required: true
	},
	bank: {
		type: Number,
		default: 0
	}
}, { collection: "polls-userdata", versionKey: false });

const Polluserdata = mongoose.model('Polluserdata', userdataSchema);
module.exports = Polluserdata;