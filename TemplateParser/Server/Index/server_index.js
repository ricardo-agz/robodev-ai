const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const jwt = require("jsonwebtoken");
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || $$PORT$$;
const corsOptions = {
  origin: "*"
}

app.use( express.json() );
app.use( cors(corsOptions) );

mongoose.connect(process.env.DB_CONNECTION, {
	useNewUrlParser: true,
});


function verifyJWT(req, res, next) {
  if (!req.headers["authorization"]) {
    return res.status(400).json({ message:"No Token Given", isLoggedIn: false });
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
    return res.status(400).json({ message: "Incorrect Token Given", isLoggedIn: false });
  }
}


// CONTROLLERS
$$dyn:0


// ROUTES
$$dyn:1
$$MANY_TO_MANY

// Default response for any other request
app.use((_req, res) => {
  res.status(404).send({ message: "404 not found" });
});

app.listen(
	PORT,
	console.log("Server running on port $$PORT$$...")
);