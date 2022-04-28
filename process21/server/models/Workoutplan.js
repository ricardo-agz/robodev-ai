const mongoose = require('mongoose');

const WorkoutplanSchema = new mongoose.Schema({
})

WorkoutplanSchema.set('toObject', { virtuals: true });
WorkoutplanSchema.set('toJSON', { virtuals: true });

const Workoutplan = mongoose.model('Workoutplan', WorkoutplanSchema);
module.exports = Workoutplan;
