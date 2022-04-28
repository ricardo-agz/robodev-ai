const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
})

UserSchema.virtual('paymentmethods', {
	ref: 'Paymentmethod',
	localField: '_id',
	foreignField: 'owner'
});

UserSchema.virtual('monthlypledges', {
	ref: 'Monthlypledge',
	localField: '_id',
	foreignField: 'user'
});

UserSchema.set('toObject', { virtuals: true });
UserSchema.set('toJSON', { virtuals: true });

const User = mongoose.model('User', UserSchema);
module.exports = User;
