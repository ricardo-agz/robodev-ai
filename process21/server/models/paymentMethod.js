const mongoose = require('mongoose');

const PaymentMethodSchema = new mongoose.Schema({
	card_number: {
		type: Number,
		required: true
	},
	name: {
		type: String,
		required: true
	},
	expiration_date: {
		type: String,
		required: true
	},
	CVV: {
		type: Number,
		required: true
	},
	owner: {
		type: mongoose.Schema.Types.ObjectId,
		ref: 'User',
		required: true
	},
});

PaymentMethodSchema.set('toObject', { virtuals: true });
PaymentMethodSchema.set('toJSON', { virtuals: true });

const PaymentMethod = mongoose.model('PaymentMethod', PaymentMethodSchema);
module.exports = PaymentMethod;
