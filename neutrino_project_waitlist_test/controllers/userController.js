const User = require('../models/user');


const UserController = {
  
  /*
   * index
   * url: /api/users
   */
  index: async (req, res) => {
    try {
      const data = await user.find({});
      return res.status(200).send(data);
    } catch(e) {
      console.error(`server error in UserController index() : ${e}`);
    };
  },

  /*
   * show
   * url: /api/users/:id
   * params: ['id']
	 */
  show: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await user.findById(id);
      return res.status(200).send(data);
    } catch(e) {
      console.error(`server error in UserController show() : ${e}`);
    };
  },

  /*
   * update
   * url: /api/users/:id
   * params: ['id']
	 */
  update: async (req, res) => {
    try {
      const { id } = req.params;
      const newData = await user.findByIdAndUpdate(id,
      {
        username,
        email,
        password,
      },
      (err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error updating user" });
        };
        return res.status(200).send({ message: "user was successfully updated!" });
      });
    } catch(e) {
      console.error(`server error in UserController update() : ${e}`);
    };
  },

  /*
   * delete
   * url: /api/users/:id
   * params: ['id']
	 */
  delete: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await user.findByIdAndDelete(id,
      (err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error deleting user" });
        };
        return res.status(200).send({ message: "user was successfully deleted" });
      });
    } catch(e) {
      console.error(`server error in UserController delete() : ${e}`);
    };
  },


}

module.exports = UserController;