const mongoose = require('mongoose');

const WorkoutgroupSchema = new mongoose.Schema({
})

WorkoutgroupSchema.set('toObject', { virtuals: true });
WorkoutgroupSchema.set('toJSON', { virtuals: true });

const Workoutgroup = mongoose.model('Workoutgroup', WorkoutgroupSchema);
module.exports = Workoutgroup;
