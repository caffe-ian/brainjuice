const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const credSchema = new Schema({
	id: {
		type: String,
		required: true
	},
	data: {}
}, { collection: "credentials", versionKey: false });

const Cred = mongoose.model('Cred', credSchema);
module.exports = Cred;