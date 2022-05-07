const mongoose = require('mongoose');

const WorkoutPlanSchema = new mongoose.Schema({
	target_days: {
		type: Number,
		required: true
	},
	curr_days_met: {
		type: Number,
		required: true
	},
	weekly_plan: {
		type: String,
		required: true
	},
	pledge: {
		type: mongoose.Schema.Types.ObjectId,
		ref: 'MonthlyPledge',
		required: true
	},
});

WorkoutPlanSchema.set('toObject', { virtuals: true });
WorkoutPlanSchema.set('toJSON', { virtuals: true });

const WorkoutPlan = mongoose.model('WorkoutPlan', WorkoutPlanSchema);
module.exports = WorkoutPlan;
