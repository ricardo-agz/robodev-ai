const mongoose = require('mongoose');

const AccessCodeSchema = new mongoose.Schema({
	code: {
		type: String,
		required: true
	},
	status: {
		type: String,
		required: true
	},
});


const AccessCode = mongoose.model('AccessCode', AccessCodeSchema);
module.exports = AccessCode;
