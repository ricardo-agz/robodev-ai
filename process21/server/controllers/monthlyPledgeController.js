const MonthlyPledge = require('../models/monthlyPledge');


const MonthlyPledgeController = {

  // REMOVE TO ENABLE PAGINATION
  index: async (req, res) => {
    try {
      const data = await MonthlyPledge.find()
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
      results.results = await MonthlyPledge.find()
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
    app.get('/monthlypledges', MonthlyPledgeController.all);

  with:
    app.get('/monthlypledges', MonthlyPledgeController.all, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  show: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await MonthlyPledge.findById(id)
				.populate({ path: 'workoutplans', select: 'target_days curr_days_met weekly_plan' })
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  create: async (req, res) => {
    try {
      await monthlypledge.save();
      res.status(200).send('data created!');
      console.log('MonthlyPledge created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await MonthlyPledge.findById(id);
    MonthlyPledge.findByIdAndUpdate(id, 
    {
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err);
        console.log(err);
      } else {
        res.status(200).send(data);
        console.log('MonthlyPledge updated!');
      }
    })
  },

  delete: async (req, res) => {
    const { id } = req.params;
    const data = await MonthlyPledge.findById(id);
    try {
      MonthlyPledge.findByIdAndDelete(id).exec();
      res.status(200).send('MonthlyPledge deleted');
      console.log('MonthlyPledge deleted!');
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },



}

module.exports = MonthlyPledgeController;