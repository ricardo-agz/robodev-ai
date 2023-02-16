const Application = require('../models/application');
const User = require('../models/user');


const ApplicationController = {
  
  /*
   * index
   * url: /api/applications
   */
  index: async (req, res) => {
    try {
      const data = await application.find({});
      return res.status(200).send(data);
    } catch(e) {
      console.error(`server error in ApplicationController index() : ${e}`);
    };
  },

  /*
   * show
   * url: /api/applications/:id
   * params: ['id']
	 */
  show: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await application.findById(id);
      return res.status(200).send(data);
    } catch(e) {
      console.error(`server error in ApplicationController show() : ${e}`);
    };
  },

  /*
   * create
   * url: /api/applications
   */
  create: async (req, res) => {
    try {
      const newData = await new User({
        first_name,
        last_name,
        company,
        description,
        accepted,
      }).save((err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error creating new application" });
        };
        return res.status(200).send({ message: "New application was successfully created!" });
      });
    } catch(e) {
      console.error(`server error in ApplicationController create() : ${e}`);
    };
  },

  /*
   * update
   * url: /api/applications/:id
   * params: ['id']
	 */
  update: async (req, res) => {
    try {
      const { id } = req.params;
      const newData = await application.findByIdAndUpdate(id,
      {
        first_name,
        last_name,
        company,
        description,
        accepted,
      },
      (err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error updating application" });
        };
        return res.status(200).send({ message: "application was successfully updated!" });
      });
    } catch(e) {
      console.error(`server error in ApplicationController update() : ${e}`);
    };
  },

  /*
   * delete
   * url: /api/applications/:id
   * params: ['id']
	 */
  delete: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await application.findByIdAndDelete(id,
      (err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error deleting application" });
        };
        return res.status(200).send({ message: "application was successfully deleted" });
      });
    } catch(e) {
      console.error(`server error in ApplicationController delete() : ${e}`);
    };
  },


}

module.exports = ApplicationController;