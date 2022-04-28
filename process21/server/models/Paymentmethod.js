const mongoose = require('mongoose');

const PaymentmethodSchema = new mongoose.Schema({
})

PaymentmethodSchema.set('toObject', { virtuals: true });
PaymentmethodSchema.set('toJSON', { virtuals: true });

const Paymentmethod = mongoose.model('Paymentmethod', PaymentmethodSchema);
module.exports = Paymentmethod;
