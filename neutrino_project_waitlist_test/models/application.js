const mongoose = require('mongoose');

const ApplicationSchema = new mongoose.Schema({
	first_name: {
		type: String,
		required: true
	},
	last_name: {
		type: String,
		required: true
	},
	company: {
		type: String,
		required: true
	},
	description: {
		type: String,
		required: true
	},
	accepted: {
		type: Boolean,
		required: true
	},
	applicant: {
		type: mongoose.Schema.Types.ObjectId,
		ref: 'User',
		required: true 
	},
});


const Application = mongoose.model('Application', ApplicationSchema);
module.exports = Application;
