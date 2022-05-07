const WorkoutPlan = require('../models/workoutPlan');


const WorkoutPlanController = {

  // REMOVE TO ENABLE PAGINATION
  index: async (req, res) => {
    try {
      const data = await WorkoutPlan.find()
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  }, 

  // UNCOMMENT AND FOLLOW INSTRUCTIONS TO ENABLE PAGINATION
  /*
  all: async (req, res, next) => {
    const page = parseInt(req.query.page);
    const limit = parseInt(req.query.limit);
    const skipIndex = (page - 1) * limit;
    const results = {};

    try {
      results.results = await WorkoutPlan.find()
        .sort({ _id: 1 })
        .limit(limit)
        .skip(skipIndex)
        .exec();
      res.paginatedResults = results;
      next();
    } catch (e) {
      res.status(500).json({ message: "Error Occured" });
    }
  }, 
  */

  /* INSTRUCTIONS
  in index.js, replace:
    app.get('/workoutplans', WorkoutPlanController.all);

  with:
    app.get('/workoutplans', WorkoutPlanController.all, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  show: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await WorkoutPlan.findById(id)
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  create: async (req, res) => {
    try {
      await workoutplan.save();
      res.status(200).send('data created!');
      console.log('WorkoutPlan created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await WorkoutPlan.findById(id);
    WorkoutPlan.findByIdAndUpdate(id, 
    {
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err);
        console.log(err);
      } else {
        res.status(200).send(data);
        console.log('WorkoutPlan updated!');
      }
    })
  },

  delete: async (req, res) => {
    const { id } = req.params;
    const data = await WorkoutPlan.findById(id);
    try {
      WorkoutPlan.findByIdAndDelete(id).exec();
      res.status(200).send('WorkoutPlan deleted');
      console.log('WorkoutPlan deleted!');
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },



}

module.exports = WorkoutPlanController;