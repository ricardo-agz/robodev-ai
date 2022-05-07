const User = require('../models/user');


const UserController = {

  // REMOVE TO ENABLE PAGINATION
  index: async (req, res) => {
    try {
      const data = await User.find()
				.populate({ path: 'paymentmethods', select: 'card_number name expiration_date CVV' })
				.populate({ path: 'workoutgroups', select: 'name' })
				.populate({ path: 'monthlypledges', select: 'payment_amount active' })
				.populate({ path: 'friends', select: 'name charity username email password' })
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
      results.results = await User.find()
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
    app.get('/users', UserController.all);

  with:
    app.get('/users', UserController.all, (req, res) => {
      res.json(res.paginatedResults.results);
    });
  */

  show: async (req, res) => {
    const { id } = req.params;
    try {
      const data = await User.findById(id)
				.populate({ path: 'paymentmethods', select: 'card_number name expiration_date CVV' })
				.populate({ path: 'workoutgroups', select: 'name' })
				.populate({ path: 'monthlypledges', select: 'payment_amount active' })
				.populate({ path: 'friends', select: 'name charity username email password' })
      res.status(200).send(data);
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  create: async (req, res) => {
    try {
      await user.save();
      res.status(200).send('data created!');
      console.log('User created!');
    } catch (err) {
      res.status(500).send(err);
      console.log(err);
    }
  },

  update: async (req, res) => {
    const { id } = req.params;
    const data = await User.findById(id);
    User.findByIdAndUpdate(id, 
    {
    },
    (err, data) => {
      if (err) {
        res.status(500).send(err);
        console.log(err);
      } else {
        res.status(200).send(data);
        console.log('User updated!');
      }
    })
  },

  delete: async (req, res) => {
    const { id } = req.params;
    const data = await User.findById(id);
    try {
      User.findByIdAndDelete(id).exec();
      res.status(200).send('User deleted');
      console.log('User deleted!');
    } catch (err) {
      res.status(400).send(err.message);
      console.log(err);
    }
  },

  addWorkoutGroup: async (req, res) => {
    const { id, workoutgroupId } = req.params;
    UserModel.findByIdAndUpdate(
      id, 
      { $push: { workoutgroups: workoutgroupId } },
      (err, data) => {
        if (err) {
          res.status(500).send(err);
          console.log(err);
        } else {
          res.status(200).send(data);
          console.log('WorkoutGroup added!');
        }
      }
    )
  },

  dropWorkoutGroup: async (req, res) => {
    const { id, workoutgroupId } = req.params;
    UserModel.findByIdAndUpdate(
      id, 
      { $pull: { workoutgroups: workoutgroupId } },
      (err, data) => {
        if (err) {
          res.status(500).send(err);
          console.log(err);
        } else {
          res.status(200).send(data);
          console.log('WorkoutGroup dropped!');
        }
      }
    )
  },

  addFriend: async (req, res) => {
    const { id, userId } = req.params;
    UserModel.findByIdAndUpdate(
      id, 
      { $push: { friends: userId } },
      (err, data) => {
        if (err) {
          res.status(500).send(err);
          console.log(err);
        } else {
          res.status(200).send(data);
          console.log('Friend added!');
        }
      }
    )
  },

  dropFriend: async (req, res) => {
    const { id, userId } = req.params;
    UserModel.findByIdAndUpdate(
      id, 
      { $pull: { friends: userId } },
      (err, data) => {
        if (err) {
          res.status(500).send(err);
          console.log(err);
        } else {
          res.status(200).send(data);
          console.log('Friend dropped!');
        }
      }
    )
  },



}

module.exports = UserController;