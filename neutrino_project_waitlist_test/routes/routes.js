const express       = require('express');
const router        = express.Router();
module.exports      = router;

const AuthController = require('../controllers/AuthController');
const ApplicationController = require('../controllers/ApplicationController');
const AccessCodeController = require('../controllers/AccessCodeController');
const UserController = require('../controllers/UserController');

// Home
router.get('/', (_req, res) => {
  res.status(200).send({ message: 'Welcome to Neutrino!' });
});

router.post('/api/login', AuthController.login);
router.post('/api/register', AuthController.register);
router.post('/api/change-password/:id', AuthController.changePassword);

router.get('/api/applications', ApplicationController.index);
router.get('/api/applications/:id', ApplicationController.show);
router.post('/api/applications', ApplicationController.create);
router.put('/api/applications/:id', ApplicationController.update);
router.delete('/api/applications/:id', ApplicationController.delete);

router.get('/api/accesscodes', AccessCodeController.index);
router.get('/api/accesscodes/:id', AccessCodeController.show);
router.post('/api/accesscodes', AccessCodeController.create);
router.put('/api/accesscodes/:id', AccessCodeController.update);
router.delete('/api/accesscodes/:id', AccessCodeController.delete);
router.post('/api/access-codes/:id/use', AccessCodeController.useCode);

router.get('/api/users', UserController.index);
router.get('/api/users/:id', UserController.show);
router.put('/api/users/:id', UserController.update);
router.delete('/api/users/:id', UserController.delete);


// Default response for any other request
router.use((_req, res) => {
  res.status(404).send({ message: "404 not found" });
});