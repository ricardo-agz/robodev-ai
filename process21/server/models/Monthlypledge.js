const mongoose = require('mongoose');

const MonthlypledgeSchema = new mongoose.Schema({
})

MonthlypledgeSchema.virtual('workoutplans', {
	ref: 'Workoutplan',
	localField: '_id',
	foreignField: 'pledge'
});

MonthlypledgeSchema.set('toObject', { virtuals: true });
MonthlypledgeSchema.set('toJSON', { virtuals: true });

const Monthlypledge = mongoose.model('Monthlypledge', MonthlypledgeSchema);
module.exports = Monthlypledge;
