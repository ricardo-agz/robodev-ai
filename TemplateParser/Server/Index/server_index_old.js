const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
$$importJWT$$
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || $$PORT$$;
const corsOptions = {
  origin: "*"
}

// MIDDLEWARES
$$verifyJWT$$
app.use( express.json() );
app.use( cors(corsOptions) );

// MONGO DB CONNECTION
mongoose
  .connect(process.env.DB_CONNECTION, {
	  useNewUrlParser: true,
  })
  .then(() => {
    console.log("MongoDB connection successful");
  })
  .catch(err => {
    console.log("MongoDB connection failed:");
    console.log(err.stack);
    process.exit(1);
  }
);


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