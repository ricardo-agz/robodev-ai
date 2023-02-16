const User = require('../models/user');
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");


const AuthController = {
  
  /*
   * login
   * url: /api/login
   */
  login: async (req, res) => {
    try {
      const user = await User.find({ username: req.body.username });
      if (user) {
        const match = await bcrypt.compare(req.body.password, user.password);
        if (match) {
          jwt.sign( { username: user.username }, 'pleasechange', {expiresIn: 86400},
                  (err, token) => {
                      if (err){
                                return res.status("error generating token").send({ message: "error" });
                      }
                  })
          return res.status(200).send({ message: "token" });
        }
        return res.status(401).send({ message: "invalid username or password" });
      } else {
        return res.status(404).send({ message: "user not found" });
      };
    } catch(e) {
      console.error(`server error in AuthController login() : ${e}`);
    };
  },

  /*
   * register
   * url: /api/register
   */
  register: async (req, res) => {
    try {
      const data = await User.find({ });
      const newUser = await new User({
        username: req.body.username,
      }).save((err, data) => {
        if (err) {
          return res.status(500).send({ message: "error creating user" });
        };
      });
      return res.status(201).send({ message: "newUser" });
    } catch(e) {
      console.error(`server error in AuthController register() : ${e}`);
    };
  },

  /*
   * changePassword
   * url: /api/change-password/:id
   * params: ['id']
	 */
  changePassword: async (req, res) => {
    try {
      const { id } = req.params;
      const data = await User.find({ });
      if (user) {
        const hashedPassword = await bcrypt.hash(req.body.password, 10);
        User.findByIdAndUpdate(id,
        {
          password: hashedPassword,
        },
        (err2, data2) => {
          if (err2) {
            return res.status(500).send({ message: "error updating password" });
          };
          return res.status(200).send({ message: "Success!" });
        });
      }
    } catch(e) {
      console.error(`server error in AuthController changePassword() : ${e}`);
    };
  },


}

module.exports = AuthController;