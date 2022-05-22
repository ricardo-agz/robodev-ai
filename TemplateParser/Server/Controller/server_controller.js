const $$Name$$ = require('../models/$$nameCamel$$');
$$AUTH$$:0


const $$Name$$Controller = {

  // REMOVE TO ENABLE PAGINATION
  index: async (req, res) => {
    try {
      const data = await $$Name$$.find()
        $$ONE_TO_MANY:ONE
        $$index_logic$$
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  }, 

  // UNCOMMENT AND FOLLOW INSTRUCTIONS TO ENABLE PAGINATION
  /*
  index: async (req, res, next) => {
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
  in server.js, replace:
    app.get('/$$pluralname$$', $$Name$$Controller.index);

  with:
    app.get('/$$pluralname$$', $$Name$$Controller.index, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  show: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await $$Name$$.findById(id)
        $$ONE_TO_MANY:ONE
        $$show_logic$$
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  create: async (req, res) => {
    $$CREATE_DECLARATIONS$$
    try {
      $$create_logic$$
      await $$nameCamel$$.save();
      res.status(200).send('data created!');
      console.log('$$Name$$ created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await $$Name$$.findById(id);
    $$update_logic$$
    $$Name$$.findByIdAndUpdate(id, 
    {
      $$UPDATE_PARAMS$$
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
    const data = await $$Name$$.findById(id);
    $$destroy_logic$$
    try {
      $$Name$$.findByIdAndDelete(id).exec();
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