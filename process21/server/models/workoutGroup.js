const mongoose = require('mongoose');

const WorkoutGroupSchema = new mongoose.Schema({
	name: {
		type: String,
		required: true
	},
	members: [
		{
			type: mongoose.Schema.Types.ObjectId,
			ref: 'User'
		}
	]
});

WorkoutGroupSchema.set('toObject', { virtuals: true });
WorkoutGroupSchema.set('toJSON', { virtuals: true });

const WorkoutGroup = mongoose.model('WorkoutGroup', WorkoutGroupSchema);
module.exports = WorkoutGroup;
