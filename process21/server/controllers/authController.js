const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
require('dotenv').config();

const User = require('../models/user');

const AuthController = {
  login: async (req, res) => {
    const user = await User.findOne({ username: req.body.username });
    if (!user) return res.status(400).json({ message: "Invalid username" });

    const checkpassword = await bcrypt.compare(req.body.password, user.password);
    if (!checkpassword) return res.status(400).json({ message: "Incorrect password" });

    const payload = {
      id: user._id.toString(),
      username: user.username,
    }
    jwt.sign(
      payload,
      process.env.JWT_SECRET, { expiresIn: 86400 },
      (err, token) => {
        if (err) return res.json({ message: err });
        return res.json({
          id: user._id.toString(),
          token: "Bearer " + token
        });
      }
    );
  },

  register: async (req, res) => {
    const user = req.body;      
    const takenUsername = await User.findOne({ username: user.username });
    const takenEmail = await User.findOne({ email: user.email });

    if (takenUsername) {
      res.status(400).json({ message: "Username already taken" });
    } else if (takenEmail) {
      res.status(400).json({ message: "Email already exists" });
    } else {
      user.password = await bcrypt.hash(req.body.password, 10);
      user.email = user.email.toLowerCase();
      user.username = user.username.toLowerCase();
      const dbUser = new User(user);
      dbUser.save();
      res.json({ message: "Success" });
    }
  }
}

module.exports = AuthController;