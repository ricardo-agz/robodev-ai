const AccessCode = require('../models/accessCode');

const AccessCodeController = {
  
  /*
   * index
   * url: /api/accesscodes
   */
  index: async (req, res) => {
    try {
      const data = await AccessCode.find({});
      return res.status(200).send(data);
    } catch(e) {
      console.error(`server error in AccessCodeController index() : ${e}`);
    };
  },

  /*
   * show
   * url: /api/accesscodes/:id
   * params: ['id']
	 */
  show: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await accesscode.findById(id);
      return res.status(200).send(data);
    } catch(e) {
      console.error(`server error in AccessCodeController show() : ${e}`);
    };
  },

  /*
   * create
   * url: /api/accesscodes
   */
  create: async (req, res) => {
    try {
      const newData = await new AccessCode({
        code,
        status,
      }).save((err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error creating new accesscode" });
        };
        return res.status(200).send({ message: "New accesscode was successfully created!" });
      });
    } catch(e) {
      console.error(`server error in AccessCodeController create() : ${e}`);
    };
  },

  /*
   * update
   * url: /api/accesscodes/:id
   * params: ['id']
	 */
  update: async (req, res) => {
    try {
      const { id } = req.params;
      const newData = await accesscode.findByIdAndUpdate(id,
      {
        code,
        status,
      },
      (err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error updating accesscode" });
        };
        return res.status(200).send({ message: "accesscode was successfully updated!" });
      });
    } catch(e) {
      console.error(`server error in AccessCodeController update() : ${e}`);
    };
  },

  /*
   * delete
   * url: /api/accesscodes/:id
   * params: ['id']
	 */
  delete: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await accesscode.findByIdAndDelete(id,
      (err, data) => {
        if (err) {
          return res.status(500).send({ message: "Error deleting accesscode" });
        };
        return res.status(200).send({ message: "accesscode was successfully deleted" });
      });
    } catch(e) {
      console.error(`server error in AccessCodeController delete() : ${e}`);
    };
  },

  /*
   * useCode
   * url: /api/access-codes/:id/use
   * params: ['id']
	 */
  useCode: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await AccessCode.find({ });
      if (accessCode) {
        if (accessCode.status == "unused") {
          AccessCode.updateOne(id,
          {
            status: "used",
          },
          (err3, data3) => {
            if (err3) {
              return res.status(500).send({ message: "error updating access code status" });
            };
          });
          return res.status(200).send({ message: "Success!" });
        } else {
          return res.status(200).send({ message: "Success!" });
        };
        return res.status(400).send({ message: "access code already used" });
      } else {
        return res.status(404).send({ message: "access code not found" });
      };
    } catch(e) {
      console.error(`server error in AccessCodeController useCode() : ${e}`);
    };
  },


}

module.exports = AccessCodeController;