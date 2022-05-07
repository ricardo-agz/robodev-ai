const mongoose = require('mongoose');

const MonthlyPledgeSchema = new mongoose.Schema({
	payment_amount: {
		type: Number,
		required: true
	},
	active: {
		type: Boolean,
		required: true
	},
	user: {
		type: mongoose.Schema.Types.ObjectId,
		ref: 'User',
		required: true
	},
});

MonthlyPledgeSchema.virtual('workoutplans', {
	ref: 'WorkoutPlan',
	localField: '_id',
	foreignField: 'pledge'
});

MonthlyPledgeSchema.set('toObject', { virtuals: true });
MonthlyPledgeSchema.set('toJSON', { virtuals: true });

const MonthlyPledge = mongoose.model('MonthlyPledge', MonthlyPledgeSchema);
module.exports = MonthlyPledge;
