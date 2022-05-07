const express       = require('express');
const router        = express.Router();
module.exports      = router;

const UserController = require('../controllers/userController');
const PaymentMethodController = require('../controllers/paymentMethodController');
const MonthlyPledgeController = require('../controllers/monthlyPledgeController');
const WorkoutPlanController = require('../controllers/workoutPlanController');
const WorkoutGroupController = require('../controllers/workoutGroupController');
const AuthController = require('../controllers/authController');
const { verifyJWT } = require('./middlewares');


// Home
router.get('/', (_req, res) => {
  res.status(200).send({ message: 'Welcome to Neutrino!' });
});

// User
router.get('/users', verifyJWT, UserController.index);
router.get('/user/:id', verifyJWT, UserController.show);
router.post('/users', UserController.create);
router.put('/user/:id/edit', verifyJWT, UserController.update);
router.delete('/user/:id', verifyJWT, UserController.delete);
router.post('/users/:id/add-workoutgroup/:workoutGroupId', UserController.addWorkoutgroup);
router.post('/users/:id/drop-workoutgroup/:workoutGroupId', UserController.dropWorkoutgroup);
router.post('/users/:id/add-friend/:userId', UserController.addFriend);
router.post('/users/:id/drop-friend/:userId', UserController.dropFriend);

// PaymentMethod
router.get('/paymentmethods', PaymentMethodController.index);
router.get('/paymentmethod/:id', PaymentMethodController.show);
router.post('/paymentmethods', PaymentMethodController.create);
router.put('/paymentmethod/:id/edit', PaymentMethodController.update);
router.delete('/paymentmethod/:id', PaymentMethodController.delete);

// MonthlyPledge
router.get('/monthlypledges', MonthlyPledgeController.index);
router.get('/monthlypledge/:id', MonthlyPledgeController.show);
router.post('/monthlypledges', MonthlyPledgeController.create);
router.put('/monthlypledge/:id/edit', MonthlyPledgeController.update);
router.delete('/monthlypledge/:id', MonthlyPledgeController.delete);

// WorkoutPlan
router.get('/workoutplans', WorkoutPlanController.index);
router.get('/workoutplan/:id', WorkoutPlanController.show);
router.post('/workoutplans', WorkoutPlanController.create);
router.put('/workoutplan/:id/edit', WorkoutPlanController.update);
router.delete('/workoutplan/:id', WorkoutPlanController.delete);

// WorkoutGroup
router.get('/workoutgroups', WorkoutGroupController.index);
router.get('/workoutgroup/:id', WorkoutGroupController.show);
router.post('/workoutgroups', WorkoutGroupController.create);
router.put('/workoutgroup/:id/edit', WorkoutGroupController.update);
router.delete('/workoutgroup/:id', WorkoutGroupController.delete);
router.post('/workoutgroups/:id/add-member/:userId', WorkoutGroupController.addMember);
router.post('/workoutgroups/:id/drop-member/:userId', WorkoutGroupController.dropMember);

// Auth
router.post('/auth/login', AuthController.login);
router.post('/auth/register', AuthController.register);

// Default response for any other request
router.use((_req, res) => {
  res.status(404).send({ message: "404 not found" });
});