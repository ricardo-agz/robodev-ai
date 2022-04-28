const MonthlypledgeModel = require('../models/Monthlypledge');

const MonthlypledgeController = {

  find: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await MonthlypledgeModel.findById(id)
				.populate({ path: 'workoutplans', select: 'target_days curr_days_met weekly_plan' })
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  // REMOVE TO ENABLE PAGINATION
  all: async (req, res) => {
    try {
      const data = await MonthlypledgeModel.find()
				.populate({ path: 'workoutplans', select: 'target_days curr_days_met weekly_plan' })
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
      results.results = await Monthlypledge.find()
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
    app.get('/monthlypledges', MonthlypledgeController.all);

  with:
    app.get('/monthlypledges', MonthlypledgeController.all, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  create: async (req, res) => {
    try {
      await monthlypledge.save();
      res.status(200).send('data created!');
      console.log('Monthlypledge created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await MonthlypledgeModel.findById(id);
    MonthlypledgeModel.findByIdAndUpdate(id, 
    {
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err);
        console.log(err);
      } else {
        res.status(200).send(data);
        console.log('Monthlypledge updated!');
      }
    })
  },

  delete: async (req, res) => {
    const { id } = req.params;
    const data = await MonthlypledgeModel.findById(id);
    try {
      MonthlypledgeModel.findByIdAndDelete(id).exec();
      res.status(200).send('Monthlypledge deleted');
      console.log('Monthlypledge deleted!');
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },



}

module.exports = MonthlypledgeController;