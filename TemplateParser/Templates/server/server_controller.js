const $$Name$$Model = require('../models/$$Name$$');
$$AUTH$$:0

const $$Name$$Controller = {

  find: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await $$Name$$Model.findById(id)
        $$ONE_TO_MANY:ONE
        $$logic$$:find
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  // REMOVE TO ENABLE PAGINATION
  all: async (req, res) => {
    try {
      const data = await $$Name$$Model.find()
        $$ONE_TO_MANY:ONE
        $$logic$$:all
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
      results.results = await $$Name$$.find()
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
    app.get('/$$name$$s', $$Name$$Controller.all);

  with:
    app.get('/$$name$$s', $$Name$$Controller.all, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  create: async (req, res) => {
    $$dynamic:0
    try {
      $$logic$$:create
      await $$name$$.save();
      res.status(200).send('data created!');
      console.log('$$Name$$ created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await $$Name$$Model.findById(id);
    $$logic$$:update
    $$Name$$Model.findByIdAndUpdate(id, 
    {
      $$dynamic:1
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err);
        console.log(err);
      } else {
        res.status(200).send(data);
        console.log('$$Name$$ updated!');
      }
    })
  },

  delete: async (req, res) => {
    const { id } = req.params;
    const data = await $$Name$$Model.findById(id);
    $$logic$$:delete
    try {
      $$Name$$Model.findByIdAndDelete(id).exec();
      res.status(200).send('$$Name$$ deleted');
      console.log('$$Name$$ deleted!');
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  $$MANY_TO_MANY

  $$AUTH$$:1
}

module.exports = $$Name$$Controller;