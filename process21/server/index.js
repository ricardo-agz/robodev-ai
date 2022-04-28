const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const jwt = require("jsonwebtoken");
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8080;
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
const UserController = require('./controllers/UserController');
const PaymentmethodController = require('./controllers/PaymentmethodController');
const MonthlypledgeController = require('./controllers/MonthlypledgeController');
const WorkoutplanController = require('./controllers/WorkoutplanController');
const WorkoutgroupController = require('./controllers/WorkoutgroupController');


// ROUTES
app.get('/users', UserController.index());
app.get('/user/:id', UserController.show());
app.post('/users', UserController.create());
app.put('/user/:id/edit', UserController.update());
app.delete('/user/:id', UserController.delete());
app.post('/users/:id/add-workoutgroup/:workoutgroupId', UserController.addWorkoutgroup());
app.post('/users/:id/drop-workoutgroup/:workoutgroupId', UserController.dropWorkoutgroup());

app.get('/paymentmethods', PaymentmethodController.index());
app.get('/paymentmethod/:id', PaymentmethodController.show());
app.post('/paymentmethods', PaymentmethodController.create());
app.put('/paymentmethod/:id/edit', PaymentmethodController.update());
app.delete('/paymentmethod/:id', PaymentmethodController.delete());

app.get('/monthlypledges', MonthlypledgeController.index());
app.get('/monthlypledge/:id', MonthlypledgeController.show());
app.post('/monthlypledges', MonthlypledgeController.create());
app.put('/monthlypledge/:id/edit', MonthlypledgeController.update());
app.delete('/monthlypledge/:id', MonthlypledgeController.delete());

app.('', WorkoutplanController.find());
app.('', WorkoutplanController.all());
app.post('/workoutplans', WorkoutplanController.create());
app.put('/workoutplan/:id/edit', WorkoutplanController.update());
app.delete('/workoutplan/:id', WorkoutplanController.delete());

app.get('/workoutgroups', WorkoutgroupController.index());
app.get('/workoutgroup/:id', WorkoutgroupController.show());
app.post('/workoutgroups', WorkoutgroupController.create());
app.put('/workoutgroup/:id/edit', WorkoutgroupController.update());
app.delete('/workoutgroup/:id', WorkoutgroupController.delete());
app.post('/workoutgroups/:id/add-member/:userId', WorkoutgroupController.addMember());
app.post('/workoutgroups/:id/drop-member/:userId', WorkoutgroupController.dropMember());


// Default response for any other request
app.use((_req, res) => {
  res.status(404).send({ message: "404 not found" });
});

app.listen(
	PORT,
	console.log("Server running on port 8080...")
);