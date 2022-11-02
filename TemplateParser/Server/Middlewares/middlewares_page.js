<<<<<<< HEAD
const jwt = require("jsonwebtoken");
require('dotenv').config();

const verifyJWT = (req, res, next) => {
  if (!req.headers["authorization"]) {
    return res.status(401).json({ message: "No Token Given", isLoggedIn: false });
  }

  const token = req.headers["authorization"].split(' ')[1];
  if (token) {
    jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
      if (err) return res.status(500).json({ message: "Failure to Auth", isLoggedIn: false });
      req.user = {};
      req.user.id = decoded.id;
      req.user.username = decoded.username;
      next();
    })
  } else {
    return res.status(401).json({ message: "Invalid Token Given", isLoggedIn: false });
  }
}

module.exports = {
  verifyJWT,
=======
$$imports$$
require('dotenv').config();

$$handler$$

module.exports = {
  $$exports$$
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
};