const PaymentMethod = require('../models/paymentMethod');


const PaymentMethodController = {

  // REMOVE TO ENABLE PAGINATION
  index: async (req, res) => {
    try {
      const data = await PaymentMethod.find()
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
      results.results = await PaymentMethod.find()
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
    app.get('/paymentmethods', PaymentMethodController.all);

  with:
    app.get('/paymentmethods', PaymentMethodController.all, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  show: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await PaymentMethod.findById(id)
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  create: async (req, res) => {
    try {
      await paymentmethod.save();
      res.status(200).send('data created!');
      console.log('PaymentMethod created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await PaymentMethod.findById(id);
    PaymentMethod.findByIdAndUpdate(id, 
    {
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err);
        console.log(err);
      } else {
        res.status(200).send(data);
        console.log('PaymentMethod updated!');
      }
    })
  },

  delete: async (req, res) => {
    const { id } = req.params;
    const data = await PaymentMethod.findById(id);
    try {
      PaymentMethod.findByIdAndDelete(id).exec();
      res.status(200).send('PaymentMethod deleted');
      console.log('PaymentMethod deleted!');
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },



}

module.exports = PaymentMethodController;